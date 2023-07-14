import phantom.rules as phantom
import json
from datetime import datetime, timedelta

phantom.debug("input_filter() called")

    
################################################################################
## Global Custom Code Start
################################################################################

################################################################################
## Global Custom Code End
################################################################################

@phantom.playbook_block()
def on_start(container):
    phantom.debug('on_start() called')

    # call 'code_1' block
    code_1(container=container)
    import logging
    import sys
    sys.stderr.write('Error message\n')
    #logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
    logging.debug('This message should go to the log file')
    logging.info('So should this')
    logging.warning('And this, too')
    logging.error('And non-ASCII stuff, too, like Øresund and Malmö')
    return

@phantom.playbook_block()
def code_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("code_1() called")

    ################################################################################
    ## Custom Code Start
    ################################################################################
    import json
    import requests
    import time
    import array
    import yaml
    
    # for async
    import asyncio
    import logging
    
    # for command line args
    import sys
    
    # get the byte size of a vars
    from sys import getsizeof
    
    
    # for file mamagment backup of JSON output etc..
    import shutil
    
    # for skipping cert errors in proxy
    import ssl
    # hiding warnings for ssl
    import urllib3
    
    # for setting OS env vars for proxy
    import os
    
    # for checking for files existing
    import pathlib
    
    # This is set to False when we enable proxy support later
    VAR_SSL_FLAG=True
    
    
    # regex
    import re
    
    # to check dates on last seen key
    import datetime
    #import dateutil.parser
    import pytz
    
    ############################################ DANGER SECURTY ############
    ############################################ DANGER SECURTY ############
    ############################################ DANGER SECURTY ############
    ############################################ DANGER SECURTY ############
    
    with open("config.yml", "w") as file:
       lines = ['{\r        "app_id":"66f2XXXXXXXXXXXXXXXXXXXXXXXXXX496f98",\r        "app_id_secret":"gKK8QXXXXXXXXXXXXXXXXXXXXXXXXXXc_a",\r        "tenant_id":"6663XXXXXXXXXXXXXXXXXXXXXXXXXX2154"\r}']
       file.writelines(lines)
       file.close()
    
    ############################################ DANGER SECURTY ############
    ############################################ DANGER SECURTY ############
    ############################################ DANGER SECURTY ############
    ############################################ DANGER SECURTY ############
    
    
    
    
    
    ############################################################ FUNCTIONS
    def LOADCONFIG():
       print("DEBUG: Running LOADCONFIG")
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
    
    
    def PROXY():
       print("DEBUG: Running PROXY")
       os.environ["HTTP_PROXY"] = "http://127.0.0.1:8080"
       os.environ["HTTPS_PROXY"] = "http://127.0.0.1:8080"
       global VAR_SSL_FLAG
       VAR_SSL_FLAG = False
       # supress warnings for ssl
       urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    ################################################################################ AUTH
    def FUNC_AUTH():
       print("DEBUG: Running FUNC_AUTH")
       r = requests.post('https://login.microsoftonline.com/' + tenant_id + '/oauth2/v2.0/token',
                         data={'grant_type': 'client_credentials', 'client_id': app_id, 'client_secret': app_id_secret,
                               'scope': 'https://graph.microsoft.com/.default'}, verify=VAR_SSL_FLAG)
       if r.status_code in [200]:
          # print("DEBUG: Status 200 OK!")
          tok_dict = json.loads(r.text)
          global access_token
          access_token = tok_dict["access_token"]
          print("DEBUG: Access Token is ", access_token)
       else:
          print(r.status_code)
          print(r.url)
          print(r.text)
          print(r.content)
          print("ERROR DID NOT GET 201 STATUS CODE")
    
       ############################################################ MAIN
    
    #LOADCONFIG()
    #PROXY()
    #FUNC_AUTH()
    sys.stderr.write('Error message\n')
    #logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
    logging.debug('This message should go to the log file')
    logging.info('So should this')
    logging.warning('And this, too')
    logging.error('And non-ASCII stuff, too, like Øresund and Malmö')

    ################################################################################
    ## Custom Code End
    ################################################################################

    return


@phantom.playbook_block()
def on_finish(container, summary):
    phantom.debug("on_finish() called")

    ################################################################################
    ## Custom Code Start
    ################################################################################
    import logging
    import sys
    # Write your custom code here...
    sys.stderr.write('Error message\n')
    #logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
    logging.debug('This message should go to the log file')
    logging.info('So should this')
    logging.warning('And this, too')
    logging.error('And non-ASCII stuff, too, like Øresund and Malmö')

    ################################################################################
    ## Custom Code End
    ################################################################################

    return
