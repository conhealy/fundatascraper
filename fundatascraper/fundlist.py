"""
Module to scrape list of mutual funds on fundata.ca along with urls
where details of funds can be found.
"""
import time
from random import randint
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def get_fund_list():
    """
    Method to get list of funds.
    returns:
    """
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    driver.get('http://idata.fundata.com/mutualfunds/Search.aspx')
    current_page = 1

    href_list = []

    while True:
        soup = BeautifulSoup(driver.page_source)

        fund_links = soup.findAll("a", {"title": "Click here to view summary" \
                " information about this mutual fund"})
        for link in fund_links:
            print(link.text)
            href_list.append(link['href'])

        current_page += 1
        print("############ Page "  + str(current_page) + "##############")

        time.sleep(randint(1, 5))
        try:
            driver.find_element_by_link_text(str(current_page)).click()
        except NoSuchElementException:
            break

        wait = WebDriverWait(driver, 30)
        wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//span[text()='" + str(current_page) + "']")
            )
        )

    return href_list
