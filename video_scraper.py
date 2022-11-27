from selenium import webdriver 
from selenium.webdriver.common.by import By

chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_argument('--incognito')
chromeOptions.add_argument('--headless')

driver = webdriver.Chrome(executable_path="C:\chromedriver.exe", options = chromeOptions)
driver.maximize_window()

def scrape_video(query):

    driver.get("https://www.youtube.com/results?search_query={}".format(query))

    user_data = driver.find_elements(by=By.XPATH, value='//*[@id="video-title"]')
    imgs = driver.find_elements(by=By.XPATH, value='//*[@id="img"]')

    links = []

    for i, (data, img) in enumerate(zip(user_data, imgs)):

        if data.get_attribute('href') != None and data.get_attribute('title') != None:
            # links.append({0: data.get_attribute('href'), 1: data.get_attribute('title'), 2: img.get_attribute('src')})
            links.append('video')
            links.append(data.get_attribute('href'))
            links.append(data.get_attribute('title'))
            break

    return links

# link = scrape_video('Can I get a video on kmp algorithm')
# for _ in link:
#     print(_)
