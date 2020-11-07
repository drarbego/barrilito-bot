import requests


BICI_STATIONS_URL = 'https://guadalajara-mx.publicbikesystem.net/ube/gbfs/v1/en/station_status'
OIL_PRICES_URL = 'https://datasource.kapsarc.org/api/records/1.0/search/?dataset=opec-crude-oil-price&q=&rows=1&facet=date&refine.date=2020'


class SemanticAnalyzer:
    def get_response(self, message_content):
        if "oil" in message_content:
            return check_oil()
        if "bicis" in message_content:
            return check_bicis()

        return "Estoy en mantenimiento, disculpe."

    def check_oil():
        response = requests.get(
            OIL_PRICES_URL,
        )

        json_response = response.json()

        results = json_response.get('records', [])
        
        total = 0
        if results:
            total = results[0].get('fields', {}).get('value', 0)

        return 'El precio del barril al día de hoy es de {total} USD'.format(total=total)


    def check_bicis(station_id='192'):
        response = requests.get(
            BICI_STATIONS_URL,
        )

        json_response = response.json()
        stations = json_response.get('data', {}).get('stations', [])
        station_count = 0

        found_station = {}
        for station in stations:
            if station.get('station_id') == station_id:
                found_station = station
                break

        return 'Hay {bikes}/{docks} bici(s) disponible(s)'.format(
            bikes=str(found_station.get('num_bikes_available')),
            docks=str(found_station.get('num_docks_available')),
        )
