import json
import io
import requests
from os import path
from uber_rides.session import Session
from uber_rides.client import UberRidesClient

class Uber:
    class __Uber:
        def __init__(self):
            self.locations_json_path = \
            path.abspath(path.join(path.dirname(__file__), "locations.json"))
            self.importJSON()

        def importJSON(self):
            try:
                with open(self.locations_json_path, 'r') as locations_json:
                    self.locations_dict = json.load(locations_json)
            except IOError:
                self.locations_dict = {}
                self.locations_dict['locations'] = {}
                with open(self.locations_json_path, 'w') as locations_json:
                    json.dump(self.locations_dict, locations_json)

        def exportJSON(self):
            with open(self.locations_json_path, 'w') as locations_json:
                json.dump(self.locations_dict, locations_json)

        def get_locations(self):
            return self.locations_dict

        def add_location(self, location):
            self.importJSON()
            self.locations_dict['locations'][location.name] = {}
            self.locations_dict['locations'][location.name]['latitude'] = location.lat
            self.locations_dict['locations'][location.name]['longitude'] = location.lon     
            self.exportJSON()       

        def remove_location(self, location_name):
            try:
                self.locations_dict['locations'].pop(location_name)
            except KeyError:
                return False
            else:
                self.exportJSON()
                return True

        def get_route_info(self, location_from, location_to):
            try:
                destination = self.locations_dict['locations'][location_to]
            except KeyError:
                return False

            server_token = "LQFjEH6XwvteSodBvsTOh0wskzA6XnVAsASUqYSl"
            session = Session(server_token = server_token)
            client = UberRidesClient(session)

            response = client.get_price_estimates(
                start_lat = location_from.lat,
                start_lon = location_from.lon,
                end_lat = destination['latitude'],
                end_lon = destination['longitude'],
                seat_count = 2
            )
            print(response)

    instance = None
    def __new__(cls):
        if not Uber.instance:
            Uber.instance = Uber.__Uber()
        return Uber.instance
