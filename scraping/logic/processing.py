import pandas as pd
from .helpers import pandas_to_json
from .consts import profile_col_names
pd.set_option('display.max_columns', 40)

# data processing
def process_data(inf_dict, friends_dict, profile_dict, lk_dict):
    # convert dicts to pandas dfs
    inf_df = pd.DataFrame(inf_dict, index=[0])
    friends_df = pd.DataFrame(friends_dict)
    profile_df = pd.DataFrame(profile_dict, index=[0])
    lk_df = pd.DataFrame(lk_dict)

    # rename columns in profile df
    profile_df.columns = profile_col_names
    # calculate additional infos and clean up dfs

    # return json objects
