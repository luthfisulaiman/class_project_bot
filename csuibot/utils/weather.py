class Weather:
    WU_METRIC_SET = "Metric (meter/sec)"
    WU_IMPER_SET = "Imperial (miles/hour)"
    METRIC_UNIT = "meter/sec"
    IMPER_UNIT = "miles/hour"
    WT_KEL = "Kelvin"
    WT_FAH = "Fahrenheit"
    WT_CEL = "Celcius"


    def __init__(self, location):
        self.location = location
        self.unit = WU_METRIC
        self.temp = WT_KEL

    def lookup_weather(self):
        pass

    def configure_weather(self):
        pass

    def group_lookup_weather(self):
        pass
