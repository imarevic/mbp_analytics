from selenium import webdriver
from bs4 import BeautifulSoup
import consts
import login_data as ld


def run():
    """
    main entry point of the program.
    """
    # create driver session object
    driver = create_driver("Chrome")
    # login to page
    login()
    # scrape content of pages with relevant data
    scrape_home_page()
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
def login():

    # login with credentials
    pass

def get_url(url_ending):

    user = consts.payload[consts.login_key].split('@')[0]
    url = consts.home_base_url + user + consts.variable_url + url_ending
    return url

# === get requests === #
def get_home_page():

    # get base url
    base_url = get_url("home")
    # scrape home page
    resp = session.get(
        base_url,
	    headers = dict(referer = base_url)
    )
    # check resp
    assert resp.status_code != '200', "Could not get content of home page, \
                                       please try again!"

    return resp.content


# === scraping === #
def scrape_home_page():

    # first get home page base content
    home_html = get_home_page()
    home_content = BeautifulSoup(home_html, 'html.parser')
    #infos_content = home_content.find_all('div', class_='aui-column-content')
    #[print(i) for i in infos_content]
    print(home_content.prettify())
    # extract friends infos

def scrape_profile_page():
    pass
    # get profile summary infos

    # get lk infos

    # get club results infos

# === data processing === #



if __name__ == '__main__':
    run()
