"""
To test use use Container ID 410766 or 409801\n\n 
"""


import phantom.rules as phantom
import json
from datetime import datetime, timedelta


@phantom.playbook_block()
def on_start(container):
    phantom.debug('on_start() called')
 
    get_incident_1(container=container)

    return

@phantom.playbook_block()
def request_token(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("request_token() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    ################################################################################
    # Get the bearer token 
    # This needs the tenent_id, the 
    # client_id and the  client secret
    # 
    # 
    ################################################################################

    parameters = []

    parameters.append({
        "body": "grant_type=client_credentials&client_id=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX&client_secret=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX2F%2Fgraph.microsoft.com",
        "headers": "{\"Content-Type\": \"application/x-www-form-urlencoded\"}",
        "location": "/token",
    })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("post data", parameters=parameters, name="request_token", assets=["defender token request 091523"])

    return


@phantom.playbook_block()
def update_incident(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("update_incident() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    headers_formatted_string = phantom.format(
        container=container,
        template="""{{\"Authorization\": \"Bearer {0}\",\"Content-Type\":\"application/json\"}}""",
        parameters=[
            "request_token:action_result.data.*.response_body.access_token"
        ])
    location_formatted_string = phantom.format(
        container=container,
        template="""/security/incidents/{0}\n""",
        parameters=[
            "get_incident_1:action_result.data.*.summary.incidentId"
        ])

    request_token_result_data = phantom.collect2(container=container, datapath=["request_token:action_result.data.*.response_body.access_token","request_token:action_result.parameter.context.artifact_id","request_token:action_result.parameter.context.artifact_external_id"], action_results=results)
    get_incident_1_result_data = phantom.collect2(container=container, datapath=["get_incident_1:action_result.data.*.summary.incidentId","get_incident_1:action_result.parameter.context.artifact_id","get_incident_1:action_result.parameter.context.artifact_external_id"], action_results=results)

    parameters = []

    # build parameters list for 'update_incident' call
    for request_token_result_item in request_token_result_data:
        for get_incident_1_result_item in get_incident_1_result_data:
            if location_formatted_string is not None:
                parameters.append({
                    "body": "{\"status\": \"resolved\"}",
                    "headers": headers_formatted_string,
                    "location": location_formatted_string,
                    "context": {'artifact_id': get_incident_1_result_item[1], 'artifact_external_id': get_incident_1_result_item[2]},
                })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("patch data", parameters=parameters, name="update_incident", assets=["ms graph endpoint 110823"])

    return


@phantom.playbook_block()
def get_incident_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("get_incident_1() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    external_id_value = container.get("external_id", None)

    parameters = []

    if external_id_value is not None:
        parameters.append({
            "id": external_id_value,
        })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("get incident", parameters=parameters, name="get_incident_1", assets=["builtin_mc_connector"], callback=decision_1)

    return


@phantom.playbook_block()
def debug_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("debug_1() called")

    get_incident_1_result_data = phantom.collect2(container=container, datapath=["get_incident_1:action_result.data.*.disposition_name"], action_results=results)

    get_incident_1_result_item_0 = [item[0] for item in get_incident_1_result_data]

    parameters = []

    parameters.append({
        "input_1": get_incident_1_result_item_0,
        "input_2": None,
        "input_3": None,
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

    # Write your custom code here..


    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.custom_function(custom_function="community/debug", parameters=parameters, name="debug_1", callback=decision_1)

    return

@phantom.playbook_block()
def code_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("code_1() called")

    ################################################################################
    ## Custom Code Start
    ################################################################################

    phantom.error("ERROR Status is not 5 (Closed)")
    raise Exception("ERROR Status is not 5 (Closed)")

    ################################################################################
    ## Custom Code End
    ################################################################################

    return


@phantom.playbook_block()
def decision_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("decision_1() called")

    # check for 'if' condition 1
    found_match_1 = phantom.decision(
        container=container,
        conditions=[
            ["get_incident_1:action_result.data.*.status", "!=", 5]
        ],
        delimiter=None)

    # call connected blocks if condition 1 matched
    if found_match_1:
        code_1(action=action, success=success, container=container, results=results, handle=handle)
        return

    # check for 'else' condition 2
    code_3(action=action, success=success, container=container, results=results, handle=handle)

    return


@phantom.playbook_block()
def code_3(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("code_3() called")

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...
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

    # regex
    import re

    import datetime

    #### START

    # This is set to False when we enable proxy support later
    VAR_SSL_FLAG = True

    # for showing debug / error localy
    logging.basicConfig(level=logging.DEBUG)

    global data_summary_userid_value
    data_summary_userid_value = container.get("data", {}).get("summary", {}).get("userId", None)
    get_incident_1_result_data = phantom.collect2(container=container, datapath=["get_incident_1:action_result.data.*.disposition_name"], action_results=results)

    get_incident_1_result_item_0 = [item[0] for item in get_incident_1_result_data]

    # worked with burp using BETA once ...
    # data_summary_requestid_value=['c0234c93-80f3-42d2-9cf9-dbca84eaa000']

    # Test userIds Only need userIds for API 1.0v does not need requestid ...
    # REMOVE FOR TESTING  data_summary_userid_value="194e95XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX11a1118"

    ############################################ DANGER SECURTY ############
    ############################################ DANGER SECURTY ############
    ############################################ DANGER SECURTY ############
    ############################################ DANGER SECURTY ############

    with open("config.yml", "w") as file:
        lines = [
            '{\r        "app_id":"66f2XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX98",\r        "app_id_secret":"u258QXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXvP",\r        "tenant_id":"66XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX154"\r}']
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

    ################################################################################ AUTH
    def FUNC_AUTH():
        phantom.debug("DEBUG: Running FUNC_AUTH using dispositoin: " + str(get_incident_1_result_item_0) )
        r = requests.post('https://login.microsoftonline.com/' + tenant_id + '/oauth2/v2.0/token',
                          data={'grant_type': 'client_credentials', 'client_id': app_id, 'client_secret': app_id_secret, 'scope': 'https://graph.microsoft.com/.default'})
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
        # set confirmFlag based on data_disposition_value if not disposition:7 then set to safe else flag as unsafe
                
        if str(get_incident_1_result_item_0) in ['True Positive - Suspicious Activity']:
            confirmFlag = 'confirmCompromised'
        else:
            confirmFlag = 'dismiss'   
        phantom.debug("confirmFlag: " + confirmFlag )
        # headers = {'Authorization': }
        global headers
        headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
        r = requests.post('https://graph.microsoft.com/v1.0/IdentityProtection/riskyUsers/' + confirmFlag , data=json.dumps(
            {'userIds': [data_summary_userid_value]}),
                          headers=headers)

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

        ############################################################ MAIN


    LOADCONFIG()
    #PROXY()
    FUNC_AUTH()

    """
    # examples to grab data from SOAR
    data_summary_requestid_value = container.get("data", {}).get("summary", {}).get("requestId", None)
        data_summary_userid_value = container.get("data", {}).get("summary", {}).get("userId", None)
        data_disposition_value = container.get("data", {}).get("disposition", None)
    """

    phantom.debug("data_summary_userid_value: " + data_summary_userid_value)
    # not needed for API 1.0 phantom.debug("data_summary_requestid_value: " + str(data_summary_requestid_value))
    phantom.debug("tenant_id: " + tenant_id)
    phantom.debug("app_id: " + app_id)
    phantom.debug("app_id_secret: XXXXXXXXXXXXXX" + app_id_secret[-10:])
    phantom.debug("access_token: XXXXXXXXXXXXXX" + access_token[-10:])

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

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    return

