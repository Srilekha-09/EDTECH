from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

DRIVER_PATH = 'C:\chromedriver.exe'
chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_argument('--incognito')
chromeOptions.add_argument('--headless')
driver = webdriver.Chrome(executable_path = DRIVER_PATH, options = chromeOptions)
driver.get("https://www.google.com")

def get_pdf_links(x):
	if x is not None:
		return x[-4:] == ".pdf"
	return False

def pdf_search(site):

    search_bar = driver.find_element(by=By.XPATH, value="//input[@maxlength=\"2048\"]")
    search_expr = "{} filetype:pdf "
    search_bar.send_keys(search_expr.format(site))
    search_bar.send_keys(Keys.RETURN)

    pdf_links = []

    try:
       links = [x.get_attribute("href") for x in driver.find_elements(by=By.TAG_NAME, value="a")]
       pdf_links += list(filter(get_pdf_links, links))
       time.sleep(0.25)
       driver.find_element(by=By.ID, value="pnnext").click()
       pdf_links.insert(0, 'pdf')
       return pdf_links

    except Exception as e:
        pass

# link = pdf_search('dsce.edu.in')
# for _ in link:
#     print(_)
