# IT Support Fix-It Log

A log of real hardware, software and network issues I've diagnosed and resolved, written up in a helpdesk ticket format to reflect how I'd document a resolved issue in a support role.

---

## Ticket 001: Intermittent Wi-Fi Drops and Slow Connection Speeds

**Reported Issue:** Wi-Fi connection was dropping intermittently and running noticeably slower than expected, affecting all devices on the network.

**Diagnosis Steps:**
1. Checked signal strength and router placement, connection was weaker in rooms further from the router, indicating possible positional interference.
2. Reviewed the Wi-Fi channel the router was broadcasting on, found it was on a channel shared with several nearby networks, likely causing congestion.
3. Tested DNS resolution speed using the default ISP DNS versus a public DNS provider.

**Resolution:**
- Repositioned the router to a more central, elevated location to improve signal coverage across the property.
- Manually changed the router's Wi-Fi channel to a less congested one to reduce interference from neighbouring networks.
- Switched DNS settings to a faster public DNS provider, improving page load and connection response times.

**Outcome:** Connection stability and speed improved immediately after the channel change and DNS switch, with no further drops reported.

**Skills demonstrated:** Network troubleshooting, router configuration, DNS management, systematic diagnosis (ruling out causes one at a time rather than guessing).

---

## Ticket 002: Driver Conflicts Following Bulk Software Installation

**Reported Issue:** After a bulk software install, certain hardware components were behaving unexpectedly, with driver related issues appearing across a few devices.

**Diagnosis Steps:**
1. Used Ninite to bulk install a standard set of applications across a machine, a common approach for setting up a system quickly with commonly used software.
2. After installation, identified that some hardware wasn't functioning as expected, pointing to a driver conflict or an outdated driver not being picked up automatically.
3. Opened Windows Device Manager to check for devices flagged with errors or warning icons, and ran a scan for hardware changes to force Windows to re-detect affected devices.
4. Ran Windows Update to check for and install any available driver updates.
5. For devices where Windows Update didn't resolve the issue, went directly to the manufacturer's website to download and install the correct, up to date driver.

**Resolution:** Combination of a Windows Update pass and manually sourcing manufacturer specific drivers resolved the conflicts, with all hardware returning to normal function.

**Outcome:** All affected devices worked correctly after driver updates were applied, confirmed by testing each one individually.

**Skills demonstrated:** Software deployment (bulk installation tooling), Windows Device Manager troubleshooting, driver management, methodically isolating and testing fixes per device rather than a blanket reinstall.

---

## Ticket 003: New Printer Setup and Network Configuration

**Reported Issue:** New printer needed to be set up and made available to a host PC on the network.

**Diagnosis Steps:**
1. Connected the printer to the home Wi-Fi network directly through the printer's own setup menu.
2. Confirmed the printer was visible on the network and reachable from the host PC.

**Resolution:**
- Installed the required printer drivers and accompanying software onto the host PC.
- Verified the printer was correctly detected and set as available for print jobs.

**Outcome:** Printer connected successfully to the network and was fully functional from the host PC, confirmed with a test print.

**Skills demonstrated:** Peripheral setup and configuration, network device connectivity, driver installation.

---

## Ticket 004: Intermittent Memory Instability Traced to CPU Socket Contamination

**Reported Issue:** Custom built PC was experiencing random memory instability, with the system behaving as though only a single channel of dual channel RAM was being detected and used.

**Diagnosis Steps:**
1. Ruled out the RAM sticks and DIMM slots first by testing each stick individually in different slots, which pointed away from the RAM or slots themselves being faulty.
2. Investigated further and traced the issue down to the physical layer, checking the CPU socket pins for contact or damage issues.
3. Found thermal paste contamination on the CPU socket pins, which was degrading electrical contact to one of the memory channels.

**Resolution:**
- Carefully cleaned the thermal paste contamination from the CPU socket pins.
- Reseated the CPU and confirmed the system was correctly detecting and running in full dual channel mode.
- Went a step further and optimised system performance by enabling DOCP for stable memory speeds and applying safe undervolting for improved thermal performance.

**Outcome:** System stabilised fully in dual channel mode with no further memory issues, and ran with improved performance and thermals following the additional optimisation.

**Skills demonstrated:** Hardware level diagnosis, methodical elimination of likely causes before assuming the root cause, physical troubleshooting beyond software or settings level checks, and a willingness to go beyond the minimum fix to improve overall system performance.

---

## Why I Keep This Log

Documenting resolved issues clearly, including what was tried, what worked, and why, is a habit I want to carry into a support role. Clear documentation makes it easier for a team to spot recurring issues, hand off unresolved tickets, and build a knowledge base over time. This log reflects the same structured, step by step approach I'd bring to logging and resolving tickets in a live service desk environment.
