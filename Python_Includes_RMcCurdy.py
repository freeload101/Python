import logging
logging.basicConfig(level=logging.DEBUG)
import requests
import pprint
import re


# FOR PROXY STUFF
# for command line args
import sys
# for skipping cert errors in proxy
import ssl
# hiding warnings for ssl
import urllib3
# for setting OS env vars for proxy
import os
VAR_SSL_FLAG = True
# END PROXY STUFF

# hidden inputs FTW __VIEWSTATE etc ...!
from bs4 import BeautifulSoup


###################################################### FUNCs  ..

################################################################################ AUTH
def FUNC_AUTH():
    phantom.debug("DEBUG: Running FUNC_AUTH")
    r = requests.post('https://login.microsoftonline.com/' + tenant_id + '/oauth2/v2.0/token',
                      data={'grant_type': 'client_credentials', 'client_id': app_id, 'client_secret': app_id_secret, 'scope': 'https://graph.microsoft.com/.default'}, verify=VAR_SSL_FLAG)
    if r.status_code in [200]:
        tok_dict = json.loads(r.text)
        global access_token
        access_token = tok_dict["access_token"]
    else:
        phantom.error(r.status_code)
        phantom.error(r.url)
        phantom.error(r.text)
        phantom.error(r.content)
        phantom.error("ERROR DID NOT GET 201 STATUS CODE")

    # headers = {'Authorization': }
    global headers
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    r = requests.post('https://graph.microsoft.com/v1.0/IdentityProtection/riskyUsers/dismiss', data=json.dumps(
        {'userIds': [data_summary_userid_value]}),
                      headers=headers, verify=VAR_SSL_FLAG)

    #json_data = json.dumps(data)
    if r.status_code in [204]:
        phantom.debug("DEBUG: Status 204 OK ")
        phantom.debug(r.status_code)
        phantom.debug(r.url)
        phantom.debug(r.text)
        phantom.debug(r.content)
    else:
        phantom.error(r.status_code)
        phantom.error(r.url)
        phantom.error(r.text)
        phantom.error(r.content)
        phantom.error("ERROR DID NOT GET 201 STATUS CODE")


# use YAML for creds no plain text creds in scripts !
def LOADCONFIG():
    phantom.debug("DEBUG: Running LOADCONFIG")
    yaml.warnings({'YAMLLoadWarning': False})

    Loader = yaml.FullLoader
    with open("config.yml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
    global app_id
    global app_id_secret
    global tenant_id
    app_id = (cfg['app_id'])
    app_id_secret = (cfg['app_id_secret'])
    tenant_id = (cfg['tenant_id'])



# for Splunk SOAR logging ... 
class phantom:
    @staticmethod
    def error(message):
        logging.error(f"Error: {message}")

    @staticmethod
    def debug(message):
        logging.debug(f"Debug: {message}")


# Proxy support see BurpSuite!!!
def PROXY():
    print("DEBUG: Running PROXY")
    os.environ["HTTP_PROXY"] = "http://127.0.0.1:8080"
    os.environ["HTTPS_PROXY"] = "http://127.0.0.1:8080"
    global VAR_SSL_FLAG
    VAR_SSL_FLAG = False
    # supress warnings for ssl
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# sso.connect.pingidentity.com
# sso.newellrubbermaid.com

# print out stuff and it look human readable ....
def get_var_name(var, globals=globals()):
    return [name for name, val in globals.items() if val is var]

def pprint_ForRealz(varname,varvalue):
    # replace common word boundaries
    varvalue = re.sub(r'\s+', '_', varvalue)
    varvalue = re.sub(r'<', '\n', varvalue)
    #varvalue = re.sub(r'=', '\=', varvalue)
    # replace all left over control chars with \n ... if you want ...
    #var1 = re.sub(r'\b', '\n', var1)
    logging.info("\n================\n"+ varname +": " + varvalue +"\n================\n")


def FindCookie(HTMLContent,CookieSearch):
    # https://stackoverflow.com/questions/69170069/python-requests-get-viewstate-and-eventvalidation-after-dopostback
    # Parse the webpage
    soup = BeautifulSoup(HTMLContent, 'html.parser')
    # Find all input tags
    input_tags = soup.find_all('input')
    logging.info("input_tags: "+str(input_tags))
    # Find the  input field and get its value
    global CookieInputValue
    CookieInputValue = soup.find('input', {'id': CookieSearch}).get('value')
    pprint_ForRealz(CookieSearch,CookieInputValue)

# main-sh

PROXY()

url = 'https://akamai.indoorfinders.com/login.aspx'
response1 = requests.get(url,verify=VAR_SSL_FLAG)

FindCookie(response1.content,'__VIEWSTATE')
FindCookie(response1.content,'__VIEWSTATEGENERATOR')
FindCookie(response1.content,'__EVENTVALIDATION')
FindCookie(response1.content,'ssoLinkButton')






#url = 'https://newellbrands.indoorfinders.com/login.aspx'
#response2 = requests.get(url,verify=VAR_SSL_FLAG,cookies=response1.cookies)

#pprint_ForRealz(response2.cookies)
