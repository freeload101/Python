


# Python Scripts

## CS_HIDE.py

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

![enter image description here](https://github.com/freeload101/Python/CS_HIDE/blob/master/CS_HIDE.jpg?raw=true)
