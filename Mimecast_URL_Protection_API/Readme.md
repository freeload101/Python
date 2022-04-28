ZeroFox CSV REPORT convert:

`cat 2mos.csv | awk '{gsub("\r","\n"); print}' |sed 's/.*hxxp/hxxp/g'| grep -E "(hxxp)"  | sed 's/,.*//g' |sort -u| grep -vEa "(twitter|linkedin)" | sed -r -e 's/hxx([p|ps])/htt\1/g' > URLS.txt`


Usage:

1) create URLS.txt file 
2) create config.yml should look like this. appid is c6903e5f-1e1b-420d-93be-9a670978e809 for me at least YMMV  :



      {
  
      "USERNAME":"bob@company.com",
  
      "PASSWORD":"yerpasswordhere",
   
      "APPID":"c6903e5f-1e1b-420d-93be-9a670978e809"
      }


3) run:

Mimecast_URL_Protection_API.exe -m



![image](https://user-images.githubusercontent.com/4307863/132733359-042c0ed6-40c8-470f-92f7-e09303fe390f.png)
