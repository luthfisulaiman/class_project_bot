from csuibot import utils
from csuibot.utils.message_dist import add_message_to_dist, get_message_dist
import json
import os



class TestZodiac:

    def test_aries_lower_bound(self):
        res = utils.lookup_zodiac(3, 21)
        assert res == 'aries'

    def test_aries_upper_bound(self):
        res = utils.lookup_zodiac(4, 19)
        assert res == 'aries'

    def test_aries_in_between(self):
        res = utils.lookup_zodiac(4, 1)
        assert res == 'aries'

    def test_not_aries(self):
        res = utils.lookup_zodiac(11, 17)
        assert res != 'aries'

    def test_taurus_lower_bound(self):
        res = utils.lookup_zodiac(4, 20)
        assert res == 'taurus'

    def test_taurus_upper_bound(self):
        res = utils.lookup_zodiac(5, 20)
        assert res == 'taurus'

    def test_taurus_in_between(self):
        res = utils.lookup_zodiac(4, 30)
        assert res == 'taurus'

    def test_not_taurus(self):
        res = utils.lookup_zodiac(11, 17)
        assert res != 'taurus'

    def test_gemini_lower_bound(self):
        res = utils.lookup_zodiac(5, 21)
        assert res == 'gemini'

    def test_gemini_upper_bound(self):
        res = utils.lookup_zodiac(6, 20)
        assert res == 'gemini'

    def test_gemini_in_between(self):
        res = utils.lookup_zodiac(6, 6)
        assert res == 'gemini'

    def test_not_gemini(self):
        res = utils.lookup_zodiac(11, 17)
        assert res != 'gemini'

    def test_cancer_lower_bound(self):
        res = utils.lookup_zodiac(6, 21)
        assert res == 'cancer'

    def test_cancer_upper_bound(self):
        res = utils.lookup_zodiac(7, 22)
        assert res == 'cancer'

    def test_cancer_in_between(self):
        res = utils.lookup_zodiac(7, 7)
        assert res == 'cancer'

    def test_not_cancer(self):
        res = utils.lookup_zodiac(11, 17)
        assert res != 'cancer'

    def test_leo_lower_bound(self):
        res = utils.lookup_zodiac(7, 23)
        assert res == 'leo'

    def test_leo_upper_bound(self):
        res = utils.lookup_zodiac(8, 22)
        assert res == 'leo'

    def test_leo_in_between(self):
        res = utils.lookup_zodiac(8, 8)
        assert res == 'leo'

    def test_not_leo(self):
        res = utils.lookup_zodiac(11, 17)
        assert res != 'leo'

    def test_virgo_lower_bound(self):
        res = utils.lookup_zodiac(8, 23)
        assert res == 'virgo'

    def test_virgo_upper_bound(self):
        res = utils.lookup_zodiac(9, 22)
        assert res == 'virgo'

    def test_virgo_in_between(self):
        res = utils.lookup_zodiac(9, 9)
        assert res == 'virgo'

    def test_not_virgo(self):
        res = utils.lookup_zodiac(11, 17)
        assert res != 'virgo'

    def test_libra_lower_bound(self):
        res = utils.lookup_zodiac(9, 23)
        assert res == 'libra'

    def test_libra_upper_bound(self):
        res = utils.lookup_zodiac(10, 22)
        assert res == 'libra'

    def test_libra_in_between(self):
        res = utils.lookup_zodiac(10, 10)
        assert res == 'libra'

    def test_not_libra(self):
        res = utils.lookup_zodiac(11, 17)
        assert res != 'libra'

    def test_scorpio_lower_bound(self):
        res = utils.lookup_zodiac(10, 23)
        assert res == 'scorpio'

    def test_scorpio_upper_bound(self):
        res = utils.lookup_zodiac(11, 21)
        assert res == 'scorpio'

    def test_scorpio_in_between(self):
        res = utils.lookup_zodiac(11, 11)
        assert res == 'scorpio'

    def test_not_scorpio(self):
        res = utils.lookup_zodiac(11, 27)
        assert res != 'scorpio'

    def test_sagittarius_lower_bound(self):
        res = utils.lookup_zodiac(11, 22)
        assert res == 'sagittarius'

    def test_sagittarius_upper_bound(self):
        res = utils.lookup_zodiac(12, 21)
        assert res == 'sagittarius'

    def test_sagittarius_in_between(self):
        res = utils.lookup_zodiac(12, 12)
        assert res == 'sagittarius'

    def test_not_sagittarius(self):
        res = utils.lookup_zodiac(11, 17)
        assert res != 'sagittarius'

    def test_capricorn_lower_bound(self):
        res = utils.lookup_zodiac(12, 22)
        assert res == 'capricorn'

    def test_capricorn_upper_bound(self):
        res = utils.lookup_zodiac(1, 19)
        assert res == 'capricorn'

    def test_capricorn_in_between(self):
        res = utils.lookup_zodiac(1, 1)
        assert res == 'capricorn'

    def test_not_capricorn(self):
        res = utils.lookup_zodiac(11, 17)
        assert res != 'capricorn'

    def test_aquarius_lower_bound(self):
        res = utils.lookup_zodiac(1, 20)
        assert res == 'aquarius'

    def test_aquarius_upper_bound(self):
        res = utils.lookup_zodiac(2, 18)
        assert res == 'aquarius'

    def test_aquarius_in_between(self):
        res = utils.lookup_zodiac(2, 2)
        assert res == 'aquarius'

    def test_not_aquarius(self):
        res = utils.lookup_zodiac(11, 17)
        assert res != 'aquarius'

    def test_pisces_lower_bound(self):
        res = utils.lookup_zodiac(2, 19)
        assert res == 'pisces'

    def test_pisces_upper_bound(self):
        res = utils.lookup_zodiac(3, 20)
        assert res == 'pisces'

    def test_pisces_in_between(self):
        res = utils.lookup_zodiac(3, 3)
        assert res == 'pisces'

    def test_not_pisces(self):
        res = utils.lookup_zodiac(11, 17)
        assert res != 'pisces'

    def test_unknown_zodiac(self, mocker):
        class FakeZodiac():
            def date_includes(self, *args, **kwargs):
                return False

        mocker.patch('csuibot.utils.z.Scorpio', return_value=FakeZodiac())

        res = utils.lookup_zodiac(11, 17)

        assert res == 'Unknown zodiac'


class TestChineseZodiac:

    def run_test(self, expected_zodiac, years):
        res = [utils.lookup_chinese_zodiac(y) == expected_zodiac for y in years]

        assert all(res)

    def test_rat(self):
        years = [1996, 1984, 1972, 1960, 2008, 2020]
        self.run_test('rat', years)

    def test_buffalo(self):
        years = [1997, 1985, 1973, 1961, 2009, 2021]
        self.run_test('buffalo', years)

    def test_tiger(self):
        years = [1998, 1986, 1974, 1962, 2010, 2022]
        self.run_test('tiger', years)

    def test_rabbit(self):
        years = [1999, 1987, 1975, 1963, 2011, 2023]
        self.run_test('rabbit', years)

    def test_dragon(self):
        years = [2000, 1988, 1976, 1964, 2012, 2024]
        self.run_test('dragon', years)

    def test_snake(self):
        years = [2001, 1989, 1977, 1965, 2013, 2025]
        self.run_test('snake', years)

    def test_horse(self):
        years = [2002, 1990, 1978, 1966, 2014, 2026]
        self.run_test('horse', years)

    def test_goat(self):
        years = [2003, 1991, 1979, 1967, 2015, 2027]
        self.run_test('goat', years)

    def test_monkey(self):
        years = [2004, 1992, 1980, 1968, 2016, 2028]
        self.run_test('monkey', years)

    def test_unknown_zodiac(self):
        years = [2005, 1993, 1981, 1969, 2017, 2029]
        self.run_test('Unknown zodiac', years)


class TestMessageDist:
    def test_file_dist_not_found(self):
        try:
            os.remove('dist.txt')
        except OSError:
            pass

        expected_res = 'Failed to open file.'
        actual_res = get_message_dist()

        assert expected_res == actual_res

    def test_division_by_zero(self):
        chat_id = 999
        example_dist = {'dist': {}}
        example_dist['dist'][str(chat_id)] = {}
        for i in range(0, 24):
            example_dist['dist'][str(chat_id)][str(i)] = 0

        try:
            with open('dist.txt', 'w') as dist_file:
                json.dump(example_dist, dist_file)
        except IOError:
            pass
        res = utils.lookup_message_dist(chat_id)
        assert res is not None


    def test_chatid_not_in_file(self):
        try:
            os.remove('dist.txt')
        except OSError:
            pass
        chat_id = 0
        hour = 0
        expected_res = {'dist': {}}
        expected_res['dist'][str(chat_id)] = {}
        for i in range(0, 24):
            if i == hour:
                expected_res['dist'][str(chat_id)][str(i)] = 1
            else:
                expected_res['dist'][str(chat_id)][str(i)] = 0

        add_message_to_dist(chat_id, hour)
        actual_res = get_message_dist()

        assert actual_res == expected_res

    def test_get_message_dist(self):
        expected_dist = {'dist': {}}
        expected_dist['dist'][str(0)] = {}
        for i in range(0, 24):
            expected_dist['dist'][str(0)][str(i)] = 1

        with open('dist.txt', 'w') as outfile:
            json.dump(expected_dist, outfile)

        chat_id = 0
        actual_dist = utils.lookup_message_dist(chat_id)

        expected_res = ''
        for i in range(0, 24):
            expected_res = expected_res + (str(i).zfill(2) + ' -> ' + str(4.17) + '%\n')
        assert actual_dist == expected_res


class TestYelKomputer:

    def test_yelkomputer(self):
        yelkomputer = (
            'Komputer!\n\n'
            'Masuknya Sulit, Fasilkom!\n'
            'Sarana Komplit, Fasilkom!\n'
            'Kelasnya Elit, Fasilkom!\n'
            'Ilmu Komputer Jaya!\n'
            'To Be Number One\n'
            'FA... SIL... KOM...\n'
            'Viva... viva... viva... Fasilkom!'
        )
        res = utils.lookup_yelkomputer('/yelkomputer')
        assert res == yelkomputer

    def test_yelkomputer_with_mars_perindo(self):
        yelkomputer = (
            'Marilah Seluruh rakyat Indonesia\n'
            'Arahkan pandanganmu ke depan\n'
            'Raihlah mimpimu bagi nusa bangsa\n'
            'Satukan tekadmu untuk masa depan\n'
            'Pantang menyerah itulah pedomanmu\n'
            'Entaskan kemiskinan cita-citamu\n'
            'Rintangan tak menggentarkan dirimu\n'
            'Indonesia maju sejahtera tujuanmu\n'
            'Nyalakan api semangat perjuangan\n'
            'Dengungkan gema nyatakan persatuan\n'
            'Oleh PERINDO... oleh PERINDO...\n'
            'Jayalah Indonesia!'
        )
        res = utils.lookup_yelkomputer('/yelkomputer')
        assert res != yelkomputer

    def test_yelkomputer_value_error(self):
        try:
            utils.lookup_yelkomputer('/yelkomputer args')
        except ValueError as e:
            assert str(e) == 'Command /yelkomputer doesn\'t need any arguments'
