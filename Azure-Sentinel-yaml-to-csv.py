# git clone https://github.com/Azure/Azure-Sentinel.git
# mkdir EXPORT
# mv Detections  .\EXPORT\
# mv "Hunting Queries" .\EXPORT\
# mv "Exploration Queries" .\EXPORT\
# cd .\EXPORT\
# find . -type f -iname "*.y*" -exec python 1.py '{}' \;


# for time/sleep
import time

# to convert yaml
import yaml 

# for command line args
import sys

#for logging
import logging

# regex
import re

# for command line args
import sys

# sys.argv[0]

with open(sys.argv[1], 'r') as f:
    doc = yaml.load(f, Loader=yaml.FullLoader) # also, yaml.SafeLoader

print ("FileName: "+sys.argv[1],"\r")




#print(sys.argv[1]+","+str(doc["id"]))
OUTPUT1 = (sys.argv[1]+"FS2FS1FS2"
+str(doc.get('id', 'NULL'))+"FS2FS1FS2"
+str(doc.get('Id', 'NULL'))+"FS2FS1FS2"
+str(doc.get('name', 'NULL'))+"FS2FS1FS2"
+str(doc.get('DisplayName', 'NULL'))+"FS2FS1FS2"
+str(doc.get('description', 'NULL'))+"FS2FS1FS2"
+str(doc.get('Description', 'NULL'))+"FS2FS1FS2"
+str(doc.get('severity', 'NULL'))+"FS2FS1FS2"
+str(doc.get('tactics', 'NULL'))+"FS2FS1FS2"
# case sensitivie inconsistancy in key names
+str(doc.get('Tactics', 'NULL'))+"FS2FS1FS2"
+str(doc.get('relevantTechniques', 'NULL'))+"FS2FS1FS2"
+str(doc.get('query', 'NULL'))+"FS2FS1FS2"
)

#R1CONTENT = r1.content.decode('utf-8')
#R1CONTENT = R1CONTENT.replace('\n', ' ').replace('\r', '')

OUTPUT1 = str(OUTPUT1)

OUTPUT1 = re.sub('"' , '""', OUTPUT1)
OUTPUT1 = re.sub('FS1' , ',', OUTPUT1)
OUTPUT1 = re.sub('FS2' , '"', OUTPUT1)

OUTPUT1 = re.sub('^' , '"', OUTPUT1)
OUTPUT1 = re.sub('$' , '"\r', OUTPUT1)



print(OUTPUT1)
#time.sleep(1)
