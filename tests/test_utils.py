from csuibot import utils


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
