import requests
from bs4 import BeautifulSoup
import sys

def fetch(url: str):
    print(f"fetching '{url}'")
    r = requests.get(url)
    return r.text

if __name__ == "__main__":
    url =  "https://nixos.org/manual/nixos/stable/release-notes"
    html = fetch(url)
    
    soup = BeautifulSoup(html, "html.parser")

    versions = set()
    for link in soup.select(".toc a"):
        text = link.text.strip()
        if text.startswith("Release"):
            parts = text.split()
            if len(parts) > 1:
                version = parts[1]
                versions.add(version)

    sorted = sorted(versions, key=lambda v: tuple(map(int, v.split('.'))))
    
    if sorted.__len__().__eq__(0):
        print("No available versions found")
        sys.exit()

    print("Available NixOS versions:")
    for version in sorted:
        print(f"- {version}")
