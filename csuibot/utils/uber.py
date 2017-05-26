import json
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
            with open(self.locations_json_path, 'r') as locations_json:
                self.locations_dict = json.load(locations_json)

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
            session = Session(server_token=server_token)
            client = UberRidesClient(session)

            print(location_from.lat)
            print(location_from.lon)
            print(destination['latitude'])
            print(destination['longitude'])
            response = client.get_price_estimates(
                start_latitude=location_from.lat,
                start_longitude=location_from.lon,
                end_latitude=destination['latitude'],
                end_longitude=destination['longitude'],
                seat_count=2
            )

            estimates = response.json['prices']
            print(response.json)
            print(estimates)
            res = 'Destination: {} ({} kilometers from current position)\n\n'\
                  .format(location_to, estimates[0]["distance"]*1.6)
            res += 'Estimated travel time and fares for each Uber services:\n'
            res += '- UberX ({} minutes, {} rupiah)\n'\
                   .format(estimates[3]["duration"]//60, estimates[3]["estimate"])
            res += '- UberPool ({} minutes, {} rupiah)\n'\
                   .format(estimates[2]["duration"]//60, estimates[2]["estimate"])
            res += '- UberBlack ({} minutes, {} rupiah)\n'\
                   .format(estimates[4]["duration"]//60, estimates[4]["estimate"])
            res += '- UberMotor ({} minutes, {} rupiah)\n\n'\
                   .format(estimates[1]["duration"]//60, estimates[1]["estimate"])
            res += 'Data provided by [Uber] (https://www.uber.com)'
            return res

    instance = None

    def __new__(cls):
        if not Uber.instance:
            Uber.instance = Uber.__Uber()
        return Uber.instance
