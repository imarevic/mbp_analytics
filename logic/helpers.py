from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

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

def pandas_to_json(pandas_df, orientation='index'):
    """
    converts  pandas df to json string
    args:
    dict_obj: dictionary object
    returns: json string
    """
    return pandas_df.to_json(orient=orientation)
