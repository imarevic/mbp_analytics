from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import consts
import login_data as ld
import pandas as pd
import json


def run():
    """
    main entry point of the program.
    """
    # global driver object
    driver = create_driver("Chrome")
    # login to page
    driver = login(driver)
    # scrape content of pages with relevant data
    driver = scrape_home_page(driver)
    # process_data

# === driver session object === #
def create_driver(browser_type):
    """
    creates driver object
    args: browser_type (Chrome, Firefox, Safari)
    """
    if browser_type == "Chrome":
        return webdriver.Chrome()
    elif browser_type == "Firefox":
        return webdriver.Firefox()
    elif browser_type == "Safari":
        return webdriver.Safar()

# === log-in === #
def login(driver):

    # login with credentials
    driver.get(consts.login_url)
    driver.find_element_by_id(consts.login_ul)\
        .click()
    driver.find_element_by_id(consts.login_key) \
        .send_keys(consts.user)
    driver.find_element_by_id(consts.pw_key) \
        .send_keys(consts.password)
    driver.find_element_by_class_name("aui-button-input-submit") \
        .click()

    return driver

def get_url(url_ending):

    user = consts.payload[consts.login_key].split('@')[0]
    url = consts.home_base_url + user + consts.variable_url + url_ending
    return url


# === scraping === #
def scrape_home_page(driver):

    # check if target page loaded
    check_page_loaded(driver, 5, "CLASS_NAME", "aui-column-content")
    # initial empty dict for data
    temp_inf = {}
    # first get home page base content
    home_html = driver.page_source
    home_content = BeautifulSoup(home_html, 'html.parser')
    # extract general infos
    info_elems = list(home_content.find_all('div', class_='aui-column-content'))
    for i, elem in enumerate(info_elems):
        if elem.text == ' Verein ':
            temp_inf['info_club'] = info_elems[i+1].text.strip()
        elif elem.text == ' Mannschaften ':
            season_inf = info_elems[i+1].text
            season_split = season_inf.split("  ")
            temp_inf['info_season'] = season_split[0]
            comp_rank_split = season_split[1].split(", ")
            temp_inf['info_competition'] = comp_rank_split[0]
            temp_inf['info_rank'] = comp_rank_split[1]

    # extract friends infos


    return driver

def scrape_profile_page(driver):
    pass
    # get profile summary infos

    # get lk infos

    # get club results infos

# === data processing === #


# helper functions
def check_page_loaded(driver, delay, elem_type, elem_name):
    """
    check if an element is loaded on a page.
    Throws timeout exception if not loaded after specific delay.
    args:
    driver: webdriver object
    delay: delay to wait before abort
    elem_type: type of element to check for (CLASS_NAME, ID, NAME)
    """

    try:
        if elem_type == "CLASS_NAME":
            elem = WebDriverWait(driver, delay) \
                .until(EC.presence_of_element_located((By.CLASS_NAME, elem_name)))
        elif elem_type == "ID":
            elem = WebDriverWait(driver, delay) \
                .until(EC.presence_of_element_located((By.ID, elem_name)))
        elif elem_type == "NAME":
            elem = WebDriverWait(driver, delay) \
                .until(EC.presence_of_element_located((By.NAME, elem_name)))

        print("The page element <" , elem_name, "> is ready!")

    except TimeoutException:
        print("Loading page took to long. Please try again.")

if __name__ == '__main__':
    run()
