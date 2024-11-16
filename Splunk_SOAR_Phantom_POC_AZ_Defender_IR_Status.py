"""

"""


import phantom.rules as phantom
import json
from datetime import datetime, timedelta


@phantom.playbook_block()
def on_start(container):
    phantom.debug('on_start() called')

    # call 'debug_1' block
    debug_1(container=container)

    return

@phantom.playbook_block()
def debug_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("debug_1() called")

    data_summary_requestid_value = container.get("data", {}).get("summary", {}).get("requestId", None)
    data_summary_userid_value = container.get("data", {}).get("summary", {}).get("userId", None)
    data_disposition_value = container.get("data", {}).get("disposition", None)
    data_incidentId_value = container.get("data", {}).get("summary", {}).get("incidentId", None)
    phantom.debug("data_incidentId_value: ")
    phantom.debug( data_incidentId_value )
    
    parameters = []

    parameters.append({
        "input_1": data_summary_requestid_value,
        "input_2": data_summary_userid_value,
        "input_3": data_incidentId_value,
        "input_4": None,
        "input_5": None,
        "input_6": None,
        "input_7": None,
        "input_8": None,
        "input_9": None,
        "input_10": None,
    })

    ################################################################################
    ## Custom Code Start
    ################################################################################
    phantom.debug("DEBUG: Custom Code Start")
    # replace:
    # with: phantom.error
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
    VAR_SSL_FLAG = True

    # regex
    import re

    # to check dates on last seen key
    import datetime
    # import dateutil.parser
    #import pytz

    #Sep 19, 12:22:26 : data_summary_userid_value: 36688b1d-1916-4b80-9627-218567ddec1b
    #Sep 19, 12:22:26 : data_summary_requestid_value: b57f2a9e-a70e-4171-9be2-2b4f6c004300

    #global data_summary_requestid_value
    #global data_summary_userid_value


    # WORKING !!!!
    #data_summary_requestid_value="1747fb72-23f3-43ed-b763-798cd31fc100"

    global headers
    global access_token
    
    #data_summary_requestid_value="c0234c93-80f3-42d2-9cf9-dbca84eaa000"

    #data_summary_userid_value="36688b1d-1916-4b80-9627-218567ddec1b"


    ############################################ DANGER SECURTY ############
    ############################################ DANGER SECURTY ############
    ############################################ DANGER SECURTY ############
    ############################################ DANGER SECURTY ############

    with open("config.yml", "w") as file:
        lines = [
            '{\r        "app_id":"66f2dfec-e2a2-4e1a-ab21-432e30496f98",\r        "app_id_secret":"REDACTED",\r        "tenant_id":"REDACTED\r}']
        file.writelines(lines)
        file.close()


    ############################################ DANGER SECURTY ############
    ############################################ DANGER SECURTY ############
    ############################################ DANGER SECURTY ############
    ############################################ DANGER SECURTY ############

        
        ############################################################ FUNCTIONS
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


        def PROXY():
            phantom.error("DEBUG: Running PROXY")
            os.environ["HTTP_PROXY"] = "http://127.0.0.1:8080"
            os.environ["HTTPS_PROXY"] = "http://127.0.0.1:8080"
            global VAR_SSL_FLAG
            VAR_SSL_FLAG = False
            # supress warnings for ssl
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    

            ################################################################################ AUTH
        def FUNC_AUTH():
                print("DEBUG: Running FUNC_AUTH")
                r = requests.post('https://login.windows.net/' + tenant_id + '/oauth2/token',
                                  data={'resource': 'https://api.security.microsoft.com', 'client_id': app_id, 'client_secret': app_id_secret, 'grant_type': 'client_credentials'}, verify=VAR_SSL_FLAG)
                if r.status_code in [200]:
                    # print("DEBUG: Status 200 OK!")
                    tok_dict = json.loads(r.text)
                    global access_token
                    access_token = tok_dict["access_token"]
                    # print("DEBUG: Access Token is: XXXXXXXXXXXXXXX ", access_token[-4:])
                    phantom.debug("200 STATUS CODE AUTH SUCCESS" )
                    phantom.debug(r.status_code)
                    phantom.debug(r.url)
                    phantom.debug(r.text)
                    phantom.debug(r.content)
                    phantom.debug("data_incidentId_value: ")
                    phantom.debug( data_incidentId_value )
                else:
                    phantom.error(r.status_code)
                    phantom.error(r.url)
                    phantom.error(r.text)
                    phantom.error(r.content)
                    phantom.error("ERROR DID NOT GET 200 STATUS CODE AUTH FAILED")


                global headers
                headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
                r = requests.patch('https://api.securitycenter.microsoft.com/api/incidents/' + data_incidentId_value , data=json.dumps(
                    {'status': 'resolved'}),
                                   headers=headers, verify=VAR_SSL_FLAG)
                if r.status_code in [200]:
                    phantom.debug("DEBUG: Status 200 OK incident updated ")
                    phantom.debug(r.status_code)
                    phantom.debug(r.url)
                    phantom.debug(r.text)
                    phantom.debug(r.content)
                else:
                    phantom.error(r.status_code)
                    phantom.error(r.url)
                    phantom.error(r.text)
                    phantom.error(r.content)
                    phantom.error("ERROR DID NOT GET 200 STATUS CODE incident NOT updated ")
                    
            ############################################################ MAIN
    phantom.debug("DEBUG: MAIN")
    
    LOADCONFIG()
    FUNC_AUTH()

    phantom.debug("DEBUG: Custom Code End")

    ################################################################################
    ## Custom Code End
    ################################################################################

    #phantom.custom_function(custom_function="community/debug", parameters=parameters, name="debug_1")

    return


@phantom.playbook_block()
def on_finish(container, summary):
    phantom.debug("on_finish() called")

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    return
