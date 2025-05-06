import sys
import os
import requests
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor, as_completed

OUTPUT_FILE = "output.txt"

def load_rss_content(source):
    # If it's a URL
    if source.startswith("http://") or source.startswith("https://"):
        try:
            response = requests.get(source, timeout=10)
            response.raise_for_status()
            content = response.text.strip()
            if not content:
                raise ValueError("RSS content from URL is empty.")
            return content
        except Exception as e:
            raise ValueError(f"Failed to load RSS from URL: {e}")
    else:
        # Local file
        if not os.path.exists(source):
            raise FileNotFoundError(f"RSS file '{source}' not found.")
        with open(source, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if not content:
                raise ValueError("RSS file is empty.")
            return content

def parse_links_from_rss(rss_content):
    try:
        root = ET.fromstring(rss_content)
        links = [elem.text for elem in root.findall(".//item/link") if elem.text]
        return links
    except ET.ParseError as e:
        raise ValueError(f"Invalid RSS XML format: {e}")

def fetch_url_content(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return url, response.text
    except Exception as e:
        return url, f"Failed to fetch: {e}"

def write_results(results):
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        for url, content in results:
            f.write(f"\n===== {url} =====\n")
            f.write(content + "\n")

def main():
    if len(sys.argv) < 2:
        print("❌ Usage: python rssFeed.py <rss_file_or_url>")
        return

    rss_source = sys.argv[1]

    try:
        content = load_rss_content(rss_source)
        links = parse_links_from_rss(content)

        if not links:
            print("❌ No <link> entries found in the RSS feed.")
            return

        print(f"✅ Found {len(links)} links. Fetching content in parallel...")

        results = []
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_url = {executor.submit(fetch_url_content, url): url for url in links}
            for future in as_completed(future_to_url):
                results.append(future.result())

        write_results(results)
        print(f"✅ All content written to '{OUTPUT_FILE}'")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
