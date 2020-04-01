from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import consts as c
import login_data as ld
import pandas as pd
import json


def run_scraper():
    """
    main entry point of the program.
    """
    # global driver object
    driver = create_driver("Chrome")
    # login to page
    driver = login(driver)
    # scrape content of pages with relevant data
    driver, d_inf, d_friends = scrape_home_page(driver)
    driver, d_profile = scrape_profile_page(driver)
    driver, d_lk = scrape_lk_page(driver)
    # post process_data
    process_data(d_inf, d_friends, d_profile, d_lk)
    
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
    driver.get(c.login_url)
    driver.find_element_by_id(c.login_ul)\
        .click()
    driver.find_element_by_id(c.login_key) \
        .send_keys(c.user)
    driver.find_element_by_id(c.pw_key) \
        .send_keys(c.password)
    driver.find_element_by_class_name("aui-button-input-submit") \
        .click()

    return driver

# === scraping === #
def scrape_home_page(driver):

    # check if target page loaded
    check_page_loaded(driver, 5, "CLASS_NAME", "aui-column-content")
    # initial empty dict for data
    data_inf = {}
    # first get home page base content
    home_html = driver.page_source
    home_content = BeautifulSoup(home_html, 'html.parser')
    # extract general infos
    info_elems = list(home_content.find_all('div', class_='aui-column-content'))
    for i, elem in enumerate(info_elems):
        if elem.text == ' Verein ':
            data_inf['info_club'] = info_elems[i+1].text.strip()
        elif elem.text == ' Mannschaften ':
            season_inf = info_elems[i+1].text
            season_split = season_inf.split("  ")
            data_inf['info_season'] = season_split[0]
            comp_rank_split = season_split[1].split(", ")
            data_inf['info_competition'] = comp_rank_split[0]
            data_inf['info_rank'] = comp_rank_split[1]

    # extract friends infos
    driver.find_element_by_link_text("Freunde") \
        .click()
    # check if target page loaded
    check_page_loaded(driver, 5, "CLASS_NAME", "person-link")
    # extract friends infos
    friends_html = driver.page_source
    friends_content =  BeautifulSoup(friends_html, 'html.parser')
    friends_elems = list(friends_content \
        .find_all('span', class_='person-link'))

    # get friends data
    friends_list = [elem.text for elem in friends_elems]
    data_friends = {
        'friends' : friends_list
    }

    return driver, data_inf, data_friends

def scrape_profile_page(driver):

    ## extract profile summary infos ##
    driver.find_element_by_class_name("usercommunity") \
        .click()
    # check if target page loaded
    check_page_loaded(driver, 5, "CLASS_NAME", "bp-statistik-big")
    # extract friends infos
    profile_html = driver.page_source
    profile_content =  BeautifulSoup(profile_html, 'html.parser')
    profile_base_elems = list(profile_content \
        .find_all('tr'))
    profile_base_elems = [elem.find_all('td', {'class':['left','right']}) for elem in profile_base_elems]
    profile_base_elems = [elem for elem in profile_base_elems if elem != []]
    # get key value base pairs
    data_profile = {}
    for elem in profile_base_elems:
        key_txt = elem[0].text.strip()
        value_txt = elem[1].text.strip()
        data_profile[key_txt] = value_txt

    ## extract profile detail infos ##
    profile_detail_elems = list(profile_content \
        .find_all('tr', class_='listing-row'))
    profile_detail_elems = [elem.find_all('td') for elem in profile_detail_elems]
    # get key value detail pairs
    for elem in profile_detail_elems:
        key_txt = elem[0].text.strip()
        value_txt = elem[1].text.strip()
        data_profile[key_txt] = value_txt

    return driver , data_profile


def scrape_lk_page(driver):

    driver.find_element_by_link_text("Generali LK-Portrait") \
        .click()
    # check if target page loaded
    check_page_loaded(driver, 5, "CLASS_NAME", "bp-list-menu")
    lk_html = driver.page_source
    lk_content =  BeautifulSoup(lk_html, 'html.parser')
    lk_year_elems = list(lk_content \
            .find_all('ul', class_='bp-list-menu')[1] \
            .findChildren(recursive=False))
    # iterate over years and get table infos
    data_lk = {}
    for elem in lk_year_elems:
        # extract data and add to dict
        season_year = elem.text.strip()
        print('Retrieving ', season_year, ' details...')
        data_lk[season_year] = get_lk_details(driver, season_year)

    return driver, data_lk

def get_lk_details(driver, year):

    driver.find_element_by_link_text(year).click()
    # check if target page loaded
    check_page_loaded(driver, 5, "CLASS_NAME", "taglib-search-iterator")
    lk_details_html = driver.page_source
    lk_details_content = BeautifulSoup(lk_details_html, 'html.parser')
    lk_details_table = list(
        lk_details_content \
        .find_all('table', class_='taglib-search-iterator')[0] \
        .find_all('tr', class_='listing-row')
        )
    lk_details_table = lk_details_table[:-1] # rm lat elem (not needed)
    lk_details_table = [elem.find_all('td') for elem in lk_details_table]
    # get data row wise
    data_tr_dict = {
        'date' : [],
        'oponent' : [],
        'score' : [],
        'result' : [],
        'lk_points' : [],
        'bonus_points' : [],
        'contest' : []
    }
    for i, row in enumerate(lk_details_table):
        # selection logic
        row_length = len(row)
        if row_length == 7:
            data_tr_dict['date'].append(row[0].text.strip())
            data_tr_dict['oponent'].append(row[1].text.strip())
            data_tr_dict['score'].append(row[2].text.strip())
            data_tr_dict['result'].append(row[3].text.strip())
            data_tr_dict['lk_points'].append(row[4].text.strip())
            data_tr_dict['bonus_points'].append(row[5].text.strip())
            data_tr_dict['contest'].append(row[6].text.strip())
        else:
            data_tr_dict['date'].append(row[0].text.strip()) if row_length==4 else data_tr_dict['date'].append(data_tr_dict['date'][i-1])
            data_tr_dict['contest'].append('Tournament: ' + row[1].text.strip()) if row_length==4 else data_tr_dict['contest'].append(data_tr_dict['contest'][i-1])
            data_tr_dict['oponent'].append(row[0].text.strip()) if row_length==6 else data_tr_dict['oponent'].append('irrelevant')
            data_tr_dict['score'].append(row[1].text.strip()) if row_length==6 else data_tr_dict['score'].append('irrelevant')
            data_tr_dict['result'].append(row[2].text.strip()) if row_length==6 else data_tr_dict['result'].append('irrelevant')
            data_tr_dict['lk_points'].append(row[3].text.strip()) if row_length==6 else data_tr_dict['lk_points'].append('irrelevant')
            data_tr_dict['bonus_points'].append("n/a")

    return data_tr_dict


# === data processing === #
# TODO:
# save data to disk during development (testing of data processing)
# profile data: create win and loss codings
# bring data into format that can be used in frontend
def process_data(inf_dict, friends_dict, profile_dict, lk_dict):
    pass



# === helper functions === #
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

def pandas_to_json(pandas_df, orientation='index'):
    """
    converts  pandas df to json string
    args:
    dict_obj: dictionary object
    returns: json string
    """
    return pandas_df.to_json(orient=orientation)


if __name__ == '__main__':
    run_scraper()
