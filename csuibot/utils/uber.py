import json
import io
from os import path

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
            with open(self.locations_json_path, 'r') as locations_json:
                json.dump(self.locations_dict, locations_json)

        def get_locations(self):
            return self.locations_dict.keys()

        def add_destination(self, location):
            self.locations_dict[location.name] = {}
            self.locations_dict[location.name]['latitude'] = location.lat
            self.locations_dict[location.name]['longitude'] = location.lon     
            exportJSON()       

        def remove_destination(self, location_name):
            self.locations_dict.pop(location_name, None)

    instance = None
    def __new__(cls):
        if not Uber.instance:
            Uber.instance = Uber.__Uber()
        return Uber.instance
