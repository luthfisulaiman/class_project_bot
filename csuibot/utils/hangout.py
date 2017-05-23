import math
import os
import json
import sys


class Hangout:
    def __init__(self):
        self.name = ''
        self.image_dir = ''
        self.address = ''
        self.longitude = 0
        self.latitude = 0

    def count_distance(self, user_long, user_lat):
        earth_radius = 6371
        d_lat = self.deg2rad(self.latitude - user_lat)
        d_lon = self.deg2rad(self.longitude - user_long)

        tmp_left = math.sin(d_lat / 2) * math.sin(d_lat / 2)

        tmp_1 = math.cos(self.deg2rad(user_lat)) * math.cos(self.deg2rad(self.latitude))
        tmp_2 = math.sin(d_lon / 2) * math.sin(d_lon / 2)
        tmp = tmp_1 * tmp_2

        a = tmp_left + tmp

        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        d = (earth_radius * c) * 1000
        return d

    def deg2rad(self, deg):
        return deg * (math.pi / 180)


def create_hangout_list():
    hangout_list = []
    path = os.path.dirname(os.path.abspath(__file__))
    json_path = path + "/hangout.json"
    with open(json_path) as json_file:
        json_data = json.load(json_file)

    for data in json_data:
        h = Hangout()
        h.name = data['name']
        h.address = data['location']
        h.image_dir = path + '/hangout_images/' + data['image']
        h.latitude = float(data['coordinate']['latitude'])
        h.longitude = float(data['coordinate']['longitude'])
        hangout_list.append(h)

    return hangout_list


def find_nearest_place(hangout_list, user_long, user_lat):

    n_dist = sys.maxsize
    nearest = None
    for data in hangout_list:
        x = data.count_distance(user_long, user_lat)
        if n_dist < x:
            n_dist = x
            nearest = data

    return nearest, n_dist
