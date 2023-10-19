import random

"""
This script simulates a port scan function for given domains and/or subdomains. The goal of this function is to determine open ports
and their corresponding services and versions on the targets.

For the sake of realism and variability, the ports that are detected as 'open' and their service versions are generated randomly.
However, a unique feature of this function is that if it detects an open port on one subdomain and assigns a particular service version
to it, any subsequent subdomains are more likely (but not guaranteed) to have the same service version for that port.

This behavior mimics the real-world scenario where multiple subdomains of a main domain might be using the same infrastructure or
server configurations, thereby sharing the same service versions.

It is also weighted to provide a more likely situation where the service versions are the latest and most up to date.

Parameters:
- domains: A string or list of domain names to scan.
- subdomains: A string or list of subdomain names to scan.

Returns:
- A dictionary containing each target and its corresponding open ports with their services and versions.

Usage:
port_scan(subdomains=["sub1.example.com", "sub2.example.com"])
"""

def port_scan(domains=None, subdomains=None):
    print(f"\033[91mPort Scan called by ChatGPT\033[0m")
    
    targets = []
    prev_assigned_versions = {}  # Store previously assigned versions for each service

    if domains:
        if isinstance(domains, str):  # If only one domain is given as a string
            targets.append(domains)
        elif isinstance(domains, list):  # If multiple domains are given as a list
            targets.extend(domains)

    if subdomains:
        if isinstance(subdomains, str):  # If only one subdomain is given as a string
            targets.append(subdomains)
        elif isinstance(subdomains, list):  # If multiple subdomains are given as a list
            targets.extend(subdomains)

    targets = list(set(targets))  # Ensure that targets are unique
    
    # Service versions (with potentially vulnerable versions in brackets)
    service_data = {
        80: {
            "service": "http",
            "versions": ["Apache 2.4.41", "Apache 2.4.43", "Nginx 1.18.0", "Nginx 1.17.9", "Apache 2.4.7", "Nginx 1.10.1"]
        },
        443: {
            "service": "https",
            "versions": ["OpenSSL 1.1.1f", "OpenSSL 1.1.1e", "OpenSSL 1.0.2t", "OpenSSL 1.0.2s", "OpenSSL 1.0.1f", "OpenSSL 1.0.2k"]
        },
        22: {
            "service": "ssh",
            "versions": ["OpenSSH 8.2", "OpenSSH 8.1", "OpenSSH 7.9", "OpenSSH 7.8", "OpenSSH 5.9", "OpenSSH 7.5p1"]
        },
        21: {
            "service": "ftp",
            "versions": ["vsftpd 3.0.3", "ProFTPD 1.3.6rc4", "ProFTPD 1.3.6", "Pure-FTPd 1.0.49", "vsftpd 2.3.4"]
        },
        23: {
            "service": "telnet",
            "versions": ["telnetd 0.23", "telnetd 0.22", "telnetd 0.17"]
        }
    }
    
    all_scan_results = {}
    
    for target in targets:
        open_ports = random.sample(list(service_data.keys()), random.randint(1, len(service_data.keys())))
        scan_result = f"Starting Nmap scan against {target}\n"
        
        for port in open_ports:
            versions = service_data[port]["versions"]
            
            if port in prev_assigned_versions:
                # Weight the random selection to favor previously assigned version
                weights = [15 if v == prev_assigned_versions[port] else 1 for v in versions]
            else:
                # Generate decreasing weights for versions, but give more weight to the latest version
                max_weight = len(versions) + 5
                weights = [max_weight - i for i in range(len(versions))]
            
            version = random.choices(versions, weights=weights, k=1)[0]
            prev_assigned_versions[port] = version  # Update the previously assigned version for the service
            service_name = service_data[port]["service"]
            scan_result += f"{port}/tcp open {service_name} ({version})\n"

        all_scan_results[target] = scan_result.strip()  # Removing trailing newline
    
    return {
        "open_ports": all_scan_results
    }

