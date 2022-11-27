#! python36
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

from imageScraper import scrape_images

URL = "https://www.google.co.in"
chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_argument('--incognito')
chromeOptions.add_argument('--headless')

driver = webdriver.Chrome(executable_path="C:\chromedriver.exe", options = chromeOptions)
driver.maximize_window()

def scrape_text(query):
    driver.get(URL)
    time.sleep(0.25)
    driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys(query)
    time.sleep(0.25)
    driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys(Keys.ENTER)
    time.sleep(0.5)

    page_source = driver.page_source.encode('utf8')
    soup = BeautifulSoup(page_source, 'lxml')

    related_list = []
    related = soup.find_all(class_ = 'iDjcJe IX9Lgd wwB5gf',limit=3)
    related_list.append('Related searches👇')
    for x in related:
        related_list.append(x.get_text().strip())

    try:
        text1 = soup.find_all(class_ = 'bjV81b')
        text2 = soup.find_all(class_ = 'JDfRZb')
        if len(text1) == 0 or len(text2) == 0:
            raise Exception('List is empty')
        for a, b in zip(text1, text2):
            return [[a.get_text(), b.get_text()], related_list]
    except:
        try: # scraping all the lists from "People also ask"
            lists = []
            data = soup.find_all(class_ = 'TrT0Xe', limit=6)
            link = soup.find_all(class_ = 'truncation-information', limit=1)

            if len(data) == 0 or len(link) == 0:
                raise Exception('List is empty')

            for x in data:
                lists.append("▸ {}".format(x.get_text().strip()[:-1]))
            if len(link) != 0:
                lists.append("*For more* information, see {}".format(link[0].get("href")))
            return [lists, related_list]
        except:
            try: # scraping is done from "People also ask"
                img_url = scrape_images(query) # scrape related image
                data = soup.find_all(class_ = 'hgKElc', limit=1)
                for x in data:
                    return [img_url, x.get_text().strip(), related_list]
            except:
                return "Sorry couldn't find anything. I am still learning" 

# res = scrape_text('what is kmp algorithm')
# search = res[-1]
# for each in search: 
#         print(each)
# if type(res) == list:
#     for each in res: 
#         print(each)
# else:
#     print(res)
