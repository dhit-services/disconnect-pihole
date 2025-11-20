#!/usr/bin/env python3
import json
import requests

URL = "https://raw.githubusercontent.com/disconnectme/disconnect-tracking-protection/master/services.json"
OUTFILE = "disconnect-pihole-list.txt"

def extract_domains(entry, domains):
    """Extract domain information from any entry"""
    if isinstance(entry, dict):
        # Single domain
        if "domain" in entry and isinstance(entry["domain"], str):
            domains.add(entry["domain"])

        # URL sometimes used instead of domain
        if "url" in entry and isinstance(entry["url"], str):
            domains.add(entry["url"])

        # lists of domains
        if "domains" in entry and isinstance(entry["domains"], list):
            for d in entry["domains"]:
                if isinstance(d, str):
                    domains.add(d)


def main():
    r = requests.get(URL, timeout=30)
    data = r.json()

    domains = set()

    for category, services in data.items():

        # category may be a string or something unexpected
        if not isinstance(services, dict):
            continue

        for name, entry in services.items():

            # some entries may be strings
            if isinstance(entry, str):
                continue

            # extract domains
            extract_domains(entry, domains)

    # write sorted output file
    with open(OUTFILE, "w") as f:
        for d in sorted(domains):
            f.write(d + "\n")

    print(f"Generated {OUTFILE} with {len(domains)} domains")

if __name__ == "__main__":
    main()
