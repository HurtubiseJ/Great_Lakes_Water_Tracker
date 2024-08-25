import sys 
import json 
import requests
from requests.models import PreparedRequest
import pandas as pd 
import pathlib
import pyodbc as pdb

#https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?product=hourly_height&application=NOS.COOPS.TAC.WL&begin_date=20230101&end_date=20240101&datum=IGLD&station=9075002&time_zone=LST&units=english&format=json
BASE_URL = "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?"
FORMAT = "json"
TIME_ZONE = 'LST'
APPLICATION = 'HurtubiseJ'
DATUM = "IGLD"
UNITS = "english"

stations_json_path = pathlib.Path('C:\\Users\\jhurt\\OneDrive\\Desktop\\Great_Lakes_Water_Tracker\\stations.json')

def get_recent_data(station='all'):
    pass 

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

def create_DB_cursor():
    try:
        conn = pdb.connect(CONNECTION_STRING)
        cursor = conn.cursor()
        print("Database connection and cursor successfully created.")
        return conn, cursor
    except pdb.Error as e:
        print(f"Failed to connect to database: {e}")
        return None, None

def call_procedure_StoreTime(StationId, Date, V, S, F, Q):
    params = (
        StationId, Date, V, S, F, Q
    )
    SQL = """
        EXEC StoreTime
            @StationId = ?, @Date = ?, @V = ?, @S = ?, @F = ?, @Q = ?
    """
    # try:
    print(params)
    cursor.execute(SQL, params)
    cursor.commit()
    # except:
    #     print("Failed to execute stored procedure 'StoreTime'.")
    #     print(params)

def recent_data_params(Id):
    params = {
        "date":"today",
        "product":"water_level",
        "station":f"{Id}",
        "datum":f"{DATUM}",
        "units":f"{UNITS}",
        "time_zone":"lst",
        "format":f"{FORMAT}",
        "application":f"{APPLICATION}"
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

CONNECTION_STRING = ("DRIVER={SQL Server};""SERVER=DESKTOP-7H6LSQ4;""DATABASE=GreatLakesWaterLevels;""TrustedServerConnection=Yes;")
conn, cursor = None, None
conn, cursor = create_DB_cursor()

def df_to_db(StationId, df):
    for index, row in df.iterrows():
        call_procedure_StoreTime(StationId, row['t'], row['v'], row['s'], row['f'], row['q'])

def main():
    df = pull_recent_data_from_Id("9044030")
    StationId = "9044030"
    # print(df)
    df_to_db(StationId, df)

if __name__ == '__main__':
    main()