#!/usr/bin/env python3
import json
import requests

# URL der Disconnect services.json
URL = "https://raw.githubusercontent.com/disconnectme/disconnect-tracking-protection/master/services.json"
OUTFILE = "disconnect-pihole-list.txt"

def extract_domains(entry, domains):
    """Extrahiert Domains rekursiv aus einem JSON-Eintrag."""
    if isinstance(entry, str):
        # Wenn es wie eine Domain aussieht, hinzufügen
        if any(c.isalnum() for c in entry) and '.' in entry:
            domains.add(entry.strip())
    elif isinstance(entry, dict):
        # Einzelne Domain
        if "domain" in entry and isinstance(entry["domain"], str):
            domains.add(entry["domain"].strip())
        if "url" in entry and isinstance(entry["url"], str):
            domains.add(entry["url"].strip())
        if "domains" in entry and isinstance(entry["domains"], list):
            for d in entry["domains"]:
                extract_domains(d, domains)
        # Untereinträge rekursiv durchgehen
        for key, subentry in entry.items():
            extract_domains(subentry, domains)
    elif isinstance(entry, list):
        for item in entry:
            extract_domains(item, domains)

def main():
    # JSON herunterladen
    r = requests.get(URL, timeout=30)
    data = r.json()

    domains = set()

    extract_domains(data, domains)

    # Datei schreiben, nur Domains, keine Lizenz- oder Kommentarzeilen
    with open(OUTFILE, "w") as f:
        for d in sorted(domains):
            # Filter: nur echte Domains, keine leeren Strings
            if d and '.' in d:
                f.write(d + "\n")

    print(f"Generated {OUTFILE} with {len(domains)} domains")

if __name__ == "__main__":
    main()


