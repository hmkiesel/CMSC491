import requests
import json

ACCESS_TOKEN = 'your_key_here'
fb_url = 'https://graph.facebook.com/me'
fields = 'id,name'
url = '%s?fields=%s&access_token=%s'% (fb_url, fields, ACCESS_TOKEN,)
results = requests.get(url).json()
print json.dumps(results, indent = 1)