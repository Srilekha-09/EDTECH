from re import L
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import json
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from helper import *
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
chrome_options.add_argument(f'user-agent={user_agent}')

def intialize_driver(chrome_options,start_url):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)
    driver.implicitly_wait(10)
    driver.get(start_url)
    return driver


def job_seek(info):

    job = info[0]
    location = info[1]
    job_type = info[2]
    q = f"{job} in {location}"

    start_url = f"https://www.google.com/search?q={q}&ibp=htl;jobs#htivrt=jobs&htilrad=-1.0&htichips=employment_type:{job_type}"

    driver = intialize_driver(chrome_options=chrome_options,start_url=start_url)

    list_elements = driver.find_elements(By.CLASS_NAME,"gws-plugins-horizon-jobs__tl-lif")

    for i in list_elements:
        try:
            i.click()
        except:
            pass
    
    link = driver.find_elements(By.XPATH,"""//span/a[@class='pMhGee Co68jc j0vryd']""")
 
    jobs = driver.find_elements(By.TAG_NAME,"ul")
    try:
        soup = BeautifulSoup(jobs[0].get_attribute('innerHTML'),'html.parser')

        job_name = soup.find_all("div",{"class":"BjJfJf PUpOsf"})
        company_name = soup.find_all("div",{"class":"vNEEBe"})
        location = soup.find_all("div",{"class":"Qk80Jf"}) 


        job_opening = []
        job_opening.append('job')

        for i in range(0 , len(job_name)):
            data = {}
            data["job_name"] = job_name[i].get_text()
            data["company_name"] = company_name[i].get_text()
            data["link"] = link[i].get_attribute('href')
            if i %2 == 0:
                data["location"] = location[i].get_text()
            else :
                data["location"] = location[i+1].get_text()
            job_opening.append(data)

        return job_opening
    except IndexError:
        return "Sorry, did not find any jobs for you"

# RES = job_seek(['Mlops','Karnataka','FULLTIME'])
# print(RES)
'''
CONTRACTOR
PARTTIME
FULLTIME
INTERNSHIP
'''
