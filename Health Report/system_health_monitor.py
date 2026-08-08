#!/usr/bin/env python3

"""
system_health_monitor.py
Generates a one-time system health report covering CPU,
RAM, disk, top processes, and network connectivity.

Requirements: pip install psutil
"""

import psutil
import socket
import subprocess
import datetime
import platform

# --- Thresholds ---
CPU_WARN = 80
RAM_WARN = 80
DISK_WARN = 80

# --- Colours ---
RED    = "\033[0;31m"
YELLOW = "\033[1;33m"
GREEN  = "\033[0;32m"
BLUE   = "\033[1;34m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

warnings = []


def badge(value, threshold):
    if value >= threshold:
        return f"{RED}[WARNING]{RESET}"
    return f"{GREEN}[OK]{RESET}"


def section(title):
    print(f"\n{BOLD}{BLUE}[ {title} ]{RESET}")


def header():
    now = datetime.datetime.now().strftime("%A %d %B %Y %H:%M:%S")
    uptime_seconds = datetime.datetime.now().timestamp() - psutil.boot_time()
    uptime = str(datetime.timedelta(seconds=int(uptime_seconds)))
    print(f"{BOLD}{BLUE}")
    print("============================================================")
    print("           SYSTEM HEALTH REPORT")
    print(f"============================================================{RESET}")
    print(f"  Host     : {BOLD}{socket.gethostname()}{RESET}")
    print(f"  Date     : {now}")
    print(f"  Uptime   : {uptime}")
    print(f"  OS       : {platform.system()} {platform.release()} ({platform.version()})")


def cpu_report():
    section("CPU")
    cpu_pct = psutil.cpu_percent(interval=1)
    load_1, load_5, load_15 = psutil.getloadavg()
    cores = psutil.cpu_count(logical=True)
    print(f"  Usage    : {BOLD}{cpu_pct}%{RESET} {badge(cpu_pct, CPU_WARN)}")
    print(f"  Load Avg : {load_1:.2f} / {load_5:.2f} / {load_15:.2f} (1m / 5m / 15m)")
    print(f"  Cores    : {cores}")
    if cpu_pct >= CPU_WARN:
        warnings.append(f"CPU usage is high: {cpu_pct}%")


def ram_report():
    section("MEMORY")
    mem = psutil.virtual_memory()
    total_mb = mem.total // (1024 ** 2)
    used_mb  = mem.used  // (1024 ** 2)
    free_mb  = mem.available // (1024 ** 2)
    pct      = mem.percent
    print(f"  Total    : {total_mb} MB")
    print(f"  Used     : {BOLD}{used_mb} MB ({pct}%){RESET} {badge(pct, RAM_WARN)}")
    print(f"  Free     : {free_mb} MB")
    if pct >= RAM_WARN:
        warnings.append(f"RAM usage is high: {pct}%")


def disk_report():
    section("DISK")
    print(f"  {'Mount':<20} {'Total':>8} {'Used':>8} {'Free':>8} {'Use%':>6}  Status")
    for part in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(part.mountpoint)
        except PermissionError:
            continue
        total_gb = usage.total / (1024 ** 3)
        used_gb  = usage.used  / (1024 ** 3)
        free_gb  = usage.free  / (1024 ** 3)
        pct      = usage.percent
        b = badge(pct, DISK_WARN)
        print(f"  {part.mountpoint:<20} {total_gb:>7.1f}G {used_gb:>7.1f}G {free_gb:>7.1f}G {pct:>5.1f}%  {b}")
        if pct >= DISK_WARN:
            warnings.append(f"Disk usage high on {part.mountpoint}: {pct}%")


def process_report():
    section("TOP 5 PROCESSES BY CPU")
    procs = sorted(psutil.process_iter(['pid', 'name', 'username', 'cpu_percent']),
                   key=lambda p: p.info['cpu_percent'] or 0, reverse=True)[:5]
    print(f"  {'USER':<15} {'PID':<8} {'CPU%':<8} COMMAND")
    for p in procs:
        user = p.info['username'] or 'unknown'
        print(f"  {user:<15} {p.info['pid']:<8} {p.info['cpu_percent']:<8} {p.info['name']}")


def network_report():
    section("NETWORK CONNECTIVITY")
    hosts = [("8.8.8.8", "Google DNS"), ("1.1.1.1", "Cloudflare DNS"),
             ("google.com", "google.com"), ("github.com", "github.com")]
    for host, label in hosts:
        result = subprocess.run(
            ["ping", "-c", "1", "-W", "2", host],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        dots = "." * (30 - len(label))
        if result.returncode == 0:
            print(f"  {label} {dots} {GREEN}REACHABLE{RESET}")
        else:
            print(f"  {label} {dots} {RED}UNREACHABLE{RESET}")


def summary():
    section("SUMMARY")
    if not warnings:
        print(f"  {GREEN}{BOLD}All systems healthy. No issues detected.{RESET}")
    else:
        for w in warnings:
            print(f"  {RED}! {w}{RESET}")
        print(f"\n  {YELLOW}{BOLD}{len(warnings)} warning(s) detected. Review items above.{RESET}")

    print(f"\n{BOLD}{BLUE}============================================================{RESET}")
    print(f"  Report complete: {datetime.datetime.now().strftime('%H:%M:%S')}")
    print(f"{BOLD}{BLUE}============================================================{RESET}\n")


if __name__ == "__main__":
    header()
    cpu_report()
    ram_report()
    disk_report()
    process_report()
    network_report()
    summary()
