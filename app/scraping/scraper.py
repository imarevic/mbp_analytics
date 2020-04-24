# imports
import app.scraping.tests.test as t
import app.scraping.logic.scraping as sc
from app.scraping.logic.helpers import check_page_loaded, pandas_to_json
from app.scraping.logic.processing import process_data
from app.scraping.logic.consts import inf_data, friends_data, profile_data, lk_data
#import time

def run_scraper():
    """
    main entry point of the program.
    """
    # global driver object
    driver = sc.create_driver("Chrome")
    # login to page
    driver = sc.login(driver)
    # scrape content of pages with relevant data
    driver, d_inf, d_friends = sc.scrape_home_page(driver)
    driver, d_profile = sc.scrape_profile_page(driver)
    driver, d_lk = sc.scrape_lk_page(driver)
    # post process_data
    #t.save_dicts(d_inf, d_friends, d_profile, d_lk)
    #d_inf, d_friends, d_profile, d_lk = t.load_dicts('d_inf_dict',
    #                                                'd_friends_dict',
    #                                                'd_profile_dict',
    #                                                'd_lk_dict')

    inf_data, friends_data, profile_data, lk_data = process_data(d_inf, d_friends, d_profile, d_lk)
    # close driver
    sc.close_driver(driver)
