#!/usr/bin/env python3

"""
log_analyser.py
Analyses a Linux system log file, categorises entries by severity,
identifies the most frequent error sources, and outputs a clean report.

Usage:
    python3 log_analyser.py
    python3 log_analyser.py --log /var/log/syslog
    python3 log_analyser.py --log /var/log/auth.log
"""

import argparse
import os
import re
import datetime
from collections import Counter

# --- Colours ---
RED    = "\033[0;31m"
YELLOW = "\033[1;33m"
GREEN  = "\033[0;32m"
BLUE   = "\033[1;34m"
BOLD   = "\033[1m"
RESET  = "\033[0m"


def section(title):
    print(f"\n{BOLD}{BLUE}[ {title} ]{RESET}")


def header(log_path, total_lines):
    print(f"{BOLD}{BLUE}")
    print("============================================================")
    print("           LOG FILE ANALYSIS REPORT")
    print(f"============================================================{RESET}")
    print(f"  File     : {BOLD}{log_path}{RESET}")
    print(f"  Date     : {datetime.datetime.now().strftime('%A %d %B %Y %H:%M:%S')}")
    print(f"  Lines    : {total_lines:,}")


def categorise(line):
    line_lower = line.lower()
    if any(k in line_lower for k in ["error", "failed", "failure", "critical", "fatal", "emerg", "alert"]):
        return "ERROR"
    elif any(k in line_lower for k in ["warn", "warning"]):
        return "WARNING"
    else:
        return "INFO"


def extract_service(line):
    """Extract the service/process name from a syslog-format line."""
    match = re.search(r'\w+ +\d+ \d+:\d+:\d+ \S+ (\S+?)[\[:]', line)
    if match:
        return match.group(1).strip()
    return "unknown"


def analyse(log_path):
    counts = Counter({"ERROR": 0, "WARNING": 0, "INFO": 0})
    error_lines = []
    warning_lines = []
    service_errors = Counter()
    service_warnings = Counter()

    try:
        with open(log_path, "r", errors="replace") as f:
            lines = f.readlines()
    except PermissionError:
        print(f"{RED}Permission denied: try running with sudo.{RESET}")
        return
    except FileNotFoundError:
        print(f"{RED}Log file not found: {log_path}{RESET}")
        return

    total = len(lines)
    header(log_path, total)

    for line in lines:
        cat = categorise(line)
        counts[cat] += 1
        service = extract_service(line)

        if cat == "ERROR":
            error_lines.append(line.strip())
            service_errors[service] += 1
        elif cat == "WARNING":
            warning_lines.append(line.strip())
            service_warnings[service] += 1

    # --- Breakdown ---
    section("SEVERITY BREAKDOWN")
    error_pct   = (counts["ERROR"]   / total * 100) if total else 0
    warning_pct = (counts["WARNING"] / total * 100) if total else 0
    info_pct    = (counts["INFO"]    / total * 100) if total else 0

    print(f"  {RED}Errors   : {counts['ERROR']:>6,}  ({error_pct:.1f}%){RESET}")
    print(f"  {YELLOW}Warnings : {counts['WARNING']:>6,}  ({warning_pct:.1f}%){RESET}")
    print(f"  {GREEN}Info     : {counts['INFO']:>6,}  ({info_pct:.1f}%){RESET}")

    # --- Top error sources ---
    section("TOP 5 ERROR SOURCES (by service)")
    if service_errors:
        for service, count in service_errors.most_common(5):
            print(f"  {RED}{service:<30}{RESET}  {count} error(s)")
    else:
        print(f"  {GREEN}No errors found.{RESET}")

    # --- Top warning sources ---
    section("TOP 5 WARNING SOURCES (by service)")
    if service_warnings:
        for service, count in service_warnings.most_common(5):
            print(f"  {YELLOW}{service:<30}{RESET}  {count} warning(s)")
    else:
        print(f"  {GREEN}No warnings found.{RESET}")

    # --- Recent errors ---
    section("LAST 5 ERRORS")
    if error_lines:
        for line in error_lines[-5:]:
            print(f"  {RED}{line[:120]}{RESET}")
    else:
        print(f"  {GREEN}No errors found.{RESET}")

    # --- Recent warnings ---
    section("LAST 5 WARNINGS")
    if warning_lines:
        for line in warning_lines[-5:]:
            print(f"  {YELLOW}{line[:120]}{RESET}")
    else:
        print(f"  {GREEN}No warnings found.{RESET}")

    # --- Summary ---
    section("SUMMARY")
    if counts["ERROR"] == 0 and counts["WARNING"] == 0:
        print(f"  {GREEN}{BOLD}No errors or warnings found. Log looks clean.{RESET}")
    else:
        if counts["ERROR"] > 0:
            print(f"  {RED}! {counts['ERROR']} error(s) detected — review top error sources above.{RESET}")
        if counts["WARNING"] > 0:
            print(f"  {YELLOW}! {counts['WARNING']} warning(s) detected — review top warning sources above.{RESET}")

    print(f"\n{BOLD}{BLUE}============================================================{RESET}")
    print(f"  Analysis complete: {datetime.datetime.now().strftime('%H:%M:%S')}")
    print(f"{BOLD}{BLUE}============================================================{RESET}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Linux Log File Analyser")
    parser.add_argument(
        "--log",
        default="/var/log/syslog",
        help="Path to log file (default: /var/log/syslog)"
    )
    args = parser.parse_args()
    analyse(args.log)
