from haversine import haversine
import json
import random


class Hospital:
    def __init__(self, long=0, lat=0):
        self.long = long
        self.lat = lat

        rs_array = []

        fetch_rs = json.loads(open('csuibot/utils/list_rs.json', 'r').read())

        for rs in fetch_rs:
            temp_dict = {}
            temp_dict['id'] = rs['id']
            temp_dict['nama'] = rs['nama']
            temp_dict['jenis'] = rs['jenis']
            temp_dict['alamat'] = rs['alamat']
            temp_dict['lat'] = rs['lat']
            temp_dict['long'] = rs['long']
            temp_dict['image'] = rs['image']
            rs_array.append(temp_dict)

        self.rs_array = rs_array

    def calculate_dist_rumah_sakit(self):
        latitude = float(self.lat)
        longitude = float(self.long)

        nearest = None
        minimal_latitude = 1.0
        minimal_longitude = 1.0
        for rs in self.rs_array:
            delta_latitude = abs(latitude - float(rs['lat']))
            delta_longitude = abs(longitude - float(rs['long']))

            if (delta_longitude + delta_latitude) < (minimal_longitude + minimal_latitude):
                minimal_latitude = delta_latitude
                minimal_longitude = delta_longitude
                nearest = rs

        source = (latitude, longitude)
        dest = (float(nearest['lat']), float(nearest['long']))
        distance = haversine(source, dest) * 1000

        data = {}
        data['lat'] = nearest['lat']
        data['long'] = nearest['long']
        data['message'] = "Rumah Sakit " + nearest['nama'] + "\n" + nearest['jenis'] \
                          + "\n" + "Alamat: " + nearest['alamat']
        data['distance'] = "Approximated Distance: " + str("{0:.2f}".format(distance)) + " m"
        data['image'] = nearest['image']

        return data

    def get_random_rumah_sakit(self):
        random_items = random.sample(self.rs_array, 5)
        return random_items

    def get_by_id(self, id):
        selected = None

        for rs in self.rs_array:
            if rs['id'] == int(id):
                selected = rs
                break

        data = {}
        data['lat'] = selected['lat']
        data['long'] = selected['long']
        data['message'] = "Rumah Sakit " + selected['nama'] + "\n" + selected['jenis'] \
                          + "\n" + "Alamat: " + selected['alamat']
        data['image'] = selected['image']
        return data
