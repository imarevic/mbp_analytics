import pandas as pd

# data processing
def process_data(inf_dict, friends_dict, profile_dict, lk_dict):

    lk_df = pd.DataFrame(profile_dict)
    print(lk_df.head)
