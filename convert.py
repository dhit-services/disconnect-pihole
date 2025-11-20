#!/usr/bin/env python3
import json
import requests

URL = "https://raw.githubusercontent.com/disconnectme/disconnect-tracking-protection/master/services.json"
OUTFILE = "disconnect-pihole-list.txt"

def main():
    r = requests.get(URL, timeout=30)
    data = r.json()

    domains = set()

    for category, services in data.items():
        for name, entry in services.items():
            if isinstance(entry, dict):
                if "domain" in entry:
                    domains.add(entry["domain"])
                if "url" in entry:
                    domains.add(entry["url"])
                if "domains" in entry and isinstance(entry["domains"], list):
                    for d in entry["domains"]:
                        domains.add(d)

    with open(OUTFILE, "w") as f:
        for d in sorted(domains):
            f.write(d + "\n")

    print(f"Generated {OUTFILE} with {len(domains)} domains")

if __name__ == "__main__":
    main()
