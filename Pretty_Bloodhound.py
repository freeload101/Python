import json
import codecs
import sys

with open(str(sys.argv[1]), encoding='utf-8-sig') as json_file:
	data = json.load(json_file)
print(json.dumps(data, indent=4),file=open("Pretty_"+sys.argv[1], "w"))
