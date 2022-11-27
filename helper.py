from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from urllib.parse import urlparse
import logging
import json
# from dotenv import load_dotenv
from pymongo import MongoClient




def check_exists_by_xpath_text(driver,xpath):
    try:
        value = driver.find_element(By.XPATH,xpath)
    except NoSuchElementException:
        logging.debug(f'XPATH NOT FOUND ---- || {xpath}')
        return "null"
    return value.text

def check_exists_by_xpath_src(driver,xpath):
    try:
        value = driver.find_element(By.XPATH,xpath)
    except NoSuchElementException:
        logging.debug(f'XPATH NOT FOUND ---- || {xpath}')
        return "null"
    return value.get_attribute('src')

def check_exists_by_xpath_href(driver,xpath:str,required_link:str=None):
    try:
       link = required_link
       value = driver.find_element(By.XPATH,xpath)
    except NoSuchElementException:
        logging.debug(f'XPATH NOT FOUND ---- || {xpath}')
        return "null"
    # if link == "registration_link" and urlparse(value.get_attribute('href')).netloc != "www.naukri.com" :
    #     return value.get_attribute('href')
    # else:
    return value.get_attribute('href')

def check_exists_by_classname(driver,xpath):
    try:
        value = driver.find_element(By.CLASS_NAME,xpath)
    except NoSuchElementException:
        return "null"
    return value

def find_registration_link(driver,data):
    a = data["job_slug"]
    b = data["company_name"]
    driver.get("https://www.google.com/")
    driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys(f"""{a} "{b}" """)
    driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys(Keys.ENTER)
                
            
    value = check_exists_by_xpath_href(driver,'//*[@id="rso"]/div[1]/div/div/div[1]/div/a',"registration_link")
            # print("REGISTRATION LINK: {}".format(data["registration_link"]))
    driver.back()
    driver.back()
    driver.implicitly_wait(10)
    return value

def save(data):
    f = open('data.json')
    final_data = json.load(f)
    final_data.append(data)
    json_object = json.dumps(final_data, indent=4, ensure_ascii=False)
    with open("data.json", "w", encoding='utf8') as outfile:
        outfile.write(json_object)

def get_database(collection_name:str):
    CONNECTION_STRING = "mongodb+srv://samrath:samrath@pragati.oeap8sk.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(CONNECTION_STRING)
    db = client['pragati']
    return db[f'{collection_name}']
  
def save_db(data:json,collection_name:str):
   dbname = get_database(f'{collection_name}')
   dbname.insert_one(data)

def intialize_driver(chrome_options,link:str):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)
    driver.implicitly_wait(10)
    start_url = link
    driver.get(start_url)
    return driver

def trigger_first_scrape(driver,data,job_list,i,j):
    
    data["registration_link"] = find_registration_link(driver,data)
               
    data["company_logo"] = check_exists_by_xpath_src(driver,'/html/body/div[1]/main/div[2]/div[2]/section[1]/div[1]/a/img')

    data["job_duration"] = check_exists_by_xpath_text(driver,'/html/body/div[1]/main/div[2]/div[2]/section[1]/div[1]/div[2]/div[1]/span')

    data["job_stipend"] = check_exists_by_xpath_text(driver,'/html/body/div[1]/main/div[2]/div[2]/section[1]/div[1]/div[2]/div[2]/span').replace('₹','')

    data["job_location"] = (check_exists_by_xpath_text(driver,'/html/body/div[1]/main/div[2]/div[2]/section[1]/div[1]/div[2]/div[3]/span')).split(",")

    data["job_description"] = check_exists_by_xpath_text(driver,'/html/body/div[1]/main/div[2]/div[2]/section[2]/div[1]')

    data["job_role"] = check_exists_by_xpath_text(driver,'//*[@id="root"]/main/div[2]/div[2]/section[2]/div[2]/div[1]/span/a')

    data["industry_type"] = check_exists_by_xpath_text(driver,'//*[@id="root"]/main/div[2]/div[2]/section[2]/div[2]/div[2]/span/a')

    data["functional_area"] = check_exists_by_xpath_text(driver,'//*[@id="root"]/main/div[2]/div[2]/section[2]/div[2]/div[3]/span/a')

    data["employment_type"] = check_exists_by_xpath_text(driver,'//*[@id="root"]/main/div[2]/div[2]/section[2]/div[2]/div[4]/span/span')

    data["role_category"] = check_exists_by_xpath_text(driver,'//*[@id="root"]/main/div[2]/div[2]/section[2]/div[2]/div[5]/span/span')

    data["education_qualification"] = check_exists_by_xpath_text(driver,'//*[@id="root"]/main/div[2]/div[2]/section[2]/div[3]')

    data["about_company"] = check_exists_by_xpath_text(driver,'/html/body/div[1]/main/div[2]/div[2]/section[3]/div[1]')
            
    data["company_address"] = check_exists_by_xpath_text(driver,'/html/body/div[1]/main/div[2]/div[2]/section[3]/div[3]/span')

    print(f"{job_list.upper()} || {j} CYCLE || {i} DONE")
    return data

def trigger_second_scrape(driver,data,job_list,i,j):

    data["registration_link"] = find_registration_link(driver,data)
               
    data["company_logo"] = check_exists_by_xpath_src(driver,'/html/body/div[1]/main/div[2]/div[2]/section[1]/div[1]/a/img')

    data["job_duration"] = check_exists_by_xpath_text(driver,'/html/body/div[1]/main/div[2]/div[2]/section[1]/div[1]/div[2]/div[1]/span')

    data["job_stipend"] = check_exists_by_xpath_text(driver,'/html/body/div[1]/main/div[2]/div[2]/section[1]/div[1]/div[2]/div[2]/span')

    data["job_location"] = (check_exists_by_xpath_text(driver,'/html/body/div[1]/main/div[2]/div[2]/section[1]/div[1]/div[2]/div[3]/span')).split(",")

    data["job_description"] = check_exists_by_xpath_text(driver,'/html/body/div[1]/main/div[2]/div[2]/section[2]/div[1]')

    data["job_role"] = check_exists_by_xpath_text(driver,'//*[@id="root"]/main/div[2]/div[2]/section[2]/div[2]/div[1]/span/a')

    data["industry_type"] = check_exists_by_xpath_text(driver,'//*[@id="root"]/main/div[2]/div[2]/section[2]/div[2]/div[2]/span/a')

    data["functional_area"] = check_exists_by_xpath_text(driver,'//*[@id="root"]/main/div[2]/div[2]/section[2]/div[2]/div[3]/span/a')

    data["employment_type"] = check_exists_by_xpath_text(driver,'//*[@id="root"]/main/div[2]/div[2]/section[2]/div[2]/div[4]/span/span')

    data["role_category"] = check_exists_by_xpath_text(driver,'//*[@id="root"]/main/div[2]/div[2]/section[2]/div[2]/div[5]/span/span')

    data["education_qualification"] = check_exists_by_xpath_text(driver,'//*[@id="root"]/main/div[2]/div[2]/section[2]/div[3]')

    data["about_company"] = check_exists_by_xpath_text(driver,'//*[@id="root"]/main/div[2]/div[2]/section[4]/div[1]')
            
    data["company_address"] = check_exists_by_xpath_text(driver,'//*[@id="root"]/main/div[2]/div[2]/section[4]/div[3]')

    print(f"{job_list.upper()} || {j} CYCLE || {i} DONE")
    return data
