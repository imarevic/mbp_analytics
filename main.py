import requests
from bs4 import BeautifulSoup
import consts
import login_data as ld

# get session object
session_requests = requests.session()

def run():
    """
    main entry point of the program.
    """
    # login to page
    login()
    # scrape content of pages with relevant data
    scrape_home_page()

# === loging === #
def login():

    # login with credentials
    resp = session_requests.post(
	               consts.login_url,
	               data = ld.payload,
	               headers = dict(referer=consts.login_url)
                   )
    # check if login succesful
    assert resp.status_code != '200', "Login failed, please try again!"

def get_home_url():

    user = consts.payload[consts.login_key].split('@')[0]
    home_url = consts.home_pre_part_url + user + consts.home_post_part_url
    return home_url

# === get requests === #
def get_home_page():

    # get base url
    home_url = get_home_url()
    # scrape home page
    resp = session_requests.get(
        home_url,
	    headers = dict(referer = home_url)
    )
    # check resp
    assert resp.status_code != '200', "Could not get content of home page, \
                                       please try again!"

    return resp.content


# === scraping === #
def scrape_home_page():

    # first get home page content
    home_content = get_home_page()


# === data processing === #



if __name__ == '__main__':
    run()
