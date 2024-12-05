import json

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# Path to Chrome executable
chrome_path = "/path/to/chrome.exe"
chromedriver_path = "/path/to/chromedriver.exe"

options = Options()
options.binary_location = chrome_path
service = Service(chromedriver_path)

driver = webdriver.Chrome(service=service, options=options)


# Save cookies after manual login
def save_cookies_as_json():
    driver.get("https://twitter.com/login")
    input("Log in manually and press Enter to save cookies...")
    cookies = driver.get_cookies()
    with open("twitter_cookies.json", "w") as file:
        json.dump(cookies, file)
    print("Cookies saved successfully!")


if __name__ == "__main__":
    try:
        save_cookies_as_json()
    finally:
        driver.quit()

# %%
