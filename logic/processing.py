import pandas as pd
pd.set_option('display.max_columns', 40)

# data processing
def process_data(inf_dict, friends_dict, profile_dict, lk_dict):
    # convert dicts to pandas dfs
    inf_df = pd.DataFrame(inf_dict, index=[0])
    friends_df = pd.DataFrame(friends_dict)
    profile_df = pd.DataFrame(profile_dict, index=[0])
    lk_df = pd.DataFrame(lk_dict['2019'])
    #lk_df = pd.DataFrame.from_dict({(i,j): lk_dict[i][j]
    #                       for i in lk_dict.keys()
    #                       for j in lk_dict[i].keys()},
    #                   orient='index')
    print(lk_dict)
    print(lk_df)
