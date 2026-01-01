**Project: ****Serverless Image Processing Pipeline**

## Overview:

Using Lambda to trigger a function from an upload to an S3 bucket, the function will take the uploaded image and create a 128x128 thumbnail upload that thumbnail to a separate S3 bucket and log the metadata (Filename and Timestamp) into a DynamoDB table.

**Skills and Concepts Demonstrated**

**Identity and Access Management (IAM):** Securely granting permissions to compute resources using IAM Roles.

**S3 Access Control:** Implementing the principle of least privilege by restricting S3 access only to the necessary Lambda Role.

**Storage and Compute separation: **Separation of unstructured data from S3, the compute layer (Lambda) and the structured data in a DynamoDB table for better maintainability

**Serverless design: **Implementing an event driven architecture that eliminates idle server costs by using Lambda and event triggers (S3 event notifications)

**Architecture Overview (The Plan)**

**S3 Bucket:** The two buckets created will 1. Host the uploaded files triggering the lambda function and 2. Host the processed images.

**IAM Role:** This is the secure way to grant the Lambda function access to both the S3 buckets and the DynamoDB table.

**Lambda Layer****:** I’ll be using the Pillow library for python 3.14 which is not by default included within Lambda, so I’ll need to create a Lambda Layer and assign it to the function.

**DynamoDB****: **Create a DynamoDB table to host the Filename (partition key) and Timestamp (sort key) of the processed images.

**Lambda Function****:** This is where I’ll write my code to handle the image processing, the uploading of the edited image to the 2nd S3 bucket and the upload of the metadata to the DynamoDB.

**Section 1: ****Creation of the ****S3 Bucket****s, ****DynamoDB ****table and Lambda function**

**1. Creating ****the ****two S3 buckets**

First, I need to create a role that my EC2 instance can assume at launch. This is how I securely grant access to my S3 bucket.

Firstly, I’ll need to create two S3 buckets that will host my user uploaded images and the processed images. Then later well assign the necessary permissions to allow our Lambda function to access the buckets.

**Steps:**

Navigate to the S3 Console and select Create bucket.

Name the bucket I’ve gone with image-pipe-line-orig and image-pipe-line-resized for the two buckets.

Scroll to the bottom of the page and click the “Add new tag” button and assign any tags I’ve gone with Category > Image Pipeline for both the buckets.


**2. Creating ****the ****DynamoDB Table**

This Table will be where we hold all of our metadata the Filename and the Timestamp of the operation.

**Steps:**

Navigate to the DynamoDB console and click on the “Create table” button

Name the new table, I’ve gone with ImagePipeline as mine.

Add our Partition Key and our Sort Key. I’ve used FileName and TimeStamp

Leaving the table settings at default is the fastest way to create the table, we wont need to change anything here, most of the settings are adjustable after table creation anyway.

Like with the S3 bucket well add a tag to the table to help with organisation, I again have gone with Category > Image Pipeline

Click the “Create Table” button at the bottom.

**3. ****Creating ****the Lambda function.**

The Lambda function will be where the Python code will run to process the image and store the metadata into our DynamoDB

**Steps:**

Navigate to the Lambda console and click “Create function”

Make sure that “Author from scratch” is selected

Name the function, I’ve gone with Resize

Select the runtime, this is the language used to write the function, for this example I’m using Python 3.14

For the architecture I’m using x86_64

Expand the “Change default execution role” section and make a note of the role name that Lambda will create, later we will edit the permissions of the role to allow access to both S3 buckets as well as the DynamoDB table

Under additional configurations there will be the option to add a tag to the function and again, I’ve gone with Category > Image Pipeline


**Section 2: ****Permissions**

**Setting permissions for the two S3 buckets**

Both the buckets will need the proper policy adjustments to allow our Lambda function(The IAM role accossiated with the function) to ListBucket, GetBucketLocation, PutObject and  GetObject

**Steps:**

Navigate back to the first S3 bucket that was created

Click on the Permissions tab

Click edit on the “Bucket Policy” section

Adjust the policy to allow the S3 actions mentioned above and set the principle to the ARN of the role that Lambda created.

The “Resource” section needs to allow access to the bucket and to the objects inside.

Do this for both the buckets only thing that needs to change is the “Resource” section, just adjust the bucket name.

**2****. ****Setting permissions for the IAM role created by Lambda**


The Lambda created IAM role will need permissions to before being able to do anything with our S3 buckets, the objects within them and the DynamoDB table.

**Steps:**

Navigate to the IAM console and select the Roles section

Select the Lambda created role we made a note of before

By default, there will be a single Policy named “AWSLambdaBasic…” already attached we can ignore that, instead click on the “Add permissions” button

Select “Create inline policy” and change the tab to the “JSON” view

Add the same permission added to the S3 buckets 

Create a new inline policy, this time we will allow the function to access the DynamoDB (PutItem)

**Section ****3****: ****Lambda** **and verification**

### 3. Adding Pillow as a Lambda Layer

In order to use Pillow (Image processing lib for Python) we will need to package it and upload it as a Lambda Layer as its not included by default. Python will need to be installed on the machine, pip install will be used to create the Pillow package, I use Windows 11 so the packaging section will be done from within Command Prompt (CMD)

Steps:

Navigate to your Desktop (Or anywhere you want to create this package)

Create a Folder named Pillow_Layer

Create a subfolder named python (case sensitive) and open it

Open CMD and navigate to the python subfolder

Run the following command within CMD: 

pip install ^

--platform manylinux2014_x86_64 ^

--target python/ ^

--implementation cp ^

--python-version 3.14 ^

--only-binary=:all: Pillow

Once the Pillow package has been downloaded and stored within the python subfolder, we will need to create a zip file, right click the python subfolder and select “Compress to…” > “ZIP File”

Rename the zip file, I’ve gone with Pillow_Layer

Navigate to the Lambda Console

Select “Layers” on the left

Click “Create layer”

Give the new layer a name and a description

Upload the ZIP file created earlier

Click Create

### 4. Editing the Lambda function

Now comes the writing of the Lambda function, everything is in place for the function to be written, the S3 buckets, DynamoDB table, The various permissions and now finally the Pillow layer

Steps:

Navigate back to the Lambda console

Select the functions section

Navigate to the function created earlier

Under “Function overview” click “Add trigger”

Select S3 as the trigger

The bucket will be the host bucket (pre-processing)

Under event types I’ve deselected “All object create events” and only selected the “PUT” option

Acknowledge the “Recursive invocation” checkbox



Click “Add”

Scroll to the bottom of the page and select “Add layer”

Select either “Custom layers” or “Specify an ARN” and select the layer created earlier (or enter the layer ARN)


Click “Add”

Now time to actually write the function, I won’t go into detail here about how to use boto3 or how to write a python function but I’ll have the code available at the bottom of this document

**7****. Verification**** and code**

Once everything is done test the project by uploading an image to the host bucket and either check the CloudWatch for any errors but its more fun to check the other bucket and the DynamoDB table. 


| Purpose | Code |
| --- | --- |
| S3 Bucket Policies (Top one is for the host bucket, the bottom is for the resized bucket) | {<br>    "Version": "2012-10-17",<br>    "Statement": [<br>        {<br>            "Sid": "Allow Access",<br>            "Effect": "Allow",<br>            "Principal": {<br>                "AWS": [<br>                    "ARN"<br>                ]<br>            },<br>            "Action": [<br>                "s3:ListBucket",<br>                "s3:GetBucketLocation",<br>                "s3:PutObject",<br>                "s3:GetObject"<br>            ],<br>            "Resource": [<br>                "arn:aws:s3:::image-pipe-line-orig",<br>                "arn:aws:s3:::image-pipe-line-orig/*"<br>            ]<br>        }<br>    ]<br>}<br><br>{<br>    "Version": "2012-10-17",<br>    "Statement": [<br>        {<br>            "Sid": "Allow Access",<br>            "Effect": "Allow",<br>            "Principal": {<br>                "AWS": [<br>                    "ARN”<br>                ]<br>            },<br>            "Action": "s3:*",<br>            "Resource": [<br>                "arn:aws:s3:::image-pipe-line-resized",<br>                "arn:aws:s3:::image-pipe-line-resized/*"<br>            ]<br>        }<br>    ]<br>} |
| Lambda Bucket access | {<br>    "Version": "2012-10-17",<br>    "Statement": [<br>        {<br>            "Sid": "ImagePipeLineBucketAccess",<br>            "Effect": "Allow",<br>            "Action": [<br>                "s3:ListBucket",<br>                "s3:GetBucketLocation"<br>            ],<br>            "Resource": [<br>                "arn:aws:s3:::image-pipe-line-orig/",<br>                "arn:aws:s3:::image-pipe-line-resized/"<br>            ]<br>        },<br>        {<br>            "Effect": "Allow",<br>            "Action": [<br>                "s3:getObject",<br>                "s3:putObject"<br>            ],<br>            "Resource": [<br>                "arn:aws:s3:::image-pipe-line-orig/*",<br>                "arn:aws:s3:::image-pipe-line-resized/*"<br>            ]<br>        }<br>    ]<br>} |
| Lambda DynamoDB access | {<br>    "Version": "2012-10-17",<br>    "Statement": [<br>        {<br>            "Sid": "AddToDB",<br>            "Effect": "Allow",<br>            "Action": "dynamodb:PutItem",<br>            "Resource": "ARN"<br>        }<br>    ]<br>} |
| Lambda Python Code | import json<br>import boto3<br>import urllib.parse<br>import io<br>import datetime<br>from PIL import Image<br><br>s3=boto3.client("s3")<br>db=boto3.client("dynamodb")<br><br>def lambda_handler(event, context):<br>    timestamp=datetime.datetime.now().isoformat() #gets the timestamp to be uploaded into dynamodb<br>    <br>    uploadBucket='image-pipe-line-resized' #this is the bucket to place the resized images<br>    <br>    bucket=event['Records'][0]['s3']['bucket']['name'] #this gets the name of the bucket that triggered the function<br>    raw_key=event['Records'][0]['s3']['object']['key'] #this gets the name of the file that was uploaded to the bucket<br>    <br>    key=urllib.parse.unquote_plus(raw_key) #reformats the filename to remove url encoding<br>    file_name=key.split('/')[-1] #removes any "/" in the name<br>    #essentially turns "bucket/download%1" into "download 1"<br><br>    #the file by default is a dictornary/network stream, read the stream and transfer the data into the functions RAM as bytes to be read<br>    raw_image=s3.get_object(Bucket=bucket, Key=key)<br>    content_image = raw_image['Body'].read()<br>    #take the image and load it into memory as an object to be processed, process the image and again load it into RAM to be uploaded into a new S3 bucket<br>    image=Image.open(io.BytesIO(content_image))<br>    image.thumbnail((128,128))<br>    proc_image= io.BytesIO()<br>    image.save(proc_image, format='JPEG')<br>    proc_image.seek(0)<br>    #uploads the image into a different bucket<br>    s3.put_object(<br>        Bucket=uploadBucket,<br>        Key=key,<br>        Body=proc_image<br>    )<br>    #this will add our filename as well as the timestamp to our dynamodb<br>    db.put_item(<br>        TableName='ImagePipeline',<br>        Item={<br>            'FileName':{'S': file_name},<br>            'TimeStamp':{'S': timestamp}<br>        }<br>    )<br><br>    return{<br>        'statusCode': 200, <br>        'body': json.dumps({<br>        'message':'Success',<br>        'bucket':bucket,<br>        'key':raw_key,<br>        'file_name':file_name<br>        })}<br> |