from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Define the path to chrome driver
DRIVER_PATH = 'C:\chromedriver.exe'
chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_argument('--incognito')
chromeOptions.add_argument('--headless')
wd = webdriver.Chrome(executable_path = DRIVER_PATH, options = chromeOptions)
# This searches images from google.com
wd.get('https://google.com')

def _build_query(query:str):
    return f"https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={query}&oq={query}&gs_l=img"

def _get_info(query):
        # image_urls = set()

        wd.get(_build_query(query))

        # img.Q4LuWd is the google tumbnail selector
        thumbnails = wd.find_elements(by=By.CSS_SELECTOR, value="img.Q4LuWd")

        for img in thumbnails[0:10]:
            # We need to click every thumbnail so we can get the full image.
            try:
                img.click()
            except Exception:
                print('ERROR: Cannot click on the image.')
                continue

            images = wd.find_elements(by=By.CSS_SELECTOR, value='img.n3VNCb')
            time.sleep(0.2)

            for image in images:
                if image.get_attribute('src') and 'http' in image.get_attribute('src'):
                    # image_urls.add(image.get_attribute('src'))
                    image_url = image.get_attribute('src')
                    if image_url == None:
                        continue
                    else:
                        return image_url


def scrape_images(query):
    image_info = _get_info(query)
    return image_info

# url = scrape_images('what is depth first search')
# print(url)
