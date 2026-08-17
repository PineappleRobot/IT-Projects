# New Starter Device Setup and Domain Join

A documented walkthrough of setting up a new client machine and joining it to an Active Directory domain, simulating the process of provisioning a device for a new starter. Built using two separate VirtualBox VMs, a Windows Server domain controller and a Windows client, on a shared network.

## Environment

- Windows Server (Evaluation), domain controller for ish.lab
- Windows 10/11 client VM
- VirtualBox, both VMs networked together
- Domain: ish.lab

## 1. Identifying the Server's Network Configuration

Checked the domain controller's current network configuration to confirm its IP address, required for pointing the client machine's DNS at the domain.

![Server IP Configuration](images/ServerIP.png)

Initial `ipconfig` output showed the server's IPv4 address as 192.168.10.10, with no default gateway configured, since this had been running as a static, isolated lab network without DHCP.

## 2. Setting Up DHCP

When bringing the second VM online to join the domain, DHCP was not yet running on the network, meaning the client had no way to automatically obtain an IP address, gateway or DNS settings. Rather than manually configuring static IPs on every future client, the more realistic and scalable approach was to install and configure the DHCP Server role on the domain controller, mirroring how most real organisations provision new devices.

### Installing the DHCP Server Role

Added the DHCP Server role through Server Manager's Add Roles and Features wizard, alongside the required management tools.

![DHCP Server Role Installation](images/DHCPServerRole.png)

### Creating a New Scope

Configured a new DHCP scope to define the range of IP addresses available for client devices on the network.

![New Scope Wizard](images/DHCPNewScope.png)

### Defining the IP Address Range

Set the scope to distribute addresses from 192.168.10.11 to 192.168.10.200, keeping 192.168.10.10 reserved for the domain controller itself, with a subnet mask of 255.255.255.0.

![Scope IP Address Range](images/ScopeIPRange.png)

### Setting the Default Gateway

Configured the router (default gateway) setting propagated to DHCP clients as 192.168.10.10, the domain controller, matching how the lab network was structured.

![Default Gateway Configuration](images/DefaultGatewayDHCPSetup.png)

## 3. Joining the Client to the Domain

With DHCP running, the client VM was able to automatically obtain an IP address, gateway and DNS settings pointing back to the domain controller. From there, the client was joined to the ish.lab domain through System Properties, authenticated with domain administrator credentials, and restarted to complete the join.

## 4. Logging In With a Domain Account

Confirmed the domain join was successful by logging into the client machine using the previously created domain user account, JSmith1@ish.lab, rather than a local account.

![Domain User Login](images/UserLogin.png)

The login screen confirms the machine is signing in to the ish.lab domain, verifying the client is correctly joined and able to authenticate against Active Directory.

## Summary

Set up a second VM as a Windows client and joined it to the ish.lab domain. Discovered DHCP was not yet configured on the network, so installed the DHCP Server role on the domain controller, created a scope covering 192.168.10.11 to 192.168.10.200, and set the default gateway to point back to the domain controller. Once the client picked up an IP address and DNS settings automatically, joined it to the domain and confirmed the setup worked by logging in with the JSmith1@ish.lab domain account.
