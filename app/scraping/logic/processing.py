import pandas as pd
from .helpers import pandas_to_json
from .consts import profile_col_names
pd.set_option('display.max_columns', 40)
import sys

# data processing
def process_data(inf_dict, friends_dict, profile_dict, lk_dict, final_data_dict):
    # convert dicts to pandas dfs
    inf_df = pd.DataFrame(inf_dict, index=[0])
    friends_df = pd.DataFrame(friends_dict)
    profile_df = pd.DataFrame(profile_dict, index=[0])
    lk_df = pd.DataFrame(lk_dict)

    # rename columns in profile df
    profile_df.columns = profile_col_names
    # calculate additional infos and clean up dfs
    # inf_df:
    inf_df['info_rank'] = inf_df['info_rank'].str.split()
    inf_df['info_rank'] = inf_df['info_rank'].values.tolist()[0][1]
    # profile_df:
    profile_df = split_wins_and_losses(profile_df, ':')
    # lk_df:
    lk_df = lk_df[lk_df['result'] != 'irrelevant']
    lk_df['match_type'] = lk_df.apply(lambda x: 'doubles' if x['lk_points'] == '-' else 'singles', axis=1)
    # return final data dict
    final_data_dict['Info Data'][0]['rows'] = inf_df.values.tolist()
    final_data_dict['Friends Data'][0]['rows'] = friends_df.values.tolist()
    final_data_dict['Profile Data'][0]['rows'] = profile_df.values.tolist()
    final_data_dict['LK Data'][0]['rows'] = lk_df.values.tolist()

    return final_data_dict

def split_wins_and_losses(df, separator):
    """
    splits a column by given separator and
    creates new columns
    args:
    df: a data frame
    separator: separator to split by
    returns: new df wit split columns
    """

    for col in df:
        lst_entry = df[col].str.split(separator)[0]
        len_lst_entry = len(lst_entry)
        if len_lst_entry > 1:
            df[col + '_win'] = lst_entry[0]
            df[col + '_loss'] = lst_entry[1]
            del df[col]
    return df
