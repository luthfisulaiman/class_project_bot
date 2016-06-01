from datetime import date


class Zodiac:

    def make_date(self, month, day, year=2000):
        return date(year, month, day)

    def date_includes(self, month, day):
        _date = self.make_date(month, day)
        return self.lower_bound <= _date <= self.upper_bound


class Aries(Zodiac):

    def __init__(self):
        self.name = 'aries'
        self.lower_bound = self.make_date(3, 21)
        self.upper_bound = self.make_date(4, 19)


class Taurus(Zodiac):

    def __init__(self):
        self.name = 'taurus'
        self.lower_bound = self.make_date(4, 20)
        self.upper_bound = self.make_date(5, 20)


class Gemini(Zodiac):

    def __init__(self):
        self.name = 'gemini'
        self.lower_bound = self.make_date(5, 21)
        self.upper_bound = self.make_date(6, 20)


class Cancer(Zodiac):

    def __init__(self):
        self.name = 'cancer'
        self.lower_bound = self.make_date(6, 21)
        self.upper_bound = self.make_date(7, 22)


class Leo(Zodiac):

    def __init__(self):
        self.name = 'leo'
        self.lower_bound = self.make_date(7, 23)
        self.upper_bound = self.make_date(8, 22)


class Virgo(Zodiac):

    def __init__(self):
        self.name = 'virgo'
        self.lower_bound = self.make_date(8, 23)
        self.upper_bound = self.make_date(9, 22)


class Libra(Zodiac):

    def __init__(self):
        self.name = 'libra'
        self.lower_bound = self.make_date(9, 23)
        self.upper_bound = self.make_date(10, 22)


class Scorpio(Zodiac):

    def __init__(self):
        self.name = 'scorpio'
        self.lower_bound = self.make_date(10, 23)
        self.upper_bound = self.make_date(11, 21)


class Sagittarius(Zodiac):

    def __init__(self):
        self.name = 'sagittarius'
        self.lower_bound = self.make_date(11, 22)
        self.upper_bound = self.make_date(12, 21)


class Capricorn(Zodiac):

    def __init__(self):
        self.name = 'capricorn'
        self.lower_bound = self.make_date(12, 22, year=2000)
        self.upper_bound = self.make_date(1, 19, year=2001)

    def date_includes(self, month, day):
        year = 2000 if month == 12 else 2001
        _date = self.make_date(month, day, year=year)

        return self.lower_bound <= _date <= self.upper_bound


class Aquarius(Zodiac):

    def __init__(self):
        self.name = 'aquarius'
        self.lower_bound = self.make_date(1, 20)
        self.upper_bound = self.make_date(2, 18)


class Pisces(Zodiac):

    def __init__(self):
        self.name = 'pisces'
        self.lower_bound = self.make_date(2, 19)
        self.upper_bound = self.make_date(3, 20)
