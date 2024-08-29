import sys 
import json 
import requests
from requests.models import PreparedRequest
import pandas as pd 
import pathlib
import pyodbc as pdb
import datetime

#https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?product=hourly_height&application=NOS.COOPS.TAC.WL&begin_date=20230101&end_date=20240101&datum=IGLD&station=9075002&time_zone=LST&units=english&format=json
BASE_URL = "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?"
FORMAT = "json"
TIME_ZONE = 'LST'
APPLICATION = 'HurtubiseJ'
DATUM = "IGLD"
UNITS = "english"

stations_json_path = pathlib.Path('C:\\Users\\jhurt\\OneDrive\\Desktop\\Great_Lakes_Water_Tracker\\API_Pulls\\stations.json')

def get_station_recent_data(stations):
    stations_id_list = stationId_by_region(load_stations_json(stations_json_path), stations)
    for pair in stations_id_list: 
        df = pull_recent_data_from_Id(pair[1])
        df_to_db(pair[1], df)
        print(f"Added {pair[1]} data to DB.")


def stationId_by_region(station_json_content, selected_region):
    list = []
    for region in station_json_content['Great Lakes Regions']:
        if region['Region'] == selected_region or region['Region'] in selected_region:
            for station in region['Stations']:
                list.append([station['Location'], station['Id']])
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
    try:
        cursor.execute(SQL, params)
        cursor.commit()
    except:
        print("Failed to execute stored procedure 'StoreTime'.")
        print(params)

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

def ensure_StationsId_helper(stations):
    stations_pairs = stationId_by_region(load_stations_json(stations_json_path), stations)
    for pair in stations_pairs:
        print(f"In ensure for {pair}")
        params = (
            pair[0], pair[1]
        )
        SQL = """
            EXEC ModifyStationsIdTable 
                @StationName = ?, @StationId = ?
        """
        try:
            cursor.execute(SQL, params)
            cursor.commit()
        except:
            print(f"Failed to ensure helper table for {params}")

def exec_select_range(stationId, startDate, endDate):
    params = (
        stationId, startDate, endDate
    )

    SQL = """
        EXEC dbo.SelectDateRange ?, ?, ?
    """
    cursor.execute(SQL, params)
    response = cursor.fetchall()
    return response if response else None

def main():
    # stations = ["Detroit River", "Lake Erie", "Lake Huron", "Lake Michigan", "Lake Ontario", "Lake St. Clair", "Lake Superior", "Niagara River", "St. Clair River", "St. Lawrence River", "St. Marys River"]
    # ensure_StationsId_helper(stations)
    # get_station_recent_data(stations)
    exec_select_range('9034052', '2024-08-26 00:00:00.000', '2024-08-26 00:54:00.000')

if __name__ == '__main__':
    main()