import http.client
import json
from dotenv import dotenv_values
from pathlib import Path

# POTENTIALLY INSECURE!!!
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

config = dotenv_values('.env')
conn = http.client.HTTPSConnection("community-open-weather-map.p.rapidapi.com")

headers = {
    'x-rapidapi-key': config['WEATHER_API_KEY'], 
    'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com"
    } 

# requesting by city 
# city = "boston"
# req_path =  "/forecast/daily?q=" + city + "%2Cus&cnt=" + str(forecast_days) + "&units=imperial"


# coordinates for boston, ma 
#lat = 42.361145
#lon = -71.057083

def get_weather(lat:float, lon:float):

    if not isinstance(lat, float):
        lat = float(lat)
    if not isinstance(lon, float):
        lat = float(lon)

    #assert(type(lat) == float)
    #assert(type(lon) == float)

    forecast_days = 17 
    # 17 is the max into the future we can look at

    req_path = "/forecast/daily?lat=" + str(lat) + "&lon=" + str(lon) + "&cnt=" + str(forecast_days) + "&units=imperial"

    conn.request("GET", req_path, headers=headers)

    res = conn.getresponse()
    data = res.read()

    w_json = data.decode('utf-8')
    # print(w_json)

    data = json.loads(w_json)
    #if 'cod' in data and data['cod'] == "400" or 'message' in data and data['message'] == "You have exceeded the rate limit per minute for your plan, BASIC, by the API provider":
    #    return []
    entries = json.dumps(data, indent=4)
    # print(entries)

    out = open(Path('weather') / 'wforecast.json', "w") 
    json.dump(data, out, indent = 4) 
    out.close() 

    forecast = []
    for i in range(forecast_days):
        days = str(i+1) + " day(s) into the future: "
        # print(data)
        conditions = str(data["list"][i]["temp"]["day"]) + " degrees F and " + str(data["list"][i]["weather"][0]["description"])
        forecast += [[days, conditions]]
    # print(forecast[3])
    res = forecast
    
    # weathertypes = ['rain and snow', 'snow' , 'light rain' , 'clear' , 'scattered clouds' , 'heavy rain', 'moderate rain', 'overcast clouds', 'broken clouds']
    # return [{"temperature": item[1].split(' ')[0], "weather": [t for t in weathertypes if t in item[1]][0]} for item in res]
    return [{"temperature": item[1].split(' ')[0], "weather": item[1][item[1].index('and') + 4:]} for item in res]

# print(get_weather(47, -75))
# for lat in range(-50, 50):
#     for lon in range(-50, 50):
#         try:
#             get_weather(lat, lon)
#         except Exception as e:
#             print("bad lat", e, lat, lon)
