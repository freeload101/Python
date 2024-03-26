import json
import requests
import time
import array
import yaml
# for async
import asyncio
# for logging
import logging
# for command line args
import sys
# get the byte size of a vars
from sys import getsizeof
# for file management backup of JSON output etc.
import shutil
# for skipping cert errors in proxy
import ssl
# hiding warnings for ssl
import urllib3
# for setting OS env vars for proxy
import os
# for checking for files existing
import pathlib
# regex
import re
import datetime
import logging
import requests
import pprint
import re
# hidden inputs FTW __VIEWSTATE etc ...!
from bs4 import BeautifulSoup

"""
# * this python script is my includes and functions for debugging and writing APIs
#  BEFORE Phantom COPY/PASTE !!!
# * REPLACE TABS WITH SPACES
# * REMOVE PHANTOM.LOGG CLASS
# * DISABLE PROXY

# print out stuff and it look human readable ....
def get_var_name(var, globals=globals()):
    Phantom.debug("DEBUG: Running get_var_name")
    return [name for name, val in globals.items() if val is var]
"""

# for showing debug / error locally
logging.basicConfig(level=logging.DEBUG)

"""
FUNCTIONS/CLASSES
"""


# Used for Splunk Phantom because you can't use logging.error or logging.debug to get any output.
class Phantom:
    @staticmethod
    def error(message):
        logging.error(f"*** {message}  ***")

    @staticmethod
    def debug(message):
        logging.debug(f"+++ {message}")


def load_config(file_path):
    Phantom.debug("load_config")
    with open(file_path, 'r') as file:
        return json.load(file)


def proxy_enable():
    Phantom.debug("proxy_enable")
    os.environ["HTTP_PROXY"] = "http://127.0.0.1:8080"
    os.environ["HTTPS_PROXY"] = "http://127.0.0.1:8080"
    # supress warnings for ssl
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def pprint_simp(varname, pprint_value):
    """
    The point of this function is to basically parse anything and make it human-readable
    """
    Phantom.debug("pprint_simp")
    Phantom.debug("Type:  " + str(type(pprint_value)))
    try:
        # json.loads(pprint_value)
        print(json.dumps(pprint_value, indent=4))
    except ValueError:
        # convert it to string
        pprint_value = str(pprint_value)
        # replace common word boundaries
        pprint_value = re.sub(r'\s+', '_', pprint_value)
        pprint_value = re.sub(r'<', '\n', pprint_value)
        pprint_value = re.sub(r'=', '\n=', pprint_value)
        # replace all leftover control chars with \n ... if you want ...
        # pprint_value = re.sub(r'\b', '\n', pprint_value)
        Phantom.debug("\n================\n" + varname + ": " + pprint_value + "\n================\n")


def find_cookie(html_content, cookie_search):
    Phantom.debug("find_cookie")
    # https://stackoverflow.com/questions/69170069/python-requests-get-viewstate-and-eventvalidation-after-dopostback
    # Parse the webpage
    soup = BeautifulSoup(html_content, 'html.parser')
    # Find all input tags
    input_tags = soup.find_all('input')
    Phantom.debug("input_tags: " + str(input_tags))
    # Find the  input field and get its value
    cookie_input_value = soup.find('input', {'id': cookie_search}).get('value')
    pprint_simp(cookie_search, cookie_input_value)
 
 
def az_auth():
    Phantom.debug("az_auth")
    r = requests.post('https://login.microsoftonline.com/' + tenant_id + '/oauth2/v2.0/token',
                      data={'grant_type': 'client_credentials', 'client_id': app_id, 'client_secret': app_id_secret,
                            'scope': 'https://graph.microsoft.com/.default'}, verify=SSL_Verify)
    if r.status_code in [200]:
        tok_dict = json.loads(r.text)
        return tok_dict["access_token"]
    else:
        Phantom.error(r.status_code)
        Phantom.error(r.url)
        Phantom.error(r.text)
        Phantom.error(r.content)
        Phantom.error("ERROR DID NOT GET 200 STATUS CODE")


def az_get(user, folder, azfilter):
    Phantom.debug("az_get")
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    r = requests.get("https://graph.microsoft.com/beta/users/" + user + "/mailFolders/" + folder + "/messages" + azfilter,
                     headers=headers, verify=SSL_Verify)
    if r.status_code in [200]:
        # Phantom.debug(r.status_code)
        # Phantom.debug(r.url)
        # pprint_simp('r.json()', r.json())
        for i in range(len(r.json()['value'])):
            print(r.json()['value'][i])
        # Phantom.debug("DEBUG: Status 200 OK ")
    else:
        Phantom.error(r.status_code)
        Phantom.error(r.url)
        Phantom.error(r.text)
        Phantom.error(r.content)
        Phantom.error("ERROR DID NOT GET 200 STATUS CODE")


"""
MAIN
"""

# load the config
config = load_config('config.yml')
app_id = config['app_id']
app_id_secret = config['app_id_secret']
tenant_id = config['tenant_id']

# This is set to False when we enable proxy support later
SSL_Verify = True

# proxy_enable()

access_token = az_auth()

az_get('phishing@XXXXXXXXXXXXXX.com', 'SentItems', '?$select=webLink')

"""
TODO:
* pageanation
* get URL
* get header info
    _dns
    _dimkeys
    _spf
    _whatever else in headers is juicy


# /mailFolders/SentItems/messages?$count=true&$filter=isread%20eq%20false
# /mailFolders/SentItems/messages?$select=sender,subject
# Inbox, Drafts, SentItems, or DeletedItems

# The Graph API URL for accessing the specific email and its attachments
#$emailUrl = "https://graph.microsoft.com/v1.0/users/$userEmailOrId/messages/$messageId"
#$attachmentsUrl = "$emailUrl/attachments"

# https://learn.microsoft.com/en-us/archive/blogs/exchangedev/building-daemon-or-service-apps-with-office-365-mail-calendar-and-contacts-apis-oauth2-client-credential-flow
# https://stackoverflow.com/questions/40763049/obtain-access-token-for-both-microsoft-graph-and-individual-service-api-endpoint
# https://learn.microsoft.com/en-us/graph/api/message-get?view=graph-rest-1.0&tabs=http
# mail.read docs
# https://kagi.com/search?q=%22graph.microsoft.com%22+%22mail.read%22
# https://learn.microsoft.com/en-us/archive/blogs/exchangedev/building-daemon-or-service-apps-with-office-365-mail-calendar-and-contacts-apis-oauth2-client-credential-flow
# https://stackoverflow.com/questions/40763049/obtain-access-token-for-both-microsoft-graph-and-individual-service-api-endpoint
# https://learn.microsoft.com/en-us/graph/api/message-get?view=graph-rest-1.0&tabs=http


"""
