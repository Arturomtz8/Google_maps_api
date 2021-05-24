import requests
from urllib.parse import urlencode
import pandas as pd
import os
#Create a dictionary to save the lat and long
lat_long = dict()

#Use the personal API key from google maps to connect to the API
api_key = os.environ.get('GOOGLE_MAPS_PASS')

#Read the excel where I have info about the stores
df = pd.read_excel('Husqvarna_stores.xlsx')
df["full"] = df["NOMBRE"] + " postal code " + df["CODIGO"].astype(str)
values = [x for x in df['full']]

#Iterate over the address and save the lat and long in the dict lat_long
for x in values:
    data_type = 'json'
    endpoint = f"https://maps.googleapis.com/maps/api/geocode/{data_type}"
    params = {"address": x, "region": "es", "key": api_key}

    url_params = urlencode(params)

    url = f"{endpoint}?{url_params}"
    r = requests.get(url)
    if r.status_code not in range(200, 299):
        print('Not found')
    # Set a flag to catch errors
    try:
        lat_long[x] = r.json()['results'][0]['geometry']['location']['lat'], r.json()['results'][0]['geometry']['location']['lng']
    except:
        lat_long[x] = {'error': x}
        continue

df = pd.DataFrame(list(lat_long.items()), columns=['Adress', 'Lat & Long'])

df.to_excel('Husqvarna_coordinates.xlsx', encoding="utf_8_sig", index=False)