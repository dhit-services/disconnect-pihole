

#!/usr/bin/env python3
import json
import requests

# URL der Disconnect services.json
URL = "https://raw.githubusercontent.com/disconnectme/disconnect-tracking-protection/master/services.json"
OUTFILE = "disconnect-pihole-list.txt"

def is_valid_domain(d):
    """Prüft, ob der String wie eine echte Domain aussieht."""
    d = d.strip()
    if not d:
        return False
    if '.' not in d:
        return False
    if ' ' in d:
        return False
    if d.lower().startswith("copyright"):
        return False
    if d.lower().startswith("http://") or d.lower().startswith("https://"):
        return False
    return True

def extract_domains(entry, domains):
    """Extrahiert Domains rekursiv aus einem JSON-Eintrag."""
    if isinstance(entry, str):
        if is_valid_domain(entry):
            domains.add(entry.strip())
    elif isinstance(entry, dict):
        # Einzelne Domain
        if "domain" in entry and isinstance(entry["domain"], str) and is_valid_domain(entry["domain"]):
            domains.add(entry["domain"].strip())
        if "url" in entry and isinstance(entry["url"], str) and is_valid_domain(entry["url"]):
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

    # Datei schreiben, nur gültige Domains
    with open(OUTFILE, "w") as f:
        for d in sorted(domains):
            f.write(d + "\n")

    print(f"Generated {OUTFILE} with {len(domains)} domains")

if __name__ == "__main__":
    main()
