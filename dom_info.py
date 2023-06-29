import dns.resolver
import time

# ANSI escape codes for color formatting
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

domain = "example.com"
record_types = ["A", "AAAA"]

with open("subdomains.txt") as file:
    subdomains = file.read().splitlines()

for subdomain in subdomains:
    full_domain = subdomain + "." + domain

    for record_type in record_types:
        try:
            answers = dns.resolver.resolve(full_domain, record_type)
            if answers:
                for answer in answers:
                    print(f"{GREEN}{record_type} record found for {full_domain}: {answer}{RESET}")
        except dns.resolver.NoAnswer:
            pass  # No DNS record found for the specific record type
        except dns.resolver.NXDOMAIN:
            pass  # Domain does not exist
        except dns.resolver.Timeout:
            pass  # DNS resolution timed out

    # If none of the record types resulted in a match, consider the subdomain as not having any DNS records
    try:
        resolved = dns.resolver.resolve(full_domain)
        if not resolved.rrset:
            print(f"{RED}No DNS records found for {full_domain}{RESET}")
    except dns.resolver.NXDOMAIN:
        print(f"{RED}Domain {full_domain} does not exist.{RESET}")
    except dns.resolver.Timeout:
        print(f"{RED}DNS resolution timed out for {full_domain}.{RESET}")

    # Check DNS propagation status
    for record_type in record_types:
        try:
            answers = dns.resolver.resolve(full_domain, record_type)
            if answers:
                print(f"{GREEN}DNS records exist for {full_domain}, indicating DNS propagation completed.{RESET}")
                break
        except dns.resolver.NXDOMAIN:
            print(f"{RED}Domain {full_domain} does not exist.{RESET}")
            break
        except dns.resolver.Timeout:
            print(f"{RED}DNS resolution timed out for {full_domain}.{RESET}")

    # Wait for a delay before checking the next subdomain (adjust as needed)
    time.sleep(1)
