from login_data import u_name, pw

# login url
login_url = "https://mybigpoint.tennis.de/home?p_p_id=58&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&saveLastPath=0&_58_struts_action=%2Flogin%2Flogin&_58_doActionAfterLogin=false"
# headers
headers = {
    "referer" : "https://mybigpoint.tennis.de/home"
}

# payload mappings
redirect_key = "_58_redirect"
login_key = "_58_login"
pw_key = "_58_password"
remember_key = "_58_rememberMe"
# payload
payload = {
	redirect_key : "",
	login_key : u_name,
	pw_key : pw,
	remember_key : False
}

# base urls
home_base_url = "https://mybigpoint.tennis.de/group/"
profile_base_url = "https://mybigpoint.tennis.de/web/"
# variable part of urls
variable_url = "/~/10555/"

#freunde1
#ubersicht
#lk-portrait
#wettspielportrait
