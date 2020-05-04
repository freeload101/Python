import time, os, requests, pickle, json
from time import sleep
# Fill your credentials, run the script, see results.json

# for regex to repalce URLs with HTML
import re

# Credit: Dmitry Neyasov  dmitry.neyasov@gmail.com  https://www.upwork.com/o/profiles/users/~01e45e5fb897bbe25a/


login='freeload101@yahoo.com'
password='bXXXXXXXXXXXXXXXXXXK'
hours = 24




def getcontent(res):
	return json.loads(res.content.decode())

def main():
	
	#unix time past N hours to grab posts since
	since = time.time() - hours * 3600
	ss = requests.Session()	
	api = 'https://mm.netsecfocus.com/api/v4/'
	
	#get token
	res = ss.post(api + 'users/login', json={'login_id' : login, 'password' : password})
	if res.status_code != 200:
		print(res.status_code)
		return
	
	token = res.raw.headers['token']
	ss.headers['Authorization'] =  'Bearer %s' % token

	#get user
	user = getcontent(res)
	
	#get user's team
	res = ss.get(api + 'users/%s/teams' % user['id'])
	teams = getcontent(res)

	#get user's channels
	res = ss.get(api + 'users/%s/teams/%s/channels' % (user['id'], teams[0]['id']))
	channels = getcontent(res)
	
	data = []
	posts_count = 0

	#get posts
	for ch in channels:
		res = ss.get(api + 'channels/%s/posts' % ch['id'], json={'since' : since})
		posts = getcontent(res)
		posts_count += len(posts)
		for k, v in posts['posts'].items():
			if v['message'].find('http') != -1:
				data.append(v)
				#print("<br>",v['message'])
				#print(v['message'])
				newstring = re.sub('(.*)((http|https)://[a-zA-Z0-9./?=_-]*)', '<a href=\"\\g<2>\">\\g<2></a>', v['message'])
				
				update_at = v['update_at']/1000
				#print("DEBUG:",update_at , since)
				#sleep(.25)
				if update_at > since:
					print("<br>",newstring,"<br>")
					sleep(1)

	with open('result.json', 'w') as f: 
		json.dump(data, f, sort_keys=True, indent=4)

	#print('Result: %d posts with links out of %d posts (from %d channels)' % (len(data), posts_count, len(channels)))
	#print('See result.json')
	#print('Done')
	return

main()
