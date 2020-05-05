from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import pickle

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

def merge_dict_of_dicts(list_of_dicts):
    """
    merges list of dicts
    arg: list of dicts (to be merged)
    returns: merged dict
    """
    final_dict = {}
    for d in list_of_dicts:
        for k, v in d.items():
            final_dict.setdefault(k, []).append(v)

    final_dict.update((k, [item for sublist in v for item in sublist]) for k,v in final_dict.items())
    return final_dict

def save_obj(obj, name):
    """
    saves any python object to file
    """
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    """
    loads any python object from file
    """
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)
