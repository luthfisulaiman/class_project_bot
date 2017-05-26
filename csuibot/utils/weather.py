import pyowm
from geopy.geocoders import Nominatim

METRIC_UNIT = "meter/sec"
IMPER_UNIT = "miles/hour"
WEATHER_UNIT_M = "metric"
WEATHER_UNIT_I = "imperial"
WT_KEL = "Kelvin"
WT_FAH = "Fahrenheit"
WT_CEL = "Celcius"

# Wind speed conversion constants
MILES_PER_HOUR_FOR_ONE_METER_PER_SEC = 2.23694

owm = pyowm.OWM('0b88353793f692bb5e20255c89cb7f1e')


class Weather:

    def __init__(self, lon=0, lat=0):
        self.lon = lon
        self.lat = lat
        self.unit = WEATHER_UNIT_M
        self.temp = WT_CEL

    def lookup_weather(self, lat, lon, unit, temp):
        geolocator = Nominatim()
        location = geolocator.reverse(lat,lon)
        observation = owm.weather_at_place(location.address)
        return self.output_builder(observation, unit, temp)

    def city_lookup_weather(self, city, unit, temp):
        observation = owm.weather_at_place(city)
        return self.output_builder(observation, unit, temp)

    def output_builder(self, observation, unit, temp):

        w = observation.get_weather()
        l = observation.get_location()

        city = l.get_name()
        weather = w.get_status()
        wid = w.get_weather_code()
        emoji = self.getEmoji(wid)
        if (unit == WEATHER_UNIT_M):
            wind_speed = str(w.get_wind().get('speed'))
            wind_unt = METRIC_UNIT
        if (unit == WEATHER_UNIT_I):
            wind_speed = str(self.metric_wind_to_imperial(w.get_wind().get('speed')))
            wind_unt = IMPER_UNIT
        if (temp == WT_KEL):
            temper = str(w.get_temperature('kelvin').get('temp'))
            temper_unt = WT_KEL
        if (temp == WT_FAH):
            temper = str(w.get_temperature('fahrenheit').get('temp'))
            temper_unt = WT_FAH
        if (temp == WT_CEL):
            temper = str(w.get_temperature('celsius').get('temp'))
            temper_unt = WT_FAH
        humid = w.get_humidity()

        return ("Weather at your position ({}):\n{} {}\n{} {}\n{} {}\n{}%"
                .format(str(city), str(weather), str(emoji), str(wind_speed),
                        str(wind_unt), str(temper), str(temper_unt), str(humid)))

    def metric_wind_to_imperial(self, windinms):
        return windinms * MILES_PER_HOUR_FOR_ONE_METER_PER_SEC

    def getEmoji(self, weatherID):
        # Openweathermap Weather codes and corressponding emojis
        thunderstorm = u'\U0001F4A8'    # Code: 200's, 900, 901, 902, 905
        drizzle = u'\U0001F4A7'         # Code: 300's
        rain = u'\U00002614'            # Code: 500's
        atmosphere = u'\U0001F301'      # Code: 700's foogy
        clearSky = u'\U00002600'        # Code: 800 clear sky
        fewClouds = u'\U000026C5'       # Code: 801 sun behind clouds
        clouds = u'\U00002601'          # Code: 802-803-804 clouds general
        hot = u'\U0001F525'             # Code: 904
        defaultEmoji = u'\U0001F300'    # default emojis

        if weatherID:
            if (str(weatherID)[0] == '2' or weatherID == 900 or
                    weatherID == 901 or weatherID == 902 or weatherID == 905):
                return thunderstorm

            elif str(weatherID)[0] == '3':
                return drizzle

            elif str(weatherID)[0] == '5':
                return rain

            elif str(weatherID)[0] == '7':
                return atmosphere

            elif weatherID == 800:
                return clearSky

            elif weatherID == 801:
                return fewClouds

            elif weatherID == 802 or weatherID == 803 or weatherID == 803:
                return clouds

            elif weatherID == 904:
                return hot

            else:
                return defaultEmoji    # Default emoji
