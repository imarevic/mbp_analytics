# scraping logic
from selenium import webdriver
from bs4 import BeautifulSoup
from . import consts as c
from .helpers import check_page_loaded, merge_dict_of_dicts
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

def close_driver(driver):
    """
    closes the webdriver session explicitly.
    """
    driver.close()

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
    lk_dict_list = []
    for elem in lk_year_elems:
        # extract data and add to dict
        season_year = elem.text.strip()
        print('Retrieving ', season_year, ' details...')
        lk_temp_dict = get_lk_details(driver, season_year)
        lk_dict_list.append(lk_temp_dict)
    # merge list of dicts in final dict
    final_lk_dict = merge_dict_of_dicts(lk_dict_list)

    return driver, final_lk_dict

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
    lk_details_table = lk_details_table[:-1] # rm last elem (not needed)
    lk_details_table = [elem.find_all('td') for elem in lk_details_table]
    # get data row wise
    data_lk_dict = {
        'season_year' : [],
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
            data_lk_dict['season_year'].append(year)
            data_lk_dict['date'].append(row[0].text.strip())
            data_lk_dict['oponent'].append(row[1].text.strip())
            data_lk_dict['score'].append(row[2].text.strip())
            data_lk_dict['result'].append(row[3].find('img', alt=True)['alt'].strip()) if row[3].text.strip() != '-' else data_lk_dict['result'].append('irrelevant')
            data_lk_dict['lk_points'].append(row[4].text.strip())
            data_lk_dict['bonus_points'].append(row[5].text.strip())
            data_lk_dict['contest'].append(row[6].text.strip())
        else:
            data_lk_dict['season_year'].append(year)
            data_lk_dict['date'].append(row[0].text.strip()) if row_length==4 else data_lk_dict['date'].append(data_lk_dict['date'][i-1])
            data_lk_dict['contest'].append('Tournament: ' + row[1].text.strip()) if row_length==4 else data_lk_dict['contest'].append(data_lk_dict['contest'][i-1])
            data_lk_dict['oponent'].append(row[0].text.strip()) if row_length==6 else data_lk_dict['oponent'].append('irrelevant')
            data_lk_dict['score'].append(row[1].text.strip()) if row_length==6 else data_lk_dict['score'].append('irrelevant')
            data_lk_dict['result'].append(row[2].find('img', alt=True)['alt'].strip()) if (row_length==6 and row[2].text.strip() != '-') else data_lk_dict['result'].append('irrelevant')
            data_lk_dict['lk_points'].append(row[3].text.strip()) if row_length==6 else data_lk_dict['lk_points'].append('irrelevant')
            data_lk_dict['bonus_points'].append("n/a")

    return data_lk_dict
