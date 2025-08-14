import subprocess
import sys

REQUIRED_PACKAGES = [
    "beautifulsoup4", 
    "requests", 
    "colorama", 
    "phonenumbers", 
    "tqdm"
]

def install_missing_packages():
    """Check and install missing packages."""
    for package in REQUIRED_PACKAGES: 
        try: 
            __import__(package if package != "beautifulsoup4" else "bs4")
        except:
            print(f"[INFO] Installing missing package: {package}")
            subprocess.check_call([sys.executable, "-m", "pip3", "install", package])

install_missing_packages()

import argparse
from scraper.scraper import fetch_html
from scraper.extractors import extract_emails, extract_links, extract_social_links, extract_author_names, extract_phone_numbers
from scraper.output import print_to_terminal, save_to_file

def main():
    parser = argparse.ArgumentParser(description="Web Scraping Tool ;D")
    parser.add_argument("--url", required=True, help="URL to scrape")
    parser.add_argument("--output", choices=["terminal", "file"], default="terminal", help="Output mode")
    parser.add_argument("--format", choices=["txt", "json", "csv"], default="txt", help="File format if saving")
    parser.add_argument("--filename", default="output.txt", help="Filename for scraped data!")
    parser.add_argument("--country", default="US", help="Country code for phone number parsing (e.g., PL, US, DEs)")
    args = parser.parse_args()

    html = fetch_html(args.url)
    if not html: 
        return 
    data = {
        "links": extract_links(html), 
        "emails": extract_emails(html), 
        "social": extract_social_links(html),
        "authors": extract_author_names(html),
        "phones": extract_phone_numbers(html, args.country)
    }

    if args.output == "terminal":
        print_to_terminal(data)
    else:
        save_to_file(data, args.filename, args.format)
        print(f"Data saved to: {args.filename}")

if __name__ == "__main__":
    main()