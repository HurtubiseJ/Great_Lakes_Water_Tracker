import sys 
import json 
import requests
from requests.models import PreparedRequest
import pandas as pd 
import pathlib

#https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?product=hourly_height&application=NOS.COOPS.TAC.WL&begin_date=20230101&end_date=20240101&datum=IGLD&station=9075002&time_zone=LST&units=english&format=json
BASE_URL = "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?"
FORMAT = 'json'
TIME_ZONE = 'LST'
APPLICATION = 'hurtubisej'
DATUM = 'IGLD'

stations_json_path = pathlib.Path('C:\\Users\\jhurt\\OneDrive\\Desktop\\Great_Lakes_Water_Tracker\\stations.json')

def get_recent_data(station='all'):
    response = requests.get('https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?product=hourly_height&application=NOS.COOPS.TAC.WL&begin_date=20230101&end_date=20240101&datum=IGLD&station=9075002&time_zone=LST&units=english&format=json')
    return response

def stationId_by_region(station_json_content, selected_region):
    list = []
    for region in station_json_content['Great Lakes Regions']:
        if region['Region'] == selected_region:
            for station in region['Stations']:
                list.append({station['Location']: station['Id']})
    return list

def load_stations_json(path):
    try:
        with open(path) as file:
            return json.loads(file.read())
    except json.JSONDecodeError as e:
        print(f'Could not Load stations.json file: {e}')

def recent_data_params(Id):
    params = {
        "date":"today",
        "product":"water_level",
        "station":f"{Id}",
        "datum":"IGLD",
        "units":"english",
        "time_zone":"lst",
        "format":"json",
        "application":"HurtubiseJ"
    }
    return params

def response_to_df(response):
    try:
        return pd.DataFrame(response.json()['data'])
    except:
        print("Failed to convert response to DataFrame.")

#Returns dataframe of today's water level data at given stationId
def pull_recent_data_from_Id(Id):
    req = PreparedRequest()
    req.prepare_url(BASE_URL, recent_data_params(Id))
    try:
        response = requests.get(req.url)
        return response_to_df(response)
    except:
        print(f"Failed to pull recent data for stationId: {Id}")

def main():
    df = pull_recent_data_from_Id("9044030")
    print(df)
    
if __name__ == '__main__':
    main()