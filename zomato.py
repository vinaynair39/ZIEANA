import requests
import json

headers = {'Api-Key': '8z76ceavpadeka7hrkze6kff'}
r = requests.get('https://api.gettyimages.com/v3/search/images?fields=id,title,thumb,referral_destinations&sort_order=best&phrase=lion',headers=headers)
data = json.loads(r.text)
formatted = json.dumps(data, indent=2)
print(formatted)
print(data['images'][0]['display_sizes'][0]['uri'])
