from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import consts
import login_data as ld


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

    # wait for page to payload
    # TODO: implement generic function
    #       that waits for page to be loaded from previous step 

    # first get home page base content
    home_html = driver.page_source
    home_content = BeautifulSoup(home_html, 'html.parser')
    # extract general infos
    info_elems = list(home_content.find_all('div', class_='aui-column-content'))
    for i, elem in enumerate(info_elems):
        if elem.text == ' Verein ':
            consts.data['info_club'] = info_elems[i+1].text.strip()
        elif elem.text == ' Mannschaften ':
            season_inf = info_elems[i+1].text
            season_split = season_inf.split("  ")
            consts.data['info_season'] = season_split[0]
            comp_rank_split = season_split[1].split(", ")
            consts.data['info_competition'] = comp_rank_split[0]
            consts.data['info_rank'] = comp_rank_split[1]

    # extract friends infos

    return driver

def scrape_profile_page(driver):
    pass
    # get profile summary infos

    # get lk infos

    # get club results infos

# === data processing === #



if __name__ == '__main__':
    run()
