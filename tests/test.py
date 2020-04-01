#from selenium import webdriver
import pickle
#driver = webdriver.Chrome()

def save_obj(obj, name):
    with open('tests/' + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open('tests/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

def save_dicts(d_inf, d_friends, d_profile, d_lk):
        save_obj(d_inf, 'd_inf_dict')
        save_obj(d_friends, 'd_friends_dict')
        save_obj(d_profile, 'd_profile_dict')
        save_obj(d_lk, 'd_lk_dict')

def load_dicts(d_inf_name, d_friends_name, d_profile_name, d_lk_name):
    return load_obj(d_inf_name),load_obj(d_friends_name), load_obj(d_profile_name), load_obj(d_lk_name)
