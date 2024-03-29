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
import dateutil.parser
import pytz



############################################################ FUNCTIONS

def FUNC_BACKUP():
    
    # CREATE DATA TIME VARIABLE
    if pathlib.Path("r_data.json").exists ():
        datetime_var = time.strftime("__%d_%m_%y-%H-%M")    
        print("DEBUG: Backing up r_data.json to: " "r_data.json"+str(datetime_var))
        shutil.move("r_data.json", "r_data.json"+str(datetime_var))
    
def FUNC_AUTH():
    
    ################################################################################ AUTH
    r = requests.post('https://api.crowdstrike.com/oauth2/token', data = {'client_id':VAR_CLIENT_ID,'client_secret':VAR_CLIENT_SECRET},verify=VAR_SSL_FLAG)
    if r.status_code in [201]:
        #print("DEBUG: Status 201 OK!")
        tok_dict = json.loads(r.text)
        global access_token
        access_token = tok_dict["access_token"]
        #print("DEBUG: Access Token is ",access_token)
    else:
        print(r.status_code)
        print(r.url)
        print(r.text)
        print(r.content)
        print("ERROR DID NOT GET 201 STATUS CODE") 


def FUNC_UNHIDE():
    VAR_AIDS_DUPE=sys.argv[2]
    print("DEBUG: Unhiding",VAR_AIDS_DUPE)
    r = requests.request("POST",'https://api.crowdstrike.com/devices/entities/devices-actions/v2?action_name=unhide_host', headers = {'Authorization': 'Bearer ' + access_token,'Content-Type': 'application/json'},json={'ids': [VAR_AIDS_DUPE]},verify=VAR_SSL_FLAG)
    print(r.text)
    sys.exit (1)


def FUNC_SET_STATUS():
    VAR_AIDS_DUPE=sys.argv[2]
    VAR_AIDS_USER=sys.argv[3]
    VAR_AIDS_STATUS=sys.argv[4]
    print("DEBUG: Setting status for ",VAR_AIDS_DUPE)
    r = requests.request("PATCH",'https://api.crowdstrike.com/detects/entities/detects/v2', headers = {'Authorization': 'Bearer ' + access_token,'Content-Type': 'application/json'},json={'ids': [VAR_AIDS_DUPE],"status":VAR_AIDS_STATUS,"assigned_to_uuid":VAR_AIDS_USER},verify=VAR_SSL_FLAG)
    print(r.text)
    
    sys.exit (1)

def FUNC_HIDE1():
    VAR_AIDS_DUPE=sys.argv[2]
    print("DEBUG: Hiding ",VAR_AIDS_DUPE)
    r = requests.request("POST",'https://api.crowdstrike.com/devices/entities/devices-actions/v2?action_name=hide_host', headers = {'Authorization': 'Bearer ' + access_token,'Content-Type': 'application/json'},json={'ids': [VAR_AIDS_DUPE]},verify=VAR_SSL_FLAG)
    print(r.text)
    sys.exit (1)

def list_duplicates(seq):
    seen = set()
    seen_add = seen.add
    # adds all elements it doesn't know yet to seen and all other to seen_twice
    seen_twice = set( x for x in seq if x in seen or seen_add(x) )
    # turn the set into a list (as requested)
    return list( seen_twice )

################################################################################ INIT




if len (sys.argv) <= 1:
    print("""
Usage: python CS_HIDE  -h -t -s -p -status

Normal options:
    
    -h search for dupilcate aids or aids with NULL values and hide them in the UI and API
    -t search for dupilcate aids or aids with NULL values and only show what aids would be hidden
    -u unhide a single aid
    -s hide a single aid
    -p enable proxy support to 127.0.0.1:8080  ( -p SWITCH MUST GO AT THE END )

Output: All host data is stored/backedup in a malformed JSON file r_data.json

Config:

    config.yml should look like this:
    {
            "client_id":"####################################",
            "client_secret":"####################################"
    }


Version:
    *1.0a: Fixed 'Only select up to 100 hosts at a time'

    """)
    sys.exit (1)

for x in sys.argv:
    if x == '-p':
        global HTTP_PROXY
        global HTTPS_PROXY
        print("DEBUG: Setting Proxy to 127.0.0.1:8080")
        os.environ["HTTP_PROXY"] = "http://127.0.0.1:8080"
        os.environ["HTTPS_PROXY"] = "http://127.0.0.1:8080"
        VAR_SSL_FLAG=False
        # supress warnings for ssl
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    if x == '-h':
        VAR_HIDE="True"
    if x == '-t':
        VAR_HIDE="False"
    if x == '-u':
        VAR_HIDE="unhide"
    if x == '-s':
        VAR_HIDE="hide1"
    if x == '-status':
        VAR_HIDE="hide2"
	
	




############################################################ CONFIG

yaml.warnings({'YAMLLoadWarning': False})

Loader=yaml.FullLoader
with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)


VAR_CLIENT_ID=(cfg['client_id'])
VAR_CLIENT_SECRET=(cfg['client_secret'])
 
# CREATE DATA TIME VARIABLE
datetime_var = time.strftime("__%d_%m_%y-%H-%M")

# backup JSON file 
FUNC_BACKUP()



################################################################################ MAIN 
FUNC_BACKUP()
FUNC_AUTH()

if VAR_HIDE == "unhide":
    FUNC_UNHIDE()
if VAR_HIDE == "hide1":
    FUNC_HIDE1()
if VAR_HIDE == "hide2":
    FUNC_SET_STATUS()



################################################################################ GET TOTAL COUNT OF AIDS
r = requests.get('https://api.crowdstrike.com/devices/queries/devices/v1?limit=2&sort=first_seen.desc&offset=0', headers = {'Authorization': 'Bearer ' + access_token},verify=VAR_SSL_FLAG)
tok_dict = json.loads(r.text)
VAR_TOTAL = (tok_dict['meta']['pagination']['total'])

print("DEBUG: Total AIDs ",VAR_TOTAL)

VAR_AID_RUNS_NEEDED=(VAR_TOTAL/5000)

print("DEBUG: Total runs needed for all AIDs ",VAR_AID_RUNS_NEEDED)


VAR_AIDS_ARRAY=[]
VAR_AIDS=[]
VAR_OFFSET_CURRENT=0
count = 0


################################################################################ GET ALL THE AIDS
while count < VAR_AID_RUNS_NEEDED:
    r = requests.get("https://api.crowdstrike.com/devices/queries/devices/v1?limit=5000&sort=first_seen.desc", headers = {'Authorization': 'Bearer ' + access_token}, params = {'offset':VAR_OFFSET_CURRENT},verify=VAR_SSL_FLAG)
    print("DEBUG: Fetching chunks",r.url)
    tok_dict = r.json()
    VAR_AIDS = (tok_dict['resources'])
    VAR_OFFSET_CURRENT += 5000
    count += 1
    # DEBUG set count to += 4 normal is +=1 
    for i in VAR_AIDS:
        VAR_AIDS_ARRAY.append(i)

  


VAR_CHUNKS = [VAR_AIDS_ARRAY[i:i + 500] for i in range(0,len(VAR_AIDS_ARRAY), 500)]

print("DEBUG: Splitting "+str(len(VAR_AIDS_ARRAY))+" AIDS into 500 count ")

VAR_CHUNKS_ALL_LIST=[]

for i in VAR_CHUNKS:
    VAR_CHUNKS_TOTAL= (len(VAR_CHUNKS))
    VAR_CHUNKS_TMP = ""
    for j in i:
        VAR_CHUNKS_TMP += str(j) + "&ids="
    VAR_CHUNKS_ALL_LIST.append(VAR_CHUNKS_TMP[:-5])

VAR_AIDS_DETAIL=[]
VAR_AIDS_DETAIL_LIST=[]

 

for i in VAR_CHUNKS_ALL_LIST:
    r = requests.get("https://api.crowdstrike.com/devices/entities/devices/v1?ids="+str(i), headers = {'Authorization': 'Bearer ' + access_token},verify=VAR_SSL_FLAG)
    r_data = json.loads(r.text)
    print("DEBUG: Fetching",len(VAR_AIDS_DETAIL_LIST),"ids of",len(VAR_AIDS_ARRAY))

    # output to broken json file
    with open('r_data.json', 'a+') as outfile1:
            json.dump(r_data, outfile1, indent=4)
    
    for i in range (len(r_data['resources'])):
        # we had at least one AID without a hostname ... WTF...
        #VAR_CURRENT_HOSTNAME=(r_data.get['resources'])
        ################################################  python "KeyError:" catch #### fix aid missing hostenams using .get

        try:
            VAR_CURRENT_HOSTNAME=(r_data['resources'][i]['hostname'])
        except KeyError:
            print("DEBUG: Missing HOSTNAME for",(r_data['resources'][i]['device_id']))
            VAR_CURRENT_HOSTNAME="NULL"

        try:
            VAR_CURRENT_DEVICE_ID=(r_data['resources'][i]['device_id'])
        except KeyError:
            print("DEBUG: Missing DEVICE_ID for",(r_data['resources'][i]))
            VAR_CURRENT_DEVICE_ID="NULL"


        try:
            VAR_CURRENT_LOCAL_IP=(r_data['resources'][i]['local_ip'])
        except KeyError:
            print("DEBUG: Missing LOCAL_IP for",(r_data['resources'][i]['device_id']))
            VAR_CURRENT_LOCAL_IP="NULL"


        try:
            VAR_CURRENT_SYSTEM_PRODUUCT_NAME=(r_data['resources'][i]['system_product_name'])
        except KeyError:
            print("DEBUG: Missing SYSTEM_PRODUUCT_NAME for",(r_data['resources'][i]['device_id']))
            VAR_CURRENT_SYSTEM_PRODUUCT_NAME="NULL"

        try:
            VAR_CURRENT_MAC_ADDRESS=(r_data['resources'][i]['mac_address'])
        except KeyError:
            print("DEBUG: Missing MAC_ADDRESS for",(r_data['resources'][i]['device_id']))
            VAR_CURRENT_MAC_ADDRESS="NULL"            

        try:
            VAR_CURRENT_LAST_SEEN=(r_data['resources'][i]['last_seen'])
        except KeyError:
            print("DEBUG: Missing LAST_SEEN for",(r_data['resources'][i]['device_id']))
            VAR_CURRENT_LAST_SEEN="NULL"
 

        #print(VAR_CURRENT_HOSTNAME,VAR_CURRENT_DEVICE_ID,VAR_CURRENT_LAST_SEEN)
        VAR_AIDS_DETAIL_LIST.append([VAR_CURRENT_HOSTNAME,VAR_CURRENT_DEVICE_ID,VAR_CURRENT_LOCAL_IP,VAR_CURRENT_SYSTEM_PRODUUCT_NAME,VAR_CURRENT_LAST_SEEN,VAR_CURRENT_MAC_ADDRESS])
 

######################################################### GET DUPE HOSTNAMES 
VAR_AIDS_DETAIL_LIST_HOSTNAMES=[]
VAR_AIDS_DETAIL_LIST_HOSTNAMES_DUPES=[]


for i in range (len(VAR_AIDS_DETAIL_LIST)):
    VAR_AIDS_DETAIL_LIST_HOSTNAMES.append((VAR_AIDS_DETAIL_LIST[i][0]))

VAR_AIDS_DETAIL_LIST_HOSTNAMES_DUPES=(list_duplicates(VAR_AIDS_DETAIL_LIST_HOSTNAMES))


#print("DEBUG: hosts with dupes ",VAR_AIDS_DETAIL_LIST_HOSTNAMES_DUPES)


# rest of this this needs to be cleaned up ... doing a lot of dupe stuff in here

VAR_AIDS_DUPE=[]
VAR_AIDS_NULL=[]
VAR_AIDS_DUPE_ALL=[]
for i in VAR_AIDS_DETAIL_LIST_HOSTNAMES_DUPES:
    count = 0
    for j in VAR_AIDS_DETAIL_LIST:
        if i in j:
            if count == 0:
                count += 1
                #print("DEBUG: Not storing ",i,j)
                VAR_AIDS_DUPE_ALL.append(j)
            else:
                VAR_LASTSEEN=j[4]
                insertion_date = dateutil.parser.parse(VAR_LASTSEEN)
                diffretiation = pytz.utc.localize(datetime.datetime.utcnow()) - insertion_date
                if diffretiation.days>3:
                    #print("DEBUG: Storing ",i,j)
                    VAR_AIDS_DUPE.append(j[1])
                    VAR_AIDS_DUPE_ALL.append(j)

                #else:
                    #print("DEBUG: Not storing due to recent last_seen value",i,j)





if VAR_HIDE == "False":
    print("DEBUG: Showing dupes only\n")
    print("DEBUG: Hostname,Aid,Last Seen,Mac Address")
    for i in VAR_AIDS_DUPE_ALL:
        print(i)
    for k in VAR_AIDS_DETAIL_LIST:
        if 'NULL' in k:
            VAR_AIDS_NULL.append(k[1])
    if len(VAR_AIDS_NULL) == 0 or len(VAR_AIDS_DUPE) == 0:
        print("No aids with NULL or old duplicate host entries found")
    else:
        print("DEBUG: Showing",len(VAR_AIDS_NULL),"aids with NULL entries")
        print(VAR_AIDS_NULL)
        print("DEBUG: Showing",len(VAR_AIDS_DUPE),"dupe aids with old last_seen entries")
        print(VAR_AIDS_DUPE)
     


if VAR_HIDE == "True":
    print("DEBUG: Hostname,Aid,Last Seen,Mac Address")
    for i in VAR_AIDS_DUPE_ALL:
        print(i)
    for k in VAR_AIDS_DETAIL_LIST:
        if 'NULL' in k:
            VAR_AIDS_NULL.append(k[1])
    if len(VAR_AIDS_NULL) == 0 and len(VAR_AIDS_DUPE) == 0:
        print("No aids with NULL or old duplicate host entries found")
    else:
        print("DEBUG: Hiding",len(VAR_AIDS_NULL),"aids with NULL entries")
        print(VAR_AIDS_NULL)
        print("DEBUG: Hiding",len(VAR_AIDS_DUPE),"dupe aids with old last_seen entries")
        print(VAR_AIDS_DUPE)

        # split up VAR_AIDS_NULL and VAR_AIDS_DUPE into 100 size chunks can only do 100 at a time
        VAR_AIDS_DUPE_NULL=[]
        VAR_AIDS_DUPE_NULL=VAR_AIDS_NULL
        VAR_AIDS_DUPE_NULL.extend(VAR_AIDS_DUPE)
        
        VAR_AIDS_DUPE_NULL_SPLIT = [VAR_AIDS_DUPE_NULL[i:i + 100] for i in range(0,len(VAR_AIDS_DUPE_NULL), 100)]
        print("DEBUG: Splitting "+str(len(VAR_AIDS_DUPE_NULL_SPLIT))+" AIDS into 100 count ")
        input("Press Enter to continue...")
        print("Please wait may take some time")
        for i in VAR_AIDS_DUPE_NULL_SPLIT:
            #print("DEBUG:",i)
            r = requests.request("POST",'https://api.crowdstrike.com/devices/entities/devices-actions/v2?action_name=hide_host', headers = {'Authorization': 'Bearer ' + access_token,'Content-Type': 'application/json'},json={'ids': i},verify=VAR_SSL_FLAG)
            print(r.text)
                         
sys.exit (1)

