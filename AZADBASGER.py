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

    container_artifact_data = phantom.collect2(container=container, datapath=["artifact:*.data.userId","artifact:*.data.requestId","artifact:*.requestId","artifact:*.id","artifact:*.external_id"])

    container_artifact_header_item_0 = [item[0] for item in container_artifact_data]
    container_artifact_header_item_1 = [item[1] for item in container_artifact_data]
    container_artifact_header_item_2 = [item[2] for item in container_artifact_data]

    parameters = []

    parameters.append({
        "input_1": container_artifact_header_item_0,
        "input_2": container_artifact_header_item_1,
        "input_3": container_artifact_header_item_2,
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

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.custom_function(custom_function="community/debug", parameters=parameters, name="debug_1")

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
