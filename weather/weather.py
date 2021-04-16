import http.client
import json

conn = http.client.HTTPSConnection("community-open-weather-map.p.rapidapi.com")

headers = {
    'x-rapidapi-key': WEATHER_API_KEY, 
    'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com"
    }

forecast_days = 17 
# 17 is the max into the future we can look at 

# requesting by city 
# city = "boston"
# req_path =  "/forecast/daily?q=" + city + "%2Cus&cnt=" + str(forecast_days) + "&units=imperial"

# coordinates for boston, ma 
lat = 42.361145
lon = -71.057083

req_path = "/forecast/daily?lat=" + str(lat) + "&lon=" + str(lon) + "&cnt=" + str(forecast_days) + "&units=imperial"

conn.request("GET", req_path, headers=headers)

res = conn.getresponse()
data = res.read()

w_json = data.decode('utf-8')
# print(w_json)

data = json.loads(w_json)
entries = json.dumps(data, indent=4)
print(entries)

for i in range(forecast_days):
    print(i+1, " day(s) into the future: ")
    print("     ", data["list"][i]["temp"]["day"], " degrees F and", data["list"][i]["weather"][0]["description"])

out = open("weather\wforecast.json", "w") 
json.dump(data, out, indent = 4) 
out.close() 

