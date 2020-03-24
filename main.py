import requests
#from bs4 import BeautifulSoup
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
    # process_data
    

# === log-in === #
def login():

    # login with credentials
    resp = session_requests.post(
	               consts.login_url,
	               data = ld.payload,
	               headers = dict(referer=consts.login_url)
                   )
    # check if login succesful
    assert resp.status_code != '200', "Login failed, please try again!"

def get_url(url_ending):

    user = ld.payload[consts.login_key].split('@')[0]
    url = consts.home_base_url + user + consts.post_url + url_ending
    return url

# === get requests === #
def get_home_page():

    # get base url
    base_url = get_url("home")
    # scrape home page
    resp = session_requests.get(
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
    home_content = get_home_page()
    print(home_content)
    # extract friends infos

def scrape_profile_page():

    # get profile summary infos

    # get lk infos

    # get club results infos

# === data processing === #



if __name__ == '__main__':
    run()
