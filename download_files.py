import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# --- Configuration ---
# Path to your downloaded HTML file
HTML_FILE_PATH = "data/roadworks_page.html"  # <--- MAKE SURE THIS FILENAME MATCHES YOURS

# Base URL of the original page (for resolving relative links, if any)
# This is important if any links in the HTML are relative (e.g., "/downloads/file.xml")
# and need to be joined with the original domain.
BASE_URL = "https://www.data.gov.uk/dataset/5b3267d8-4307-4eef-a9af-3a4c28224694/highways_agency_planned_roadworks"

# Directory to save downloaded XML files
DOWNLOAD_DIR = "data/downloaded_xml_files"
# --- End Configuration ---

def download_xml_files(html_filepath, base_url, download_dir):
    """
    Parses an HTML file, finds links to XML files, and downloads them.
    """
    # Create download directory if it doesn't exist
    os.makedirs(download_dir, exist_ok=True)
    print(f"Downloads will be saved to: {os.path.abspath(download_dir)}")

    try:
        with open(html_filepath, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except FileNotFoundError:
        print(f"Error: HTML file not found at '{html_filepath}'.")
        print("Please make sure the file exists and the HTML_FILE_PATH variable is correct.")
        return
    except Exception as e:
        print(f"Error reading HTML file '{html_filepath}': {e}")
        return

    soup = BeautifulSoup(html_content, 'html.parser')
    xml_links_found = []

    # Find all <a> tags with an href attribute
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        # Check if the link likely points to an XML file
        # We check the end of the href and also if 'xml' is in the link text for robustness
        link_text = a_tag.get_text().lower()
        if href.lower().endswith('.xml') or 'xml' in link_text:
            # Resolve the URL (handles both absolute and relative links)
            # urljoin will correctly handle if href is already an absolute URL
            full_url = urljoin(base_url, href)

            # Further check if the resolved URL seems to be an XML file path
            parsed_full_url = urlparse(full_url)
            if parsed_full_url.path.lower().endswith('.xml'):
                if full_url not in xml_links_found: # Avoid duplicates
                    xml_links_found.append(full_url)
            elif 'xml' in link_text and parsed_full_url.scheme in ['http', 'https']:
                 # If 'xml' was in text but not extension, it might be a landing page for an XML.
                 # For this specific task, we are strict about .xml extension in the URL.
                 # print(f"Skipping link (no .xml extension in URL path): {full_url} (Text: {a_tag.get_text()})")
                 pass


    if not xml_links_found:
        print("No XML download links ending with '.xml' found in the HTML file.")
        return

    print(f"\nFound {len(xml_links_found)} potential XML links. Starting downloads...")

    for i, xml_url in enumerate(xml_links_found):
        # Clean up potential malformed URL like "http:// http://..."
        cleaned_xml_url = xml_url.replace("http:// http://", "http://").replace("https:// https://", "https://")
        if cleaned_xml_url != xml_url:
            print(f"Cleaned malformed URL: {xml_url} -> {cleaned_xml_url}")
        xml_url = cleaned_xml_url

        try:
            # Extract filename from URL
            parsed_url = urlparse(xml_url)
            filename = os.path.basename(parsed_url.path)

            if not filename:
                filename = f"downloaded_file_{i}.xml"
            elif not filename.lower().endswith('.xml'):
                filename += ".xml"

            filepath = os.path.join(download_dir, filename)

            # Check if file already exists
            if os.path.exists(filepath):
                # print(f"File already exists, skipping: {filepath}") # Optional: uncomment if you want to see skipped files
                continue

            print(f"\n[{i+1}/{len(xml_links_found)}] Attempting to download: {xml_url}") # Moved here
            # Make the request
            # Add a user-agent header as some servers might block default Python requests
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(xml_url, stream=True, timeout=30, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)

            # Save the file
            with open(filepath, 'wb') as f_out:
                for chunk in response.iter_content(chunk_size=8192):
                    f_out.write(chunk)
            print(f"Successfully downloaded and saved to: {filepath}")

        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error for {xml_url}: {e}")
        except requests.exceptions.ConnectionError as e:
            print(f"Connection Error for {xml_url}: {e}")
        except requests.exceptions.Timeout as e:
            print(f"Timeout Error for {xml_url}: {e}")
        except requests.exceptions.RequestException as e:
            print(f"Error downloading {xml_url}: {e}")
        except Exception as e:
            print(f"An unexpected error occurred while processing {xml_url}: {e}")

    print(f"\n--- Download process finished. ---")
    print(f"Check the '{os.path.abspath(download_dir)}' directory for downloaded files.")

if __name__ == "__main__":
    # --- IMPORTANT ---
    # 1. Save the attached HTML file from your prompt (or the one you downloaded)
    #    as "roadworks_page.html" in the same directory as this Python script.
    #    Or, change the HTML_FILE_PATH variable at the top of this script.
    # 2. Make sure you have the 'requests' and 'beautifulsoup4' libraries installed:
    #    pip install requests beautifulsoup4
    # ---

    if not os.path.exists(HTML_FILE_PATH):
        print(f"ERROR: The HTML file '{HTML_FILE_PATH}' was not found in the current directory ({os.getcwd()}).")
        print("Please save the HTML file you downloaded to that path, or update the HTML_FILE_PATH variable in the script.")
    else:
        download_xml_files(HTML_FILE_PATH, BASE_URL, DOWNLOAD_DIR)
