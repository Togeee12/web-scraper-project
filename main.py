import subprocess
import sys
import queue
import argparse
import re
import time
import threading
import json
import os

from scraper.extractors import (
    extract_emails, 
    extract_links, 
    extract_social_links, 
    extract_author_names, 
    extract_phone_numbers, 
    extract_images, 
    extract_metadata, 
    extract_document_links, 
    extract_tables
)

from scraper.output import (
    print_to_terminal, 
    save_to_file
)

from concurrent.futures import (
    ThreadPoolExecutor, 
    as_completed
)

from scraper.scraper import fetch_html
from tqdm import tqdm

REQUIRED_PACKAGES = [
    "beautifulsoup4", 
    "requests", 
    "colorama", 
    "phonenumbers", 
    "tqdm",
    "pandas",
    "openpyxl",
    "schedule",
    "whois",
    "dnspython",
    "textblob",
    "langdetect"
]

DOWNLOAD_IMAGES = False

def install_missing_packages():
    """Check and install missing packages."""
    for package in REQUIRED_PACKAGES:
        try:
            __import__(package if package != "beautifulsoup4" else "bs4")
        except ImportError:
            print(f"[I] Installing missing package: {package}")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install_missing_packages()

def scrape_recursive(url, depth=1, max_depth=1, visited=None, country="US", accumulated_data=None):
    """Recursively scrape a website up to specified depth with deduplication."""
    if visited is None:
        visited = set()
    
    if accumulated_data is None:
        accumulated_data = {
            "links": set(),
            "emails": set(),
            "social": {},
            "authors": set(),
            "phones": set(),
            "images": set(),
            "metadata": {},
            "documents": set(),
            "tables": []
        }

    if url in visited or depth > max_depth:
        return accumulated_data
    
    visited.add(url)
    print(f"Scraping: {url} Depth: {depth}")

    html = fetch_html(url)
    if not html: 
        return accumulated_data
    
    page_data = {
        "links": set(extract_links(html)), 
        "emails": set(extract_emails(html)), 
        "social": extract_social_links(html), 
        "authors": set(extract_author_names(html)), 
        "phones": set(extract_phone_numbers(html, country)),
        "images": set(extract_images(html, download=DOWNLOAD_IMAGES)), 
        "metadata": extract_metadata(html), 
        "documents": set(extract_document_links(html)),
        "tables": extract_tables(html)
    }
    
    accumulated_data["links"].update(page_data["links"])
    accumulated_data["emails"].update(page_data["emails"])
    accumulated_data["authors"].update(page_data["authors"])
    accumulated_data["phones"].update(page_data["phones"])
    accumulated_data["images"].update(page_data["images"])
    accumulated_data["documents"].update(page_data["documents"])
    
    for platform, links in page_data["social"].items():
        if platform not in accumulated_data["social"]:
            accumulated_data["social"][platform] = set()
        accumulated_data["social"][platform].update(links)
    
    if not accumulated_data["metadata"] and page_data["metadata"]:
        accumulated_data["metadata"] = page_data["metadata"]
    
    accumulated_data["tables"].extend(page_data["tables"])

    if depth < max_depth:
        internal_links = [
            link for link in page_data["links"]
            if link.startswith('/') or url.split('/')[2] in link
        ]

        for link in internal_links:
            if link.startswith('/'):
                base_url = '/'.join(url.split('/')[:3])
                link = base_url + link

            accumulated_data = scrape_recursive(link, depth + 1, max_depth, visited, country, accumulated_data)
    
    if depth == 1:
        result = {
            "url": url,
            "depth": depth,
            "links": list(accumulated_data["links"]),
            "emails": list(accumulated_data["emails"]),
            "social": {platform: list(links) for platform, links in accumulated_data["social"].items()},
            "authors": list(accumulated_data["authors"]),
            "phones": list(accumulated_data["phones"]),
            "images": list(accumulated_data["images"]),
            "metadata": accumulated_data["metadata"],
            "documents": list(accumulated_data["documents"]),
            "tables": accumulated_data["tables"]
        }
        return result
    
    return accumulated_data


def scrape_parallel(urls, country="US", max_workers=5):
    """Scrape multiple URLs in parallel."""
    results = {}
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_url = {
            executor.submit(fetch_and_extract, url, country): url 
            for url in urls
        }
        
        for future in tqdm(as_completed(future_to_url), total=len(urls), desc="Scraping URLs"):
            url = future_to_url[future]
            try:
                data = future.result()
                results[url] = data
            except Exception as e:
                print(f"Error scraping {url}: {e}")
                results[url] = {"error": str(e)}
    return results

def fetch_and_extract(url, country="US"):
    """Fetch HTML from a URL and extract all data."""
    try:
        html = fetch_html(url)
        if not html: 
            return {"error": "Failed to fetch HTML"}
    
        return {
            "url": url, 
            "links":        extract_links(html), 
            "social":       extract_social_links(html), 
            "authors":      extract_author_names(html), 
            "phones":       extract_phone_numbers(html, country), 
            "images":       extract_images(html, download=DOWNLOAD_IMAGES), 
            "metadata":     extract_metadata(html), 
            "documents":    extract_document_links(html), 
            "tables":       extract_tables(html)
        }
    except Exception as e:
        return {"error": f"\nError processing {url}: {str(e)}"}

def schedule_scraping(url, interval_hours=24, output_file="scheduled_output.json", country="US"):
    """Schedule scraping to return at regular intervals."""
    import schedule

    def job():
        print(f"Running scheduled scraping at {time.strftime('%Y-%m-%d %H-%M-%S')}")
        html = fetch_html(url)
        if not html: 
            print("Failed to fetch HTML")
            return 
        
        data = {
            "timestamp": time.strftime('%Y-%m-%d %H:%M:%S'), 
            "url": url, 
            "links":        extract_links(html), 
            "emails":       extract_emails(html), 
            "social":       extract_social_links(html), 
            "authors":      extract_author_names(html),
            "phones":       extract_phone_numbers(html, country),
            "images":       extract_images(html, download=DOWNLOAD_IMAGES), 
            "metadata":     extract_metadata(html),
            "documents":    extract_document_links(html),
            "tables":       extract_tables(html)
        }

        try:
            with open(output_file, 'r') as f:
                existing_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            existing_data = []

        existing_data.append(data)

        with open(output_file, 'w') as f:
            json.dump(existing_data, f, indent=4)

        print(f"Data appended to {output_file}")

    schedule.every(interval_hours).hours.do(job)
    print(f"Scheduled scraping every {interval_hours} hours. Press CTRL+C to exit.")

    try: 
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt: 
        print("\nScheduled scraping stopped.")

def filter_data(data, keyword=None, regex_pattern=None):
    """Filter data by keyword or regex pattern."""
    if not keyword and not regex_pattern:
        return data
    
    filtered_data = {}

    for key, value in data.items():
        if isinstance(value, list):
            if keyword:
                filtered_items = [
                    item for item in value 
                    if keyword.lower() in str(item).lower()
                ]
            else: 
                try:
                    pattern = re.compile(regex_pattern)
                    filtered_items = [
                        item for item in value
                        if pattern.search(str(item))
                    ]
                except re.error:
                    filtered_items = value
            
            if filtered_items:
                filtered_data[key] = filtered_items
        elif isinstance(value, dict):
            filtered_dict = filter_data(value, keyword, regex_pattern)
            if filtered_dict:
                filtered_data[key] = filtered_dict
        elif keyword and keyword.lower() in str(value).lower():
            filtered_data[key] = value
        elif regex_pattern:
            try:
                pattern = re.compile(regex_pattern)
                if pattern.search(str(value)):
                    filtered_data[key] = value
            except re.error:
                if key in data:
                    filtered_data[key] = value 
    return filtered_data

def process_data(data):
    """Process data by removing duplicates and sorting."""
    processed_data = {}
   
    for key, value in data.items():
        if isinstance(value, list):
            unique_items = list(set(value)) if all(isinstance(item, str) for item in value) else value
            
            if key == "emails":
                processed_data[key] = sorted(unique_items, key=lambda x: x.lower())
            elif key == "phones":
                processed_data[key] = sorted(unique_items)
            elif key == "links":
                processed_data[key] = sorted(unique_items)
            else:
                processed_data[key] = unique_items
        else:
            processed_data[key] = value
    
    return processed_data


def live_preview_mode(url, country="US"):
    """Show scraping results as they're being extracted."""
    data_queue = queue.Queue()
    
    def scrape_thread():
        html = fetch_html(url)
        if not html:
            data_queue.put({"error": "Failed to fetch HTML"})
            return
            
        data_queue.put({"status": "Extracting links..."})
        links = extract_links(html)
        data_queue.put({"links": links})
        
        data_queue.put({"status": "Extracting emails..."})
        emails = extract_emails(html)
        data_queue.put({"emails": emails})
        
        data_queue.put({"status": "Extracting social links..."})
        social = extract_social_links(html)
        data_queue.put({"social": social})
        
        data_queue.put({"status": "Extracting author names..."})
        authors = extract_author_names(html)
        data_queue.put({"authors": authors})
        
        data_queue.put({"status": "Extracting phone numbers..."})
        phones = extract_phone_numbers(html, country)
        data_queue.put({"phones": phones})
        
        data_queue.put({"status": "Extracting images..."})
        images = extract_images(html, download=DOWNLOAD_IMAGES)
        data_queue.put({"images": images})
        
        data_queue.put({"status": "Extracting metadata..."})
        metadata = extract_metadata(html)
        data_queue.put({"metadata": metadata})
        
        data_queue.put({"status": "Extracting documents..."})
        documents = extract_document_links(html)
        data_queue.put({"documents": documents})

        data_queue.put({"status": "Extracting tables..."})
        tables = extract_tables(html)
        data_queue.put({"tables": tables})
        data_queue.put({"status": "Done"})

    thread = threading.Thread(target=scrape_thread)
    thread.daemon = True
    thread.start()
    
    collected_data = {}

    while True:
        try:
            data = data_queue.get(timeout=0.1)

            if "status" in data:
                print(f"\r{data['status']}", end="", flush=True)
            elif "error" in data:
                print(f"\nError: {data['error']}")
                break
            else:
                for key, value in data.items():
                    collected_data[key] = value

                print("\r" + " " * 80, end="\r")
                print_to_terminal(collected_data)

                if data.get("status") == "Done":
                    break
        except queue.Empty:
            if not thread.is_alive():
                break

    return collected_data

def main():
    """Main entry point for the web scraping tool"""
    global DOWNLOAD_IMAGES

    parser = argparse.ArgumentParser(description="Web Scraping Tool")

    url_group = parser.add_mutually_exclusive_group(required=True)
    url_group.add_argument("--url", help="URL to scrape")
    url_group.add_argument("--urls", nargs='+', help="Multiple URLs to scrape in parallel")

    parser.add_argument("--output", choices=["terminal", "file"], default="terminal", help="Output mode")
    parser.add_argument("--format", choices=["txt", "json", "csv", "md", "xlsx", "sqlite"], default="txt", help="File format if saving to file")
    parser.add_argument("--filename", default="output.txt", help="Filename for scraped data")
    parser.add_argument("--country", default="US", help="Country code (e.g., PL, US, DE) for phone number parsing")
    parser.add_argument("--depth", type=int, default=1, help="Depth for recursive scraping")
    parser.add_argument("--recursive", action="store_true", help="Enable recursive scraping")
    parser.add_argument("--parallel", action="store_true", help="Enable parallel scraping")
    parser.add_argument("--max-workers", type=int, default=5, help="Maximum number of workers for parallel scraping")
    parser.add_argument("--schedule", type=int, help="Schedule scraping every x hours")
    parser.add_argument("--schedule-output", default="scheduled_output.json", help="Output file for scheduled scraping")
    parser.add_argument("--filter-keyword", help="Filter results by keyword")
    parser.add_argument("--filter-regex", help="Filter results by regex pattern")
    parser.add_argument("--process", action="store_true", help="Process data (remove duplicates and sort)")
    parser.add_argument("--download-images", action="store_true", help="Download images locally")
    parser.add_argument("--live-preview", action="store_true", help="Enable live preview mode")

    args = parser.parse_args()
    DOWNLOAD_IMAGES = args.download_images

    format_extensions = {
        "txt" : ".txt",
        "json" : ".json",
        "csv" : ".csv",
        "md" : ".md",
        "xlsx" : ".xlsx",
        "sqlite" : ".sqlite",
    }

    if args.output == "file":
        base_name, current_ext = os.path.splitext(args.filename)
        expected_ext = format_extensions.get(args.format, "")

        if current_ext.lower() != expected_ext.lower():
            args.filename = base_name + expected_ext
            print(f"[I] Updated filename: {args.filename}")

    if args.schedule: 
        if args.urls: 
            print("Error: Scheduled scraping only works with a single URL")
            return
        schedule_scraping(args.url, args.schedule, args.schedule_output, args.country)
        return
    
    if args.live_preview:
        if args.urls:
            print("Error: Live preview only works with a single URL")
            return
        data = live_preview_mode(args.url, args.country)

    elif args.parallel and args.urls:
        data = scrape_parallel(args.urls, args.country, args.max_workers)

    elif args.recursive:
        if args.urls:
            print("Error: Recursive scraping only works with a single URL")
            return
        data = scrape_recursive(args.url, depth=1, max_depth=args.depth, country=args.country)
    elif args.url:
        html = fetch_html(args.url)
        if not html:
            return
        
        data = {
            "links": extract_links(html),
            "emails": extract_emails(html), 
            "social": extract_social_links(html),
            "author": extract_author_names(html), 
            "phones": extract_phone_numbers(html, args.country), 
            "images": extract_images(html, download=DOWNLOAD_IMAGES), 
            "metadata": extract_metadata(html), 
            "documents": extract_document_links(html), 
            "tables": extract_tables(html)
        }
    
    if args.filter_keyword or args.filter_regex: 
        data =filter_data(data, args.filter_keyword, args.filter_regex)

    if args.process: 
        data = process_data(data)

    if args.output == "terminal":
        print_to_terminal(data)
    else:
        save_to_file(data, args.filename, args.format)
        print(f"Data saved to: {args.filename}")

if __name__ == "__main__":
    main()