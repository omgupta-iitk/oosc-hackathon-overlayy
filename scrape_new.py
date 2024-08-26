import os
import requests
import zipfile
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import xml.etree.ElementTree as ET
from collections import Counter
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import xml.etree.ElementTree as ET

import json 
import re
segment_array = []
names = []
title = [] 
def remove_http_https(url):
    return re.sub(r'^https?://', '', url)

# URLs for Chrome and ChromeDriver
CHROME_URL = "https://storage.googleapis.com/chrome-for-testing-public/128.0.6613.84/linux64/chrome-linux64.zip"
CHROMEDRIVER_URL = "https://storage.googleapis.com/chrome-for-testing-public/128.0.6613.84/linux64/chromedriver-linux64.zip"

# Paths for Chrome and ChromeDriver
CHROME_PATH = os.path.join(os.getcwd(), 'chrome-linux64')
CHROMEDRIVER_PATH = os.path.join(os.getcwd(), 'chromedriver-linux64')

def download_and_extract(url, extract_to='.'):
    local_filename = url.split('/')[-1]
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                f.write(chunk)
    with zipfile.ZipFile(local_filename, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    os.remove(local_filename)
    return os.path.join(extract_to, local_filename.replace('.zip', ''))

def setup_chrome():
    # chrome_binary = os.path.join(CHROME_PATH, 'chrome')
    # chromedriver_binary = os.path.join(CHROMEDRIVER_PATH, 'chromedriver')

    # if not os.path.exists(chrome_binary):
    #     print("Chrome not found. Downloading and extracting Chrome...")
    #     download_and_extract(CHROME_URL)
    #     print("Chrome downloaded and extracted.")
    # else:
    #     print("Chrome already installed.")

    # if not os.path.exists(chromedriver_binary):
    #     print("ChromeDriver not found. Downloading and extracting ChromeDriver...")
    #     download_and_extract(CHROMEDRIVER_URL)
    #     print("ChromeDriver downloaded and extracted.")
    # else:
    #     print("ChromeDriver already installed.")

    # # Make sure the binaries are executable
    # os.chmod(chrome_binary, 0o755)
    # os.chmod(chromedriver_binary, 0o755)
    chrome_binary = "jelo"
    chromedriver_binary = "fdgs"

    return chrome_binary, chromedriver_binary

def setup_driver(chrome_binary, chromedriver_binary):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    return driver

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import xml.etree.ElementTree as ET

def get_sitemap_links(driver, sitemap_url):
    print(f"Attempting to fetch sitemap from {sitemap_url}")
    try:
        # Check if it's the /sitemap case
        if sitemap_url.endswith('/sitemap'):
            return scrape_links_from_page(driver, sitemap_url)
        
        # For sitemap.xml, use requests to get the raw content
        response = requests.get(sitemap_url)
        response.raise_for_status()
        
        # Check if the content is XML
        if 'xml' in response.headers.get('Content-Type', ''):
            # Parse the XML content using ElementTree
            root = ET.fromstring(response.content)
            # Define the namespace
            namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
            # Find all URL elements and extract the loc
            links = [elem.text for elem in root.findall('.//ns:loc', namespace)]
        else:
            # If not XML, parse as HTML using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            links = [a['href'] for a in soup.find_all('a', href=True)]
        
        print(f"Found {len(links)} links in sitemap")
        return links
    
    except requests.RequestException as e:
        print(f"Failed to fetch sitemap: {e}")
    except ET.ParseError as e:
        print(f"Failed to parse XML: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    
    # If we reach here, something went wrong. Try to scrape links from the page
    print("Falling back to scraping links from the page")
    return scrape_links_from_page(driver, sitemap_url)

def scrape_links_from_page(driver, url):
    try:
        driver.get(url)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        # Use JavaScript to get all href attributes
        links = driver.execute_script("""
            var links = [];
            var elements = document.getElementsByTagName('a');
            for (var i = 0; i < elements.length; i++) {
                if (elements[i].href) {
                    links.push(elements[i].href);
                }
            }
            return links;
        """)
        
        print(f"Found {len(links)} links on the page")
        return links
    
    except Exception as e:
        print(f"Failed to scrape links from page: {e}")
        return []

def get_links(driver, base_url):
    print(f"\nAttempting to fetch links from {base_url}")
    
    # Try to fetch sitemap.xml
    sitemap_links = get_sitemap_links(driver, urljoin(base_url, "sitemap.xml"))
    if sitemap_links:
        print("Successfully fetched links from sitemap.xml")
        return sitemap_links

    # If sitemap.xml doesn't exist, try sitemap
    sitemap_links = get_sitemap_links(driver, urljoin(base_url, "sitemap"))
    if sitemap_links:
        print("Successfully fetched links from sitemap")
        return sitemap_links

    # If no sitemap is found, scrape links from the homepage
    print("No sitemap found. Scraping links from homepage...")
    return scrape_links_from_page(driver, base_url)


def follow_redirects(driver, url, max_redirects=5):
    for _ in range(max_redirects):
        try:
            driver.get(url)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            if driver.current_url == url:
                return url
            url = driver.current_url
        except Exception as e:
            print(f"Error following redirect: {e}")
            return None
    print(f"Max redirects reached for {url}")
    return None

def scrape_links_from_homepage(driver, url):
    print(f"Attempting to scrape links from homepage: {url}")
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        elements = driver.find_elements(By.TAG_NAME, "a")
        links = [element.get_attribute('href') for element in elements if element.get_attribute('href')]
        
        print(f"Found {len(links)} links on the homepage")
        return links

    except Exception as e:
        print(f"Failed to scrape homepage: {e}")
        return []

def count_path_segments(urls):
    print("\nCounting path segments...")
    path_segments = []
    
    for url in urls:
        print(url)
        if url:
            url = remove_http_https(url)
            parsed_url = urlparse(url)
            path = parsed_url.path.strip('/')
            print(parsed_url)
            print(path)
            if path:
                split_path = path.split('/')
                if len(split_path) > 1:  # Check if there's a second segment
                    first_segment = split_path[1]
                    path_segments.append(first_segment)
    
    counter = Counter(path_segments)
    print(f"Found {len(counter)} unique path segments")
    print("\nTop 5 path segments:")
    for segment, count in counter.most_common(5):
        print(f"{segment}: {count}")
    return counter

def save_text_for_top_segments(base_url, chrome_binary, chromedriver_binary, top_n=5):
    driver = setup_driver(chrome_binary, chromedriver_binary)
    print(f"\nProcessing website: {base_url}")
    
    try:
        links = get_links(driver, base_url)
        
        print("\nAll found links:")
        for link in links:
            print(link)

        segment_counts = count_path_segments(links)
        
        print(f"\nFinding top {top_n} valid segments...")
        valid_segments = []
        for segment, count in segment_counts.most_common():
            print(f"\nChecking segment: {segment} (count: {count})")
            url = urljoin(base_url, segment)
            if check_url_exists(driver, url):
                valid_segments.append(segment)
                print(f"Added '{segment}' to valid segments")
                if len(valid_segments) == top_n:
                    print(f"Found {top_n} valid segments. Stopping search.")
                    break
            else:
                print(f"Skipping '{segment}' as it does not exist")
        
        print(f"\nTop {len(valid_segments)} valid segments:")
        for segment in valid_segments:
            print(segment)

        for segment in valid_segments:
            url = urljoin(base_url, segment)
            text = get_all_text_from_url(driver, url)
            if text:
                filename = f"{segment}_content.txt"
                with open(filename, 'w', encoding='utf-8') as file:
                    file.write(text)
                print(f"Saved content for segment '{segment}' to {filename}")
            else:
                print(f"No content found for segment '{segment}' at {url}")
    
    finally:
        driver.quit()
def check_url_exists(driver, url):
    print(f"Checking if URL exists: {url}")
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        print("URL exists")
        return True
    except Exception as e:
        print(f"Error checking URL: {e}")
        return False

def get_all_text_from_url(driver, url):
    print(f"\nFetching text content from: {url}")
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        for script_or_style in soup(['script', 'style']):
            script_or_style.decompose()
        
        text = soup.get_text(separator=' ', strip=True)
        print(f"Extracted {len(text)} characters of text")
        
        return text
    
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return ""

def save_text_for_top_segments(base_url, chrome_binary, chromedriver_binary, top_n=5):
    driver = setup_driver(chrome_binary, chromedriver_binary)
    print(f"\nProcessing website: {base_url}")
    
    try:
        links = get_links(driver, base_url)
        
        print("\nAll found links:")
        for link in links:
            print(link)

        segment_counts = count_path_segments(links)
        
        print(f"\nFinding top {top_n} valid segments...")
        valid_segments = []
        for segment, count in segment_counts.most_common():
            print(f"\nChecking segment: {segment} (count: {count})")
            url = urljoin(base_url, segment)
            if check_url_exists(driver, url):
                valid_segments.append(segment)
                print(f"Added '{segment}' to valid segments")
                if len(valid_segments) == top_n:
                    print(f"Found {top_n} valid segments. Stopping search.")
                    break
            else:
                print(f"Skipping '{segment}' as it does not exist")
        
        print(f"\nTop {len(valid_segments)} valid segments:")
        for segment in valid_segments:
            print(segment)
            segment_array.append(base_url+'/'+segment)

        for segment in valid_segments:
            url = urljoin(base_url, segment)
            driver.get(url)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            
            # Get the page title
            title.append(driver.title) 
            
            text = get_all_text_from_url(driver, url)
            if text:
                filename = f"{segment}_content.txt"
                names.append(filename)
                with open(filename, 'w', encoding='utf-8') as file:
                    file.write(f"Title: {title}\n\n")  # Write the title at the top of the file
                    file.write(text)
                print(f"Saved content for segment '{segment}' to {filename}")
                print(f"Title: {title}")
            else:
                print(f"No content found for segment '{segment}' at {url}")
    
    finally:
        data = {
        "relevant_links": [
            {
                "url": j,
                "title": i,
            } for i , j in zip(title,segment_array)
        ]
    }

    driver.quit()

    # Update the JSON data with titles

    # Write the updated data to the JSON file
    with open("links.json", "w") as json_file:
        json.dump(data, json_file, indent=4)

    print(f"Updated JSON data has been written to links.json")
base_url = "https://spo.iitk.ac.in"
def begin():
    # base_url = "https://github.com"  # Replace with the target URL
    
    print("Starting web scraping process...")
    try:
        chrome_binary, chromedriver_binary = setup_chrome()
        save_text_for_top_segments(base_url, chrome_binary, chromedriver_binary)
        print("\nWeb scraping process completed.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
    output_file = "output.json"

    # Write the array to a JSON file



    output_file = "segment.txt"

    # Write the array to the text file
    with open(output_file, "w") as file:
        for item in names:
            file.write(item + "\n")

    print(f"Array has been written to {output_file}")

def base_link():
    return base_url
