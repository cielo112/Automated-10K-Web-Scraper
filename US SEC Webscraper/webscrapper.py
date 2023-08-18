import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from getpass import getpass
from time import sleep
import csv

import pandas as pd


def web_scrapper(cik):
    '''This function automtically gathers the 10-K report of a given CIK'''

    #Open the webpage and maximize window
    options = Options()
    options.add_experimental_option('detach', True)

    driver = webdriver.Chrome(options=options)

    driver.get("https://www.sec.gov/edgar/search/#")
    driver.maximize_window()


    def search_file(cik):
        #Fill in the details for the company and report needed

        search_options = driver.find_element(By.XPATH, './/a[@id="show-full-search-form"]')
        search_options.click()

        #Name of the document
        document_name = 'Annual Report'
        document_box = driver.find_element(By.XPATH, './/input[@id= "keywords"]')
        document_box.send_keys(document_name)

        #CIK of the company
        cik_box = driver.find_element(By.XPATH, './/input[@id="entity-full-form"]')
        cik_box.send_keys(cik)

        #Filling Category
        filling_button = driver.find_element(By.XPATH, './/button[@id="category-select"]')
        filling_button.click()
        reports_option = driver.find_element(By.XPATH, './/li[contains(., "All annual")]')
        reports_option.click()
        sleep(3)

        #Initiate Search
        search_button = driver.find_element(By.XPATH, './/button[@id="search"]')
        search_button.send_keys(Keys.ENTER)
    try:
        search_file(cik)
    except NoSuchElementException:
        return

    def open_browser():
        try:
            #Get the contents form the table returned by the search
            files = driver.find_elements(By.XPATH, './/a[@href][contains(., "10-K")]')
            latest_report = files[1]
            latest_report.click()
            
        except IndexError:
            return
        #Open a new window to the file directory
        open_file = driver.find_element(By.XPATH, './/button[contains(., "Open filing")]')
        open_file.click()
        driver.switch_to.window(driver.window_handles[-1])
    try:
        open_browser()
    except NoSuchElementException:
        return

    def open_file():
        #Get file from the directory
        file = driver.find_element(By.XPATH, './/div[@id="PageTitle"]').text
        file = driver.find_element(By.XPATH, './/table[@class="tableFile"]/tbody/tr[2]/td[3]/a[@href]')
        file.click()

        sleep(1)    
        content = driver.find_element(By.XPATH, './/div[@class="reboot main-container"]/div[@id="dynamic-xbrl-form"]').text
        return content
    
    try:
        content = open_file()
    except NoSuchElementException:
        return
    
    return content

