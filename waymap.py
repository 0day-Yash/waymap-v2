import os
import argparse
import requests
from termcolor import colored
from lib.crawler import run_crawler
from lib.injector import inject_payloads, load_payloads, load_errors_xml
from extras.error_handler import check_internet_connection, check_required_files, check_required_directories, handle_error

# Directories for data and session
data_dir = os.path.join(os.getcwd(), 'data')
session_dir = os.path.join(os.getcwd(), 'session')

# Version and banner details
WAYMAP_VERSION = "1.0.3"  # Update version to 1.0.3
AUTHOR = "Trix Cyrus"
COPYRIGHT = "Copyright © 2024 Trixsec Org"

def check_for_updates():
    # Load current version from VERSION file
    with open('VERSION', 'r') as version_file:
        current_version = version_file.read().strip()

    # URL for the latest version in the repository
    latest_version_url = 'https://raw.githubusercontent.com/TrixSec/waymap/refs/heads/main/VERSION'

    try:
        response = requests.get(latest_version_url)
        response.raise_for_status()
        latest_version = response.text.strip()

        if current_version != latest_version:
            print(colored(f"[•] New version available: {latest_version}. Updating...", 'yellow'))
            # Logic to update the Waymap tool (e.g., using git)
            os.system('git pull')  # Ensure you're in the correct directory
            with open('VERSION', 'w') as version_file:
                version_file.write(latest_version)  # Update local VERSION file
        else:
            print(colored(f"[•] You are using the latest version: {current_version}.", 'green'))

    except requests.RequestException as e:
        print(colored(f"[×] Error checking for updates: {e}", 'red'))

# Function to print the banner
def print_banner():
    banner = r"""
     __    __
    / / /\ \ \  __ _  _   _  _ __ ___    __ _  _ __
    \ \/  \/ / / _ || | | || '_  _ \  / _ || '_ \
     \  /\  / | (_| || |_| || | | | | || (_| || |_) |
      \/  \/   \__,_| \__, ||_| |_| |_| \__,_|| .__/
                      |___/                   |_|    Fastest And Optimised Web Vulnerability Scanner  v1.0.3
    """
    print(colored(banner, 'cyan'))
    print(colored(f"Waymap Version: {WAYMAP_VERSION}", 'yellow'))
    print(colored(f"Made by {AUTHOR}", 'yellow'))
    print(colored(COPYRIGHT, 'yellow'))
    print("")

# Save the crawled URLs to a file
def save_to_file(domain, urls):
    domain_path = os.path.join(session_dir, domain)
    os.makedirs(domain_path, exist_ok=True)
    crawl_file = os.path.join(domain_path, 'crawl.txt')

    with open(crawl_file, 'w') as f:
        for url in urls:
            f.write(url + '\n')

# Load previously crawled URLs from a file
def load_crawled_urls(domain):
    domain_path = os.path.join(session_dir, domain)
    crawl_file = os.path.join(domain_path, 'crawl.txt')

    if os.path.exists(crawl_file):
        with open(crawl_file, 'r') as f:
            return [url.strip() for url in f.readlines()]
    return None

# Load user-agents
def load_user_agents(file_path):
    with open(file_path, 'r') as f:
        return [line.strip() for line in f.readlines()]

# Main function
def main():
    # Print the banner
    print_banner()

    # Error handling: Check internet connection
    if not check_internet_connection():
        handle_error("No internet connection. Please check your network and try again.")

    # Required files for scanning
    required_files = ['sqlipayload.txt', 'cmdipayload.txt', 'ua.txt', 'errors.xml', 'cmdi.xml']

    # Error handling: Check for missing files in the data directory
    missing_files = check_required_files(data_dir, session_dir, required_files)
    if missing_files:
        handle_error(f"Missing required files: {', '.join(missing_files)}")

    # Error handling: Check for required directories
    required_directories = [data_dir, session_dir]
    missing_dirs = check_required_directories(required_directories)
    if missing_dirs:
        handle_error(f"Missing required directories: {', '.join(missing_dirs)}")

    # Argument parser for crawl depth, scan type, and target
    parser = argparse.ArgumentParser(description="Waymap - Crawler and Scanner")
    parser.add_argument('--crawl', type=int, required=True, help="Crawl depth")
    parser.add_argument('--scan', type=str, required=True, choices=['sql', 'cmdi'], help="Scan type: 'sql' or 'cmdi'")
    parser.add_argument('--target', type=str, required=True, help="Target URL")
    args = parser.parse_args()

    target = args.target
    crawl_depth = args.crawl
    scan_type = args.scan

    # Extract the domain name
    domain = target.split("//")[-1].split("/")[0]

    # Load previously crawled URLs if available for the same domain
    crawled_urls = load_crawled_urls(domain)

    if not crawled_urls:
        # Crawl if no previous data
        print(colored(f"[•] Starting crawling on: {target} with depth {crawl_depth}", 'yellow'))
        crawled_urls = run_crawler(target, crawl_depth)
        save_to_file(domain, crawled_urls)

    # Load payloads and DBMS error messages
    sql_payloads = load_payloads(os.path.join(data_dir, 'sqlipayload.txt'))
    cmdi_payloads = load_payloads(os.path.join(data_dir, 'cmdipayload.txt'))
    dbms_errors = load_errors_xml(os.path.join(data_dir, 'errors.xml'))
    user_agents = load_user_agents(os.path.join(data_dir, 'ua.txt'))

    # Load command injection error messages
    cmdi_errors = load_errors_xml(os.path.join(data_dir, 'cmdi.xml'))

    # Perform scanning based on the type
    try:
        if scan_type == 'sql':
            for url in crawled_urls:
                inject_payloads([url], sql_payloads, dbms_errors, user_agents)

        elif scan_type == 'cmdi':
            for url in crawled_urls:
                inject_payloads([url], cmdi_payloads, cmdi_errors, user_agents)

    except KeyboardInterrupt:
        print(colored("\n[×] Scan interrupted by the user. Exiting...", 'red'))

    # Exit the script
    print(colored("[•] Exiting Waymap.", 'yellow'))
    exit()

if __name__ == "__main__":
    main()
