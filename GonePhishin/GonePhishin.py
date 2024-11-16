#!/usr/bin/env python


'''
TODO:
* config file for spider and ajax spider filetypes ? spider settings / proxy / 
* blacklist https://github.com/zaproxy/zap-api-python/blob/master/src/examples/zap_example_api_script.py contextExcludeURL 
* get list of binary file types mht pdf ... 

# pip install python-owasp-zap-v2.4
# https://www.zaproxy.org/docs/api/#using-ajax-spider

# To start the Spider scan (Response: Scan ID). Modify the API Key and URL to suite the target
$ curl "http://localhost:8080/JSON/spider/action/scan/?apikey=xxxxxxxxxxxx&url=https://public-firing-range.appspot.com&contextName=&recurse="

# To view the scan status/ percentage of work done
$ curl "http://localhost:8080/JSON/spider/view/status/?apikey=<ZAP_API_KEY>&scanId=<SCAN_ID>"

# To view the scan results
$ curl "http://localhost:8080/JSON/spider/view/results/?apikey=xxxxxxxxxxxx&scanId=<SCAN_ID>"

# To stop the scanning
$ curl "http://localhost:8080/JSON/spider/action/stop/?apikey=<ZAP_API_KEY>&scanId=<SCAN_ID>"
# To pause the scanning
$ curl "http://localhost:8080/JSON/spider/action/pause/?apikey=<ZAP_API_KEY>&scanId=<SCAN_ID>"
# To resume the scanning
$ curl "http://localhost:8080/JSON/spider/action/resume/?apikey=<ZAP_API_KEY>&scanId=<SCAN_ID>"


https://github.com/zaproxy/zap-api-docs/blob/master/source/includes/explore.md

https://groups.google.com/forum/#!topic/zaproxy-users/cdvEo7G9Qlo

https://github.com/alex-leonhardt/zapy/blob/master/zapy.py

https://github.com/zaproxy/zap-api-python/blob/master/src/examples/zap_example_api_script.py

# command line stuff 
https://github.com/bertjan/zap-cmdline

# scope / context stuff
https://groups.google.com/forum/#!topic/zaproxy-users/3qnqURb9Gq4


'''
import time
from zapv2 import ZAPv2

# to set splider settings setOptionMaxDepth
import requests

############################################################################### some needed config .. like broswer and browser path ..stuff that's not def for ZAP ui ... ?

# subprocess.Popen(['zap.sh','-daemon','-config','api.disablekey=true','-config','ajaxSpider.browserId='+browser,'-config','selenium.phantomJsBinary=' + phantomJSPath])
browser='phantomjs'








# The URL of the application to be tested
target = 'https://drive.google.com/drive/folders/1-xxxxxxxxxxxxxxxx'

#target = 'https://random-ize.com/random-website/'
#target = 'https://public-firing-range.appspot.com'
# target = 'http://176.126.84.32/stuff/DELETE/'
#target = 'http://176.126.84.32/stuff/G1/BINS/FILEUTILS/'


# Change to match the API key set in ZAP, or use None if the API key is disabled
apiKey = '46ojgm6978e7656thq574obdts'

# By default ZAP API client will connect to port 8080
zap = ZAPv2(apikey=apiKey)
# Use the line below if ZAP is not listening on port 8080, for example, if listening on port 8090
# zap = ZAPv2(apikey=apikey, proxies={'http': 'http://127.0.0.1:8090', 'https': 'http://127.0.0.1:8090'})


# does nothing ... contextName= "Default Context"
  
zap.context.set_context_in_scope("Default Context", True)


zap.core.access_url(url=target, followredirects=True, apikey=apiKey)
print(zap.context.include_in_context("Default Context","https://.*", apiKey))
print(zap.context.include_in_context("Default Context","http://.*", apiKey))


################################################################################ NORMAL SPIDER  ##################################


'''
zap.spider.scan(contextname="Default Context")


zap.spider.set_option_max_depth(3, apikey=apiKey)
zap.spider.set_option_thread_count(10, apikey=apiKey)
zap.spider.set_option_max_duration(1, apikey=apiKey)
#optionThreadCount
# optionMaxDuration



print('Spidering target {}'.format(target))
# The scan returns a scan id to support concurrent scanning
scanID = zap.spider.scan(target, "false")
while int(zap.spider.status(scanID)) < 100:
    # Poll the status until it completes
    print('Spider progress %: {}'.format(zap.spider.status(scanID)))
    time.sleep(1)

print('Spider has completed!')
# Prints the URLs the spider has crawled
print('\n'.join(map(str, zap.spider.results(scanID))))
# If required post process the spider results
'''

################################################################################ AJAX ##################################



zap.ajaxSpider.set_option_max_crawl_depth(2, apikey=apiKey)
zap.ajaxSpider.set_option_max_crawl_states(0, apikey=apiKey)
zap.ajaxSpider.set_option_max_duration(999, apikey=apiKey)
zap.ajaxSpider.set_option_number_of_browsers(8, apikey=apiKey)
 
 

print('Ajax Spider target {}'.format(target))
scanID = zap.ajaxSpider.scan(target,contextname="Default Context")

# Loop until the ajax spider has finished or the timeout has exceeded
while zap.ajaxSpider.status == 'running':
    print('Ajax Spider status ' + zap.ajaxSpider.status ," ", zap.ajaxSpider.number_of_results,"Results")
    time.sleep(2)

print('Ajax Spider completed')
# show responce info 
ajaxResults = zap.ajaxSpider.results(start=0, count=99999)
# print(*ajaxResults, sep='\n')

# show all urls basicly this is what we need maybe use ajaxResults to peek into file types to make sure they are reall what they say they are ...
print('zap.ajaxSpider.full_results #####################################################################################')
print(zap.ajaxSpider.full_results)
print(len(ajaxResults),"Results total")

 
