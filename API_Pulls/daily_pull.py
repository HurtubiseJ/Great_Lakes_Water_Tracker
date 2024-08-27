#File is run by task scheduler every day

import info_pull

if __name__ == '__main__':
    #Stations to pull data for
    stations = ["Detroit River", "Lake Erie", "Lake Huron", "Lake Michigan", "Lake Ontario", "Lake St. Clair", "Lake Superior", "Niagara River", "St. Clair River", "St. Lawrence River", "St. Marys River"]
    #Ensure helper table is built 
    info_pull.ensure_StationsId_helper(stations)
    #pull data from api to DB
    info_pull.get_station_recent_data(stations)