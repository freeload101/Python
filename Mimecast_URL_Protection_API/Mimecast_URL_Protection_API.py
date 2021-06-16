
# importing the multiprocessing module
import multiprocessing

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

def OUTPUT(message):
    print(message)
    logging.warning(message)
    sys.stdout.flush()



def FUNC_MIMECASTGO():

    
 

    with requests.Session() as s:
        s.get('https://login-us.mimecast.com/u/rest/api/login/login',verify=VAR_SSL_FLAG)
        OUTPUT(datetime_var+",[+]INFO: Auth to get sid cookie,")
        r1 = s.post('https://login-us.mimecast.com/u/rest/api/login/login', json={
        "data":[{
            "username":VAR_CLIENT_USERNAME,
            "password":VAR_CLIENT_PASSWORD,
            "authenticationType":"Basic-Cloud",
            "extendOnValidate":"true",
            "tokenType":"key"}]
            },
        headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
        'Content-Type': 'application/json;charset=utf-8',
        'X-Mc-App-Id': VAR_CLIENT_APPID
    },verify=VAR_SSL_FLAG)
    OUTPUT(s.cookies['mc-you'])
    OUTPUT(s.cookies['sid'])
    
    OUTPUT(datetime_var+",[+]INFO: Loading URLS.txt")
    f = open("URLS.txt", "r")
    for url in f:
            url = url.replace('\n', ' ').replace('\r', '')
            from threading import Thread
            Thread(target=SCAN,args=(s.cookies['sid'],s.cookies['mc-you'],url)).start()
            time.sleep(1)


def SCAN(sid,mcyou,url):
    with requests.Session() as s:
        s.cookies.set("mc-you", mcyou)
        OUTPUT(datetime_var+",[+]INFO: Checking,"+url)
        r1 = s.post('https://login-us.mimecast.com/u/proxy/api/ttp/url/detailed-scan-url', json={
        "data":[{"url":url}]},
        headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
        'Content-Type': 'application/json;charset=utf-8',
        'X-Mc-App-Id': VAR_CLIENT_APPID,
        'sid': sid
        },verify=VAR_SSL_FLAG)
        # dump the output buffer
        sys.stdout.flush()
        R1CONTENT = r1.content.decode('utf-8')
        R1CONTENT = R1CONTENT.replace('\n', ' ').replace('\r', '')
        OUTPUT(datetime_var+",[+]INFO: Complete,"+url+","+str(r1.content))

        #print(str(r1.content)
        
         # match
         # "relaxed":"Clean","moderate":"Clean","aggressive":"Clean"
 

################################################################################ INIT




# CREATE DATA TIME VARIABLE
datetime_var = time.strftime("%Y-%m-%d,%H:%M:%S")

# setup log file
logging.basicConfig(filename=time.strftime("%Y_%m_%d_%H_%M")+".log", filemode='w', format='%(name)s - %(levelname)s - %(message)s')





# load up yaml 
yaml.warnings({'YAMLLoadWarning': False})

Loader=yaml.FullLoader
with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
 

VAR_CLIENT_USERNAME=(cfg['USERNAME'])
VAR_CLIENT_PASSWORD=(cfg['PASSWORD'])
VAR_CLIENT_APPID=(cfg['APPID'])



 

################################################################################ MAIN 
#FUNC_BACKUP()
#FUNC_AUTH()

 


if len (sys.argv) <= 1:
    print("""
Usage:  

Normal options:
    
    -m read URLS.txt and scan with URL Protection
    -p proxy support for use with burpsuite for debugging on localhost:8080

Config:

    config.yml should look like this:
{
        "USERNAME":"bob@company.com",
        "PASSWORD":"yerpasswordhere",
        "APPID":"yerappid"
}


Version:
    *1.0a: Logs and output in same function

    """)
    sys.exit (1)

for x in sys.argv:
    if x == '-p':
        global HTTP_PROXY
        global HTTPS_PROXY
        print(datetime_var+",[+]INFO: Setting Proxy to 127.0.0.1:8080")
        os.environ["HTTP_PROXY"] = "http://127.0.0.1:8080"
        os.environ["HTTPS_PROXY"] = "http://127.0.0.1:8080"
        VAR_SSL_FLAG=False
        # supress warnings for ssl
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    if x == '-m':
        FUNC_MIMECASTGO()
 


 


   # if VAR_HIDE == "unhide":
   #     FUNC_UNHIDE()
   # if VAR_HIDE == "hide1":
   #     FUNC_HIDE1()
   # if VAR_HIDE == "hide2":
   #     FUNC_SET_STATUS()



                         
sys.exit (1)
