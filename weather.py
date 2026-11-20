import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv('API_KEY')
API_HOST = "https://mk76x9w3kh.re.qweatherapi.com"
# url = f"{API_HOST}/v7/weather/3d"
# params = {'key': API_KEY,'range':'cn'}
# response = requests.get(url, params=params)
# data = response.json()
# with open('./data/city.json2', 'w', encoding='utf-8') as f:
#     json.dump(data, f, ensure_ascii=False, indent=4)

def get_cityID(city_name):
    url = f"{API_HOST}/geo/v2/city/lookup"
    params = {'key': API_KEY,
              'location': city_name,
              'lang': 'zh-hans'}
    response = requests.get(url, params=params)
    data = response.json()
    # print(data)
    if response.status_code == 200 and len(city_name)>0:
        return data['location'][0]['id']
    else:
        print(f'get city name error {response.status_code}')
        return None

def get_weather(cityID):
    url = f"{API_HOST}/v7/weather/3d"
    params = {'key': API_KEY,'location':cityID,'range':'cn'}
    response = requests.get(url, params=params)
    data = response.json()
    # with open('./data/city.json2', 'w', encoding='utf-8') as f:
    #     json.dump(data, f, ensure_ascii=False, indent=4)
    if response.status_code == 200:
        return data
    else:
        print(f'get weather error {response.status_code}')
        return None
if __name__ == '__main__':
    city_name = input('city name: ')
    try:
        cityID = get_cityID(city_name)
        if cityID == None:
            print('city name error')
            exit()
        weather = get_weather(cityID)
        if weather == None:
            print(print("获取天气失败"))
        else:
            for day in weather['daily']:
                print(f"日期{day['fxDate']}")
                print(f"月相{day['moonPhase']}")
                print(f"天气{day['textNight']}")
                print(f"最高温{day['tempMax']}")
                print(f"最低温{day['tempMin']}")
                print(f"风速{day['windSpeedDay']}")
    except Exception as e:
        print(e)
