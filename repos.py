import requests
import json
API_KEY = '34d02f1ed81f4ada8205ba1a11019398'
API_HOST = "https://mk76x9w3kh.re.qweatherapi.com"
url = f"{API_HOST}/geo/v2/city/top"
params = {'key': API_KEY,
          'range':'cn',

          }
response = requests.get(url, params=params,headers={'User-Agent': 'Mozilla/5.0'})
print(response.status_code)
data = response.json()
print(data)
with open('./data/city.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
