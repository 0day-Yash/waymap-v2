# Copyright (c) 2024 waymap developers 
# See the file 'LICENSE' for copying permission.

import random
import requests
import re
import os
from termcolor import colored
from xml.etree import ElementTree as ET
from concurrent.futures import ThreadPoolExecutor, as_completed

data_dir = os.path.join(os.getcwd(), 'data')

def load_dbms_errors(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    dbms_errors = {}
    for dbms in root.findall('dbms'):
        dbms_name = dbms.attrib['value']
        errors = [error.attrib['regexp'] for error in dbms.findall('error')]
        dbms_errors[dbms_name] = errors
    return dbms_errors

def detect_dbms(response_content, dbms_errors):
    for dbms_name, patterns in dbms_errors.items():
        for pattern in patterns:
            if re.search(pattern, response_content, re.IGNORECASE):
                return dbms_name
    return None

def detect_web_tech(headers):
    if 'x-powered-by' in headers:
        return headers['x-powered-by']
    elif 'server' in headers:
        return headers['server']
    return 'Unknown'

def test_payload(url, payload, user_agent, dbms_errors):
    headers = {'User-Agent': user_agent}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response_content = response.text

        dbms = detect_dbms(response_content, dbms_errors)
        if dbms:
            return {'vulnerable': True, 'dbms': dbms, 'response': response_content, 'headers': response.headers}

    except requests.RequestException as e:
        print(colored(f"[×] Error testing payload on {url}: {e}", 'red'))

    return {'vulnerable': False}

def perform_sqli_scan(crawled_urls, sql_payloads, user_agents):
    dbms_errors = load_dbms_errors(os.path.join(data_dir, 'errors.xml'))
    detected_tech = None  
    user_decision = None  

    try:
        for url in crawled_urls:
            print(colored(f"\n[•] Testing URL: {url}", 'yellow'))

            payloads_to_test = random.sample(sql_payloads, 10)
            found_vulnerability = False 

            with ThreadPoolExecutor(max_workers=5) as executor:
                futures = {
                    executor.submit(test_payload, f"{url}{payload}", payload, random.choice(user_agents), dbms_errors): payload 
                    for payload in payloads_to_test
                }

                for future in as_completed(futures):
                    result = future.result()
                    if result['vulnerable']:
                        found_vulnerability = True
                        if not detected_tech:
                            detected_tech = detect_web_tech(result['headers'])
                            print(colored(f"[•] Web Technology: {detected_tech or 'Unknown'}", 'magenta'))

                        print(colored(f"[★] Vulnerable URL found: {url}{futures[future]}", 'white', attrs=['bold']))
                        print(colored(f"[•] Vulnerable Parameter: {url.split('?')[1] if '?' in url else 'N/A'}", 'green'))
                        print(colored(f"[•] Payload: {futures[future]}", 'green'))
                        print(colored(f"[•] Backend DBMS: {result['dbms']}", 'blue'))

                        if user_decision is None:
                            user_input = input(colored("\n[?] Vulnerable URL found. Do you want to continue testing other URLs? (y/n): ", 'yellow')).strip().lower()
                            if user_input == 'n':
                                print(colored("[•] Stopping further scans as per user's decision.", 'red'))
                                return  
                            user_decision = (user_input == 'y')  

                        break  

                if not found_vulnerability:
                    print(colored(f"[×] No vulnerabilities found on: {url}", 'red'))

    except KeyboardInterrupt:
        print(colored("\n[!] Scan interrupted by user. Exiting cleanly...", 'red'))
