#!/usr/bin/env python3
import json
import requests

URL = "https://raw.githubusercontent.com/disconnectme/disconnect-tracking-protection/master/services.json"
OUTFILE = "disconnect-pihole-list.txt"

def extract_from_entry(entry, domains):
    """Versucht, Domains aus entry zu extrahieren, unabhängig vom Typ."""
    if isinstance(entry, dict):
        # Wenn dict, wie gehabt
        if "domain" in entry and isinstance(entry["domain"], str):
            domains.add(entry["domain"])
        if "url" in entry and isinstance(entry["url"], str):
            domains.add(entry["url"])
        if "domains" in entry and isinstance(entry["domains"], list):
            for d in entry["domains"]:
                if isinstance(d, str):
                    domains.add(d)
    elif isinstance(entry, list):
        # Falls entry eine Liste ist, sie durchgehen
        for item in entry:
            extract_from_entry(item, domains)
    elif isinstance(entry, str):
        # Wenn einfach ein String ist, nehmen wir ihn als Domain an
        domains.add(entry)

def main():
    r = requests.get(URL, timeout=30)
    data = r.json()

    domains = set()

    # Über alle Schlüssel in der JSON iterieren
    for key, value in data.items():
        # value kann ein dict, list oder string sein
        extract_from_entry(value, domains)

        # Wenn value dict, vielleicht Services in value
        if isinstance(value, dict):
            for subkey, subentry in value.items():
                extract_from_entry(subentry, domains)

    # Domains sortieren und in Datei schreiben
    with open(OUTFILE, "w") as f:
        for d in sorted(domains):
            f.write(d + "\n")

    print(f"Generated {OUTFILE} with {len(domains)} domains")

if __name__ == "__main__":
    main()

