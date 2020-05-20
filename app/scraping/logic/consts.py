# uncomment when reading test user data from file
#from .login_data import u_name, pw

# login url
login_url = "https://mybigpoint.tennis.de"

# payload mappings
login_ul = "_58_-loginul"
login_key = "_58_login"
pw_key = "_58_password"
remember_key = "_58_rememberMe"
# login infos
user = None
password = None

# base urls
home_base_url = "https://mybigpoint.tennis.de/group/"
profile_base_url = "https://mybigpoint.tennis.de/web/"
# variable part of urls
variable_url = "/~/10555/"

# profile df cor names
profile_col_names = ['lk', 'race_position', 'race_position_in_club', 'race_points',
                      'result_singles_season', 'result_doubles_season',
                      'result_singles_career', 'result_doubles_career',
                      'result_home_singles_career', 'result_away_singles_career',
                      'result_tiebreak_singles_season', 'result_tiebreak_singles_career',
                      'result_match_tiebreak_singles_season', 'result_match_tiebreak_singles_career']

# json data placeholder
# structure (col names) are hard coded as we know it a priori
# and it will not change adaptively
final_data_init = {'Info Data': [{
                        "columns":[
                                {"text":"info_club","type":"string"},
                                {"text":"info_season","type":"string"},
                                {"text":"info_competition","type":"string"},
                                {"text":"info_rank","type":"string"}
                                ],
                        "rows":[],
                        "type":"table"
                        }],
            'Friends Data': [{
                        "columns":[
                            {"text":"friends","type":"string"}
                            ],
                        "rows":[],
                        "type":"table"
                        }],
            'Profile Data': [{
                        "columns":[
                            {"text":"lk","type":"string"},
                            {"text":"race_position","type":"string"},
                            {"text":"race_position_in_club","type":"string"},
                            {"text":"race_points","type":"string"},
                            {"text":"result_singles_season","type":"string"},
                            {"text":"result_doubles_season","type":"string"},
                            {"text":"result_singles_career","type":"string"},
                            {"text":"result_doubles_career","type":"string"},
                            {"text":"result_home_singles_career","type":"string"},
                            {"text":"result_away_singles_career","type":"string"},
                            {"text":"result_tiebreak_singles_season","type":"string"},
                            {"text":"result_tiebreak_singles_career","type":"string"},
                            {"text":"result_match_tiebreak_singles_season","type":"string"},
                            {"text":"result_match_tiebreak_singles_career","type":"string"}
                            ],
                        "rows":[],
                        "type":"table"
                        }],
            'LK Data': [{
                        "columns":[
                            {"text":"season_year","type":"string"},
                            {"text":"date","type":"string"},
                            {"text":"oponent","type":"string"},
                            {"text":"score","type":"string"},
                            {"text":"result","type":"string"},
                            {"text":"lk_points","type":"string"},
                            {"text":"bonus_points","type":"string"},
                            {"text":"contest","type":"string"}
                            ],
                        "rows":[],
                        "type":"table"
                        }]
            }
