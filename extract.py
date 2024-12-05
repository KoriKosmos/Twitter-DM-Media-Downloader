import json
import os
import subprocess
import time

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# Path to Chrome executable
chrome_path = "/path/to/chrome.exe"

# Path to ChromeDriver executable
chromedriver_path = "/path/to/chromedriver.exe"

# Configure Selenium for Chrome with performance logging enabled
options = Options()
options.binary_location = chrome_path

# Enable performance logging
options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

service = Service(chromedriver_path)

driver = webdriver.Chrome(service=service, options=options)


# Load Twitter with saved cookies
def load_cookies_from_json(cookies_file):
    driver.get("https://twitter.com")
    try:
        with open(cookies_file, "r") as file:
            cookies = json.load(file)
            for cookie in cookies:
                driver.add_cookie(cookie)
        print("Cookies loaded successfully!")
    except Exception as e:
        print(f"Error loading cookies: {e}")
        return False
    return True


# Convert Selenium cookies to requests format
def get_session_cookies():
    selenium_cookies = driver.get_cookies()
    session_cookies = {cookie["name"]: cookie["value"] for cookie in selenium_cookies}
    return session_cookies


# Function to clean up and download media
# Function to clean up and download media with full headers
def download_media(url, media_type, session_cookies):
    # Define folders for images and videos
    folder_mapping = {
        "image": "IMG",
        "video": "VID"
    }
    download_folder = folder_mapping.get(media_type, "downloads")

    # Ensure the folder exists
    os.makedirs(download_folder, exist_ok=True)

    # Clean up the URL (remove specific suffixes like ':small', ':large', ':medium')
    if any(suffix in url for suffix in [":small", ":large", ":medium"]):
        cleaned_url = url.rsplit(":", 1)[0]  # Remove the last ':suffix'
    else:
        cleaned_url = url  # Retain the original URL

    try:
        # Capture headers from Selenium's network requests
        headers = {
            "User-Agent": driver.execute_script("return navigator.userAgent;"),  # Get browser's User-Agent
            "Cookie": "; ".join([f"{k}={v}" for k, v in session_cookies.items()]),  # Include cookies
            "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",  # Generic image headers
            "Referer": "https://x.com/",  # Include referer
            "Connection": "keep-alive",
        }

        if media_type == "image":
            # Debugging: Print URL and headers
            print(f"Attempting to download: {cleaned_url}")
            print(f"Headers: {headers}")

            response = requests.get(cleaned_url, headers=headers, stream=True)
            response.raise_for_status()

            # Extract file name from URL
            filename = os.path.join(download_folder, cleaned_url.split("/")[-1].split("?")[0])
            with open(filename, "wb") as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f"Downloaded to IMG: {filename}")
        elif media_type == "video":
            # Debugging: Print URL and headers
            print(f"Attempting to download and convert: {cleaned_url}")
            print(f"Headers: {headers}")

            # Convert .m3u8 to .mp4 using FFmpeg
            output_filename = os.path.join(download_folder,
                                           f"{cleaned_url.split('/')[-1].split('?')[0].split('.')[0]}.mp4")
            command = [
                "ffmpeg",
                "-headers", f"Cookie: {'; '.join([f'{k}={v}' for k, v in session_cookies.items()])}",
                "-i", cleaned_url,  # Input URL
                "-c", "copy",  # Copy codec (fast conversion)
                output_filename
            ]
            subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(f"Converted to MP4: {output_filename}")
    except requests.exceptions.HTTPError as e:
        print(f"Failed to process {cleaned_url}: {e}")
        print(f"Response: {response.content if 'response' in locals() else 'No response available'}")
    except Exception as e:
        print(f"An unexpected error occurred while processing {cleaned_url}: {e}")


# Continuously extract and download URLs live
def extract_and_download_urls_live():
    seen_urls = set()
    session_cookies = get_session_cookies()
    print("Monitoring network traffic for specific URLs. Scroll through your messages.")

    try:
        while True:
            # Get performance logs
            logs = driver.get_log("performance")

            for log in logs:
                try:
                    message = json.loads(log["message"])
                    params = message["message"]["params"]
                    if "request" in params:
                        url = params["request"]["url"]

                        # Capture full stream `.m3u8` URLs ending with `variant_version=1&tag` as videos
                        if "variant_version=1&tag" in url and ".m3u8" in url:
                            if url not in seen_urls:
                                seen_urls.add(url)
                                print(f"Captured Full Stream URL: {url}")
                                download_media(url, "video", session_cookies)

                        # Capture `.jpg`, `.png`, and `.gif` as images, excluding "preview" and "profile_images"
                        elif any(ext in url for ext in [".jpg", ".png", ".gif"]) and not any(
                                exclude in url for exclude in ["preview", "profile_images"]):
                            if url not in seen_urls:
                                seen_urls.add(url)
                                print(f"Captured Image/GIF URL: {url}")
                                download_media(url, "image", session_cookies)

                except (KeyError, json.JSONDecodeError):
                    continue

            # Wait a bit before checking logs again
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopped live URL extraction.")
        return seen_urls


# Main Execution
if __name__ == "__main__":
    try:
        # Login using cookies
        cookies_file = "twitter_cookies.json"  # Use the new JSON cookie file
        if load_cookies_from_json(cookies_file):
            # Navigate directly to the specific DM
            dm_url = "https://x.com/messages"
            driver.get(dm_url)
            print(f"Opened DM: {dm_url}")

            # Wait for user input to start URL extraction
            input(
                "Press Enter to start extracting and downloading URLs after you have navigated to the desired location...")

            # Extract and download URLs live
            extracted_urls = extract_and_download_urls_live()

            # Final save of all unique URLs
            with open("extracted_urls.txt", "w") as file:
                for url in extracted_urls:
                    file.write(url + "\n")
            print(f"Extracted URLs saved to 'extracted_urls.txt'.")
        else:
            print("Failed to load cookies. Please check the cookie file.")

    except KeyboardInterrupt:
        print("\nStopped by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()
        print("Browser closed. Goodbye!")

# %%
