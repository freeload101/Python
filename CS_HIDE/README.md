


# Python Scripts

## CS_HIDE.py

## Also check out CS_BADGER https://github.com/freeload101/SCRIPTS/tree/master/Bash/CS_BADGER 

This script will find duplicate host names and remove any old or null duplicate aids or 'device_ids'
Creates complete broken JSON output of all aid info.

>Usage: python CS_HIDE -h -t -s -p
> 
> Normal options:
> 
>
>-h search for dupilcate aids or aids with NULL values and hide them in the UI and API
>
>-t search for dupilcate aids or aids with NULL values and only show what aids would be hidden
>
>-u unhide a single aid
>
>-s hide a single aid
>
>-p enable proxy support to 127.0.0.1:8080 ( -p SWITCH MUST GO AT THE END )
>
>-status Detect_ID User_ID Status
> Example : ( -status ldt:6346acb9431b4f5959f7f36ac1742965:197568642580 "3fbed8da-7445-4278-afbc-085868267968" ignored )
>Output: 
>
>All host data is stored/backedup in a malformed JSON file r_data.json
>
>Config:
> config.yml should look like this:
>
>{
>
>"client_id":"####################################",
>
>"client_secret":"####################################"
>
>}

![enter image description here](https://github.com/freeload101/Python/blob/master/CS_HIDE/CS_HIDE.jpg?raw=true)


> -status help
>To get your idt:#:# use the url of a detection example :

>https://falcon.crowdstrike.com/activity/detections/detail/6346acb9431b4f5959f7f36ac1742965/197568642580

>to get the user ID use Chrome F12 then click network tab and then the response tab for a request that includes the account ID you searched for:

![enter image description here](https://github.com/freeload101/Python/blob/master/CS_HIDE/CS_USER.jpg?raw=true)


