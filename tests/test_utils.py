from csuibot import utils
import re
from requests.exceptions import ConnectionError
import requests


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


class TestDefine:

    def test_define_diamond(self):
        res = utils.lookup_define('diamond')
        result = 'a precious stone consisting of a clear and colourless'
        result += ' crystalline form of pure carbon,'
        result += ' the hardest naturally occurring substance'
        assert res == result

    def test_define_read(self):
        res = utils.lookup_define('read')
        result = 'look at and comprehend the meaning of (written or'
        result += ' printed matter) by interpreting the'
        result += ' characters or symbols of which it is composed'
        assert res == result

    def test_define_value_error(self):
        utils.lookup_define('/define')

    def test_define_contains_num(self):
        res = utils.lookup_define('r34d')
        assert res == 'r34d contains number'

    def test_define_page_not_found(self):
        try:
            utils.lookup_define('/define akugantengsekali')
        except requests.HTTPError as e:
            assert str(e) == ('"akugantengsekali" is not an english word')


class TestKelaskata:

    def run_test(self, word, expected):
        try:
            result = utils.lookup_kelaskata(word)
            assert result == expected
        except requests.ConnectionError as e:
            assert str(e) == ('"akugantengsekali" is not a word')

    def test_kelaskata_intan(self):
        self.run_test('intan', 'intan/n')

    def test_kelaskata_membaca(self):
        self.run_test('membaca', 'membaca/v')

    def test_kelaskata_value_error(self):
        try:
            self.run_test('', 'Try /kelaskata [word]')
        except ValueError as e:
            assert str(e) == 'Try /kelaskata [word]'


class TestCustomChuckJoke:

    def test_custom_chuck(self):
        res = utils.custom_chuck.CustomChuckJoke().generate_custom_chuck_joke(
                "Chuck", "Norris")

        assert res is not None

    def test_fetch(self):
        res = utils.generate_custom_chuck_joke("Chuck", "Norris")

        assert res is not None


class TestPassword:

    def test_minimum_length(self):
        res = utils.generate_password(1)
        assert len(res) == 1

    def test_average_length(self):
        res = utils.generate_password(16)
        assert len(res) == 16

    def test_maximum_length(self):
        res = utils.generate_password(128)
        assert len(res) == 128

    def test_under_minimum_length(self):
        res = utils.generate_password(0)
        expected = 'Only a single integer, 1-128, is allowed as length'
        assert res == expected

    def test_over_maximum_length(self):
        res = utils.generate_password(500)
        expected = 'Only a single integer, 1-128, is allowed as length'
        assert res == expected


class TestIP:

    def test_wellformed_ip(self):
        res = utils.get_public_ip()
        pattern = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
        assert pattern.match(res)


class TestHipster():

    def test_make_one_paragraph(self):
        res = utils.make_hipster(1)
        length = res.count("\n")
        assert length == 0

    def test_make_four_paragraph(self):
        res = utils.make_hipster(4)
        length = res.count("\n")
        assert length == 3

    def test_nums_zero(self):
        res = utils.make_hipster(0)
        assert res == 'Number of paragraph exceed the limit'

    def test_nums_hundred(self):
        res = utils.make_hipster(100)
        assert res == 'Number of paragraph exceed the limit'


class TestMeme:

    def test_success(self):
        res = utils.get_meme("Top", "Bottom")
        assert "http" in res

    def test_top_too_long(self):
        top = (
            'Lorem_ipsum_dolor_sit_amet_consectetur_adipiscing'
            '_elit_Proin_nec_massa_tempus_blandit_ipsum_eget_'
            'aliquam_diam_Sed_porttitor_eget_lorem_at_mollis_'
            'Maecenas_metus_diam_sagittis_at_ex_eu_porta_faucibus_'
            'nulla_Praesent_tempus_nunc_felis_vitae_aliquet_diam_'
            'pellentesque_at_Aliquam_venenatis_vel_velit_quis_'
            'sollicitudin_Ut_sit_amet_nisi_a_ante_congue_tincidunt_'
            'at_sit_amet_elit_Etiam_pharetra_risus_sed_interdum_mollis'
            '_Morbi_facilisis_ipsum_non_consectetur_euismod_Donec_'
            'id_neque_felis_Sed_maximus_rutrum_varius_Phasellus_'
            'id_dapibus_arcu_Suspendisse_tincidunt_vulputate_nulla_'
            'ac_elementum_ipsum_dictum_vel_Class_aptent_taciti_'
            'sociosqu_ad_litora_torquent_per_conubia_'
            'nostra_per_inceptos_himenaeos')
        res = utils.get_meme(top, "Bottom")
        assert res == 'Caption is too long, min < 100 words'

    def test_bottom_too_long(self):
        bottom = (
            'Lorem_ipsum_dolor_sit_amet_consectetur_adipiscing'
            '_elit_Proin_nec_massa_tempus_blandit_ipsum_eget_'
            'aliquam_diam_Sed_porttitor_eget_lorem_at_mollis_'
            'Maecenas_metus_diam_sagittis_at_ex_eu_porta_faucibus_'
            'nulla_Praesent_tempus_nunc_felis_vitae_aliquet_diam_'
            'pellentesque_at_Aliquam_venenatis_vel_velit_quis_'
            'sollicitudin_Ut_sit_amet_nisi_a_ante_congue_tincidunt_'
            'at_sit_amet_elit_Etiam_pharetra_risus_sed_interdum_mollis'
            '_Morbi_facilisis_ipsum_non_consectetur_euismod_Donec_'
            'id_neque_felis_Sed_maximus_rutrum_varius_Phasellus_'
            'id_dapibus_arcu_Suspendisse_tincidunt_vulputate_nulla_'
            'ac_elementum_ipsum_dictum_vel_Class_aptent_taciti_'
            'sociosqu_ad_litora_torquent_per_conubia_'
            'nostra_per_inceptos_himenaeos')
        res = utils.get_meme("top", bottom)
        assert res == 'Caption is too long, min < 100 words'


class TestLoremIpsum:
    def test_get_loripsum(self):
        try:
            res = utils.call_lorem_ipsum()


class TestSoundComposer:
    def test_get_track(self):
        try:
            res = utils.call_composer('iamlione')
        except ValueError:
            pass
        except ConnectionError:
            pass
        else:
            assert res is not None


class TestXkcd:
    def test_xkcd(self):
        res = utils.xkcd.Comic.get_latest_comic()

        assert res is not None

    def test_fetch(self):
        res = utils.fetch_latest_xkcd()

        assert res is not None


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
