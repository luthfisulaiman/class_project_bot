import requests
import json

def GetAQICity(city):
    url = "https://api.waqi.info/feed/"
    token = "21003f71e603a67f7313fd9b3692eb2363412228"
    payload = url + city + "/?token=" + token
    response = requests.get(payload)
    response_json = json.loads(response.text)
    status = response_json['status']

    if(status == 'ok'):
        aqi = response_json['data']['aqi']
        level = ""
        health_implication = ""

        if(int(aqi) >= 0 and int(aqi) <= 50):
            level = "Good"
            health_implication = "Air quality is considered satisfactory," \
                                 " and air pollution poses little or no risk"
        elif(int(aqi) > 50 and int(aqi) <= 100):
            level = "Moderate"
            health_implication = "Air quality is acceptable; however, for some" \
                                 " pollutants there may be a moderate health concern" \
                                 " for a very small number of people who are " \
                                 "unusually sensitive to air pollution."
        elif (int(aqi) > 100 and int(aqi) <= 150):
            level = "Unhealthy for Sensitive Groups"
            health_implication = "Members of sensitive groups may experience health" \
                                 " effects. The general public is not likely " \
                                 "to be affected."
        elif (int(aqi) > 150 and int(aqi) <= 200):
            level = "Unhealthy"
            health_implication = "Everyone may begin to experience health effects;" \
                                 " members of sensitive groups may experience " \
                                 "more serious health effects"
        elif (int(aqi) > 200 and int(aqi) <= 300):
            level = "Very Unhealthy"
            health_implication = "Health warnings of emergency conditions. " \
                                 "The entire population is more likely to be affected."
        elif (int(aqi) > 300):
            level = "Hazardous"
            health_implication = "Health alert: everyone may experience" \
                                 " more serious health effects"

        return 'AQI value: ' + str(aqi) + '\n' + 'Air Quality level: ' + level + '\n' + \
            'Health Implications: ' + health_implication

    elif(status == 'error'):
        return "Invalid city name or coordinate, please try again"

    else:
        return "Invalid city name or coordinate, please try again"


def GetAQICoord(coord):
    url = "https://api.waqi.info/feed/"
    token = "21003f71e603a67f7313fd9b3692eb2363412228"
    coords = coord.split(' ')
    lat = coords[0]
    lon = coords[1]
    payload = url + 'geo:' + lat + ';' + lon + "/?token=" + token
    response = requests.get(payload)
    response_json = json.loads(response.text)
    status = response_json['status']

    if (status == 'ok'):
        aqi = response_json['data']['aqi']
        level = ""
        health_implication = ""

        if (int(aqi) >= 0 and int(aqi) <= 50):
            level = "Good"
            health_implication = "Air quality is considered satisfactory," \
                                 " and air pollution poses little or no risk"
        elif (int(aqi) > 50 and int(aqi) <= 100):
            level = "Moderate"
            health_implication = "Air quality is acceptable; however, for some" \
                                 " pollutants there may be a moderate health concern" \
                                 " for a very small number of people who are " \
                                 "unusually sensitive to air pollution."
        elif (int(aqi) > 100 and int(aqi) <= 150):
            level = "Unhealthy for Sensitive Groups"
            health_implication = "Members of sensitive groups may experience health" \
                                 " effects. The general public is not likely" \
                                 " to be affected."
        elif (int(aqi) > 150 and int(aqi) <= 200):
            level = "Unhealthy"
            health_implication = "Everyone may begin to experience health effects;" \
                                 " members of sensitive groups may experience " \
                                 "more serious health effects"
        elif (int(aqi) > 200 and int(aqi) <= 300):
            level = "Very Unhealthy"
            health_implication = "Health warnings of emergency conditions. " \
                                 "The entire population is more likely to be affected."
        elif (int(aqi) > 300):
            level = "Hazardous"
            health_implication = "Health alert: everyone may experience" \
                                 " more serious health effects"

        return 'AQI value: ' + str(aqi) + '\n' + 'Air Quality level: ' + level + '\n' + \
                'Health Implications: ' + health_implication

    elif (status == 'error'):
        return "Invalid city name or coordinate, please try again"

    else:
        return "Invalid city name or coordinate, please try again"
