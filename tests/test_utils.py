from csuibot import utils, config
from csuibot.utils import plant as p
from csuibot.utils import data_processor as processor
from csuibot.utils.message_dist import add_message_to_dist, get_message_dist
import os
import re
from requests.exceptions import ConnectionError
import requests
import json


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
            def date_includes(self, args, kwargs):
                return False

        mocker.patch('csuibot.utils.z.Scorpio', return_value=FakeZodiac())

        res = utils.lookup_zodiac(11, 17)

        assert res == 'Unknown zodiac'


class TestNotifTaker:
    def test_notif_taker(self):
        res = utils.takeSceleNotif()
        assert res != ""


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


class TestWiki:
    wikipedia_summary = (
        'The Ukrainian revolution of 2014 (also known as the'
        ' Euromaidan Revolution or Revolution of Dignity; Ukrainian:'
        ' Революція гідності, Revoliutsiia hidnosti) took place in'
        ' Ukraine in February 2014, when a series of violent events'
        ' involving protesters, riot police, and unknown shooters in'
        ' the capital, Kiev, culminated in the ousting of Ukrainian'
        ' President, Viktor Yanukovych. This was followed by a series'
        ' of changes in Ukraine\'s sociopolitical system, including'
        ' the formation of a new interim government, the restoration'
        ' of the previous constitution, and a call to hold impromptu'
        ' presidential elections within months.\n\n'
        'source: https://en.wikipedia.org/wiki/2014_Ukrainian_revolution'
    )

    def test_wiki_wikipedia(self):
        res = utils.lookup_wiki('The Ukrainian revolution of 2014')
        assert res == self.wikipedia_summary

    def test_wiki_tongkol(self):
        res = utils.lookup_wiki('Tongkol')
        assert res != self.wikipedia_summary

    def test_wiki_value_error(self):
        try:
            utils.lookup_wiki('')
        except ValueError as e:
            assert str(e) == 'Command /wiki need an argument'

    def test_wiki_page_error(self):
        try:
            utils.lookup_wiki('nama_nama_ikan')
        except IndexError as e:
            assert str(e) == (
                'Page id "nama_nama_ikan" does not match any pages.'
                ' Try another id!'
            )


class TestPlant:
    def test_is_poisonous_true(self):
        plant = p.Plant('test', True, 'test')
        assert plant.is_poisonous is True

    def test_is_poisonous_false(self):
        plant = p.Plant('test', False, 'test')
        assert plant.is_poisonous is False

    def test_name(self):
        plant = p.Plant('test', False, 'test')
        assert plant.name == 'test'

    def test_desription(self):
        plant = p.Plant('test', False, 'test')
        assert plant.description == 'test'


class TestDataProcessor:
    def test_fetch_data_is_poisonous(self):
        test = processor.fetch_data('Daffodil')
        assert test is not None

    def test_fetch_data_not_poisonous(self):
        test = processor.fetch_data('test')
        assert test is not None

    def test_fetch_all_data(self):
        test = processor.fetch_all_data()
        assert test is not None

    def test_fetch_user_input(self):
        test = processor.fetch_user_input('elephant')
        assert test is None

    def test_fetch_user_input_trivia(self):
        test = processor.fetch_user_input('triviaplant')
        assert test is not None

    def test_fetch_user_input_ask_false(self):
        test = processor.fetch_user_input('askplant apple')
        assert test is not None

    def test_fetch_user_input_ask_true(self):
        test = processor.fetch_user_input('askplant Daffodil')
        assert test is not None

    def test_send_trivia(self):
        test = processor.send_trivia()
        assert test is not None


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
        assert actual_dist is not None


class TestMarsFasilkom:
    def test_marsfasilkom(self):
        marsfasilkom = (
            'Samudera laut ilmu\n'
            'Terhampar di hadapanku\n'
            'Cakrawala bersinar\n'
            'Memanggil ku ke sana\n\n'
            '‘Kan ku seberangi lautan\n'
            '‘Tak ku kenal putus asa\n'
            'Dengan daya dan upaya\n'
            'Untuk ilmu komputer\n')
        res = utils.lookup_marsfasilkom('/marsfasilkom')
        assert res == marsfasilkom

    def test_marsfasilkom_value_error(self):
        try:
            utils.lookup_marsfasilkom('/marsfasilkom args')
        except ValueError as e:
            assert str(e) == 'Command /marsfasilkom doesn\'t need any arguments'


class TestYelFasilkom:
    def test_yelFasilkom(self):
        yelfasilkom = (
            'Fasilkom!!!\n'
            'Fasilkom!\n'
            'Ilmu Komputer\n'
            'Fasilkom!\n'
            'Satu Banding Seratus\n'
            'Kami Elit, Kami Kompak, Kami Anak UI\n'
            'MIPA Bukan, Teknik Bukan,\n'
            'FE Apalagi\n'
            'Kami ini Fakultas No.1 di UI\n'
            'Kami Cinta Fasilkom\n'
            'Kami Bangga Fasilkom\n'
            'Maju Terus\n'
            'Fasilkom!')
        res = utils.lookup_yelfasilkom('/yelfasilkom')
        assert res == yelfasilkom

    def test_yelfasilkom_value_error(self):
        try:
            utils.lookup_yelfasilkom('/yelfasilkom args')
        except ValueError as e:
            assert str(e) == 'Command /yelfasilkom doesn\'t need any arguments'


class TestDiscreteMaterial:
    def test_number_theory(self):
        try:
            res = utils.call_discrete_material('number theory')
        except ConnectionError:
            pass
        else:
            assert res is not None

    def test_gcd(self):
        try:
            res = utils.call_discrete_material('gcd')
        except ConnectionError:
            pass
        else:
            assert res is not None

    def test_lcm(self):
        try:
            res = utils.call_discrete_material('lcm')
        except ConnectionError:
            pass
        else:
            assert res is not None

    def test_relasi_rekurensi(self):
        try:
            res = utils.call_discrete_material('relasi rekurensi')
        except ConnectionError:
            pass
        else:
            assert res is not None

    def test_relasi_biner(self):
        try:
            res = utils.call_discrete_material('relasi biner')
        except ConnectionError:
            pass
        else:
            assert res is not None

    def test_domain_range(self):
        try:
            res = utils.call_discrete_material('domain dan range')
        except ConnectionError:
            pass
        else:
            assert res is not None


class TestNotes:
    def run_test(self, command, text=''):
        if command == 'add':
            a = utils.manage_notes(command, text)
            assert a == 'Notes added'
        elif command == 'view':
            text = utils.manage_notes(command)
            assert type(text) == str and len(text) > 0

    def test_write_text(self):
        text = 'Test add text'
        self.run_test('add', text)

    def test_view(self):
        a = utils.manage_notes('view')
        assert a == 'List notes:\n1. Test add text\n'

    def test_view_empty(self):
        f = open('notes.json', 'w')
        f.close()

        a = utils.manage_notes('view')
        assert a == 'No notes yet'

    def test_write_json_decode_error(self, mocker):
        with mocker.patch('csuibot.utils.note.Notes') as MockNotes:
            instance = MockNotes.return_value
            instance.wite.side_effect = json.JSONDecodeError

            a = utils.manage_notes('write', 'aaa')
            assert a is None


class TestDefinisi:
    def run_test(self, word, expected_output):
        mean = utils.lookup_definisi(word)
        assert mean == expected_output

    def test_found(self):
        self.run_test('bahtera', 'Nomina:\n1. perahu; kapal\n\n')

    def test_not_found(self):
        expected_output = 'makimaki is not a word :(, maybe try another one?'
        self.run_test('makimaki', expected_output)

    def test_multiple_word(self):
        expected_output = 'Nomina:\n1. gelombang hidup; kehidupan\n\n'
        self.run_test('bahtera hidup', expected_output)

    def test_with_number(self):
        expected_output = 'Nomina:\n1. abad Masehi ke-10\n\n'
        self.run_test('kurun masehi ke-10', expected_output)


class TestReminder:
    def test_reminder_return_text_one_word(self):
        output = utils.remind_me(0, "Test")
        assert output == "Test"

    def test_reminder_return_text_more_word(self):
        output = utils.remind_me(0, "Test more")
        assert output == "Test more"


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


class TestOriconBooks:

    def test_books(self):
        res = utils.books.Books().get_top_10('2017-04-10')

        assert res is not None

    def test_fetch(self):
        res = utils.get_oricon_books('2017-04-10')

        assert res is not None

    def test_no_entry(mocker):
        res = utils.get_oricon_books('2017-10-16')

        assert res == "No chart is found on this date."

    def test_too_early(mocker):
        res = utils.get_oricon_books('2017-04-03')

        assert res == "Oricon books' earliest record is on 2017-04-10"

    def test_not_monday(mocker):
        res = utils.get_oricon_books('2017-05-12')

        assert res == 'Oricon books command only accepts dates of Mondays.'

    def test_invalid_date(mocker):
        res = utils.get_oricon_books('2017-05-99')

        assert res == 'Requested date is invalid.'
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
        except ConnectionError:
            pass
        else:
            assert res is not None


class TestSoundComposer:
    def test_get_track(self):
        try:
            res = utils.call_composer('iamlione')
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


class TestDayofDate:
    def test_dayofdate(self):
        day = utils.lookup_dayofdate(2016, 5, 13)
        assert day == 'Friday'

    def test_invalid_dayofdate(self):
        day = utils.lookup_dayofdate(2016, 20, 13)
        assert day == ('Incorrect use of dayofdate command. '
                       'Please write a valid date in the form of yyyy-mm-dd, '
                       'such as 2016-05-13')


class TestChuck:
    def test_get_chuck(self):
        try:
            res = utils.get_chuck('/chuck')
        except ConnectionError:
            pass
        else:
            assert res is not None


class TestYoutube:
    def test_get_url(self):
        try:
            res = utils.lookup_url('https://www.youtube.com/watch?v=kJ5PCbtiCpk')
        except ConnectionError:
            pass
        except AttributeError:
            pass
        else:
            assert res is not None

    def test_video_not_found(self):
        try:
            res = utils.lookup_url('https://www.youtube.com/watch?v=kJ5PCbtwkwwkkwkwwk')
        except ConnectionError:
            pass
        except AttributeError:
            pass
        else:
            assert res == "This video is unavailable."

    def test_no_http(self):
        res = utils.lookup_url("youtube.com/watch?v=kJ5PCbtiCpk")
        assert res == "Invalid URL, do you mean http://youtube.com/watch?v=kJ5PCbtiCpk ?"

    def test_not_youtube_video(self):
        res = utils.lookup_url("http://youtube.com")
        assert res == "Please provide a YouTube video URL"


class TestJapanArtist:
    def test_get_artist(self):
        try:
            res = utils.lookup_artist('Kana Nishino')
        except ConnectionError:
            pass
        else:
            assert res is not None

    def test_get_artist_not_found(self):
        try:
            res = utils.lookup_artist('Tulus')
        except ConnectionError:
            pass
        else:
            assert res == 'Artist not present on the Top 100 Chart'


class TestTropicalChartBillboard:
    def test_get_top10_200_chart(self):
        res = utils.b.get_top10('200')
        assert len(res['items']) == 10

    def test_get_top10_tropical_chart(self):
        res = utils.b.get_top10('tropical')
        assert len(res['items']) == 10

    def test_get_top10_hot100_chart(self):
        res = utils.b.get_top10('hot100')
        assert len(res['items']) == 10

    def test_invalid_chart_category(self):
        res = utils.b.get_top10('invalid')
        assert res == 'Invalid chart category'


class TestOriconCD:
    def test_connection_error(self, mocker):
        mocker.patch('csuibot.utils.ocd.Oricon_cd._get_page', side_effect=ConnectionError)

        output = utils.top_ten_cd_oricon('w', '2017-05-05')

        assert output == 'Error occured when connecting to Oricon website.'

    def test_daily_chart(self):
        output = utils.top_ten_cd_oricon('d', '2017-05-12')

        assert len(output.split('\n')) >= 10

    def test_weekly_chart(self):
        output = utils.top_ten_cd_oricon('w', '2017-05-15')

        assert len(output.split('\n')) >= 10

    def test_montly_chart(self):
        output = utils.top_ten_cd_oricon('m', '2017-04')

        assert len(output.split('\n')) >= 10

    def test_yearly_chart(self):
        output = utils.top_ten_cd_oricon('y', '2016')

        assert len(output.split('\n')) >= 10

    def test_unknown(self):
        output = utils.top_ten_cd_oricon('d', '1854-05-05')

        assert output == "Oricon don't know chart in this date"

    def test_invalid_date(self):
        output = utils.top_ten_cd_oricon('d', '9999-12-99')

        assert output == 'Invalid date'

    def test_invalid_month(self):
        output = utils.top_ten_cd_oricon('m', '2016-90')

        assert output == 'Invalid date'

    def test_invalid_date_format(self):
        output = utils.top_ten_cd_oricon('d', 'Maki Cantik Sekali')

        assert output == 'Invalid date'


class TestHot100_artist:
    err_msg = ("Artist is not present on chart or no such artist exists\n"
               "Artist's name is case sensitive")

    def run_test(self, artist, expectedresult):
        try:
            result = utils.find_hot100_artist(artist)
            assert result == expectedresult
        except requests.ConnectionError as ce:
            assert str(ce) == TestHot100_artist.err_msg

    def test_h100artist_found(self):
        exp = ("Russ\nLosin Control\n68\n")
        self.run_test('Russ', exp)

    def test_h100artist_notfound(self):
        self.run_test('foo bar', TestHot100_artist.err_msg)


class TestNewAge_artist:
    err_msg = ("Artist is not present on chart or no such artist exists\n"
               "Artist's name is case sensitive")

    def run_test(self, artist, expectedresult):
        try:
            result = utils.find_newage_artist(artist)
            assert result == expectedresult
        except requests.ConnectionError as ce:
            assert str(ce) == TestNewAge_artist.err_msg

    def test_newageartist_found(self):
        exp = ("Enya\nDark Sky Island\n3\n")
        self.run_test('Enya', exp)

    def test_newageartist_notfound(self):
        self.run_test('foo bar', TestNewAge_artist.err_msg)


class TestComic:
    def test_valid(self):
        comic = utils.get_comic('1834')
        assert "https" in comic

    def test_lower_bound(self):
        comic = utils.get_comic('0')
        error = 'Cant\'t found requested comic. Please ensure that your input is correct'
        assert error == comic

    def test_upper_bound(self):
        comic = utils.get_comic('10000')
        error = 'Cant\'t found requested comic. Please ensure that your input is correct'
        assert error == comic

    def test_invalid(self):
        comic = utils.get_comic('abab')
        error = 'Cant\'t found requested comic. Please ensure that your input is correct'
        assert error == comic


class TestHotCountry_artist:
    err_msg = ("Artist is not present on chart or no such artist exists\n"
               "Artist's name is case sensitive")

    def run_test(self, artist, expectedresult):
        try:
            result = utils.find_hotcountry_artist(artist)
            assert result == expectedresult
        except requests.ConnectionError as ce:
            assert str(ce) == TestHotCountry_artist.err_msg

    def test_hcountryartist_found(self):
        exp = ("Sam Hunt\nBody Like A Back Road\n1\n")

        self.run_test('Sam Hunt', exp)

    def test_hcountryartist_notfound(self):
        self.run_test('foo bar', TestHotCountry_artist.err_msg)


class TestHotcountry:
    def run_test(self, expected):
        try:
            result = utils.lookup_hotcountry()
            assert result == expected
        except requests.ConnectionError as e:
            assert str(e) == ('Cannot connect to billboard API')

    def test_hotcountry(self):
        expected = "(1) Sam Hunt - Body Like A Back Road\n(2) "
        expected += "Brett Young - In Case You Didn't Know\n(3) "
        expected += "Luke Combs - Hurricane\n(4) Keith Urban Featuring "
        expected += "Carrie Underwood - The Fighter\n(5) Jon Pardi - "
        expected += "Dirt On My Boots\n(6) Dierks Bentley - Black\n(7) "
        expected += "Josh Turner - Hometown Girl\n(8) Darius Rucker - "
        expected += "If I Told You\n(9) Kelsea Ballerini - "
        expected += "Yeah Boy\n(10) Brantley Gilbert - The Weekend"
        self.run_test(expected)


class TestNewAge:
    def run_test(self, expect):
        try:
            result = utils.lookup_newage()
            assert result == expect
        except requests.ConnectionError as e:
            assert str(e) == ('Cannot connect to billboard API')

    def test_newage(self):
        expected = "(1) Armik - Enamor\n"
        expected += "(2) The Piano Guys - Uncharted\n"
        expected += "(3) Enya - Dark Sky Island\n"
        expected += "(4) Armik - Solo Guitar Collection\n"
        expected += "(5) Armik - Romantic Spanish Guitar, Vol. 3\n"
        expected += "(6) Various Artists - Music For Deep Sleep\n"
        expected += "(7) George Winston - Spring Carousel\n"
        expected += "(8) Enigma - The Fall Of A Rebel Angel\n"
        expected += "(9) Various Artists - 111 Tracks\n"
        expected += "(10) Laura Sullivan - Calm Within"
        self.run_test(expected)


class TestBillArtist:
    def run_test(self, command, expected):
        try:
            result = utils.lookup_billArtist(command)
            assert result == expected
        except requests.ConnectionError as e:
            assert str(e) == ('Cannot connect to billboard API')

    def test_billArtist_Taylor_Swift(self):
        self.run_test('Taylor Swift', "Taylor Swift doesn't exist in bill200")

    def test_billArtist_Rhoma_Irama(self):
        self.run_test('Rhoma Irama', "Rhoma Irama doesn't exist in bill200")

    def test_billArtist_Pentatonix(self):
        self.run_test('Pentatonix', "Pentatonix\nPTX Vol. IV: Classics (EP)\nRank #93")


class TestSimilar:
    def test_similar_text(self):
        res = utils.similar_text('Tomorrow is Holiday', 'Tomorrow is Judgement day')
        assert '%' in res

    def test_similar_url(self):
        url1 = 'https://docs.python.org/3/library/unittest.mock.html#quick-guide'
        url2 = 'https://docs.python.org/3/library/unittest.mock.html#unittest.mock.patch'
        res = utils.similar_text(url1, url2)
        assert '%' in res

    def test_connection_error(self):
        res = utils.similar_text('http://www.aku1.com', 'http://www.aku2.com')
        assert res == "Connection Error occurs, please check your url or try again later"

    def test_bound(self):
        fake1 = 'a' * 10000
        fake2 = 'ab' * 5000
        res = utils.similar_text(fake1, fake2)
        assert res == "Your input is too long, please keep below 500 words"


class TestExtractColour:
    EXAMPLE_IMAGGA_JSON = {
        "unsuccessful": [],
        "results": [
            {
                "info": {
                    "background_colors": [
                        {
                            "html_code": "#a9a9a0",
                            "b": "160",
                            "percentage": 67.04,
                            "closest_palette_color": "twig",
                            "closest_palette_distance": 4.36372161759075,
                            "closest_palette_color_html_code": "#a29e92",
                            "closest_palette_color_parent": "grey",
                            "g": "169",
                            "r": "169"
                        }
                    ],
                    "foreground_colors": [
                        {
                            "html_code": "#2d2d21",
                            "b": "33",
                            "percentage": 100.0,
                            "closest_palette_color": "graphite",
                            "closest_palette_distance": 8.829642270845508,
                            "closest_palette_color_html_code": "#3a3536",
                            "closest_palette_color_parent": "black",
                            "g": "45",
                            "r": "45"
                        }
                    ],
                    "color_percent_threshold": 1.75
                },
                "image": "https://api.telegram.org/file/botsomerandomstring/photos/file_2.jpg"
            }
        ]
    }

    EXAMPLE_TELEGRAM_JSON = {"ok": True, "result": {
        "file_id": "id", "file_size": 65661, "file_path": "photo_path"}}

    EXAMPLE_FOREGROUND_RES = "EXTRACT FGCOLOUR\n(45, 45, 33)\n#2d2d21\nPercentage: 100.0%"

    EXAMPLE_BACKGROUND_RES = "EXTRACT BGCOLOUR\n(169, 169, 160)\n#a9a9a0\nPercentage: 67.04%"

    # ExtractColour Class and its methods Tests #
    def test_extract_colour_class(self, mocker):
        # assert state
        EC = utils.extractcolour.ExtractColour
        instance = EC('photo_id')

        # assert get_photo_url()
        fake_response = requests.Response()
        fake_response.status_code = 200
        fake_response._content = bytes(json.dumps(self.EXAMPLE_TELEGRAM_JSON), 'utf-8')
        mocker.patch('requests.get', return_value=fake_response)
        assert instance.get_photo_url() == instance.TELEGRAM_FILE_URL.format(
            config.TELEGRAM_BOT_TOKEN, "photo_path")

        # assert extract()
        mocker.patch('csuibot.utils.extractcolour.ExtractColour.get_photo_url',
                     return_value='photo_path')
        fake_response = requests.Response()
        fake_response.status_code = 200
        fake_response._content = bytes(json.dumps(self.EXAMPLE_IMAGGA_JSON), 'utf-8')
        mocker.patch('requests.get', return_value=fake_response)

        # for state BGCOLOUR
        extracted = instance.extract()
        assert extracted == self.EXAMPLE_BACKGROUND_RES

        # for state FGCOLOUR
        instance.state = EC.FGCOLOUR
        extracted = instance.extract()
        assert extracted == self.EXAMPLE_FOREGROUND_RES

    # utils.extract_colour Tests #
    def test_extract_colour_utils(self, mocker):
        res = 'fake result'
        photo = mocker.Mock()
        attrs = {'file_id': 'somestr'}
        photo.configure_mock(**attrs)
        message = mocker.Mock()
        attrs = {'photo': [photo], 'caption': '/bgcolour'}
        message.configure_mock(**attrs)

        mocker.patch('csuibot.utils.extractcolour.ExtractColour.extract',
                     return_value='fake result')

        assert utils.extract_colour(message) == res

        message = mocker.Mock()
        attrs = {'photo': [photo], 'caption': '/fgcolour'}
        message.configure_mock(**attrs)

        mocker.patch('csuibot.utils.extractcolour.ExtractColour.extract',
                     return_value='fake result')

        assert utils.extract_colour(message) == res


class TestFakeJson:
    def test_response(self):
        expected = (
            '{\n'
            '  "userId": 1,\n'
            '  "id": 1,\n'
            '  "title": "sunt aut facere repellat provident occaecati excepturi'
            ' optio reprehenderit",\n'
            '  "body": "quia et suscipit\\nsuscipit recusandae consequuntur'
            ' expedita et cum\\nreprehenderit molestiae ut ut quas totam\\nnostrum'
            ' rerum est autem sunt rem eveniet architecto"\n'
            '}'
        )

        assert utils.get_fake_json('') == expected

    def test_with_arguments(self):
        try:
            utils.get_fake_json('some_arguments here')
        except ValueError as e:
            assert str(e) == 'Command /fake_json doesn\'t need any arguments'


class TestDetectLang:
    def test_get_type_url(self):
        url = 'http://google.com/'
        assert 'url' == utils.detectlang.DetectLang(url).get_type()

    def test_get_type_text(self):
        text = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.'
        assert 'text' == utils.detectlang.DetectLang(text).get_type()

    def test_text(self, mocker):
        fake_detect_lang = {
            'timestamp': '2017-05-10T14:00:46.882',
            'detectedLangs': [
                {
                    'confidence': 0.9285,
                    'lang': 'ro'
                },
                {
                    'confidence': 0.0714,
                    'lang': 'fr'
                }
            ],
            'time': 1
        }
        mocker.patch(
            'csuibot.utils.detectlang.DetectLang.make_request',
            return_value=fake_detect_lang
        )
        res = utils.lookup_lang(
            'Lorem ipsum dolor sit amet, consectetur adipiscing elit.'
            ' Vestibulum elementum condimentum suscipit. Sed semper,'
            ' dolor eu ultrices interdum, elit quam mollis ligula,'
            ' vel cursus nisi enim sed nunc.'
        )
        assert res == 'Romanian (92.85%)\nFrench (7.14%)\n'

    def test_url(self, mocker):
        fake_detect_lang = {
            'timestamp': '2017-05-10T14:00:46.882',
            'detectedLangs': [
                {
                    'confidence': 1.0,
                    'lang': 'en'
                }
            ],
            'time': 1
        }
        mocker.patch(
            'csuibot.utils.detectlang.DetectLang.make_request',
            return_value=fake_detect_lang
        )
        res = utils.lookup_lang('https://en.wikipedia.org/wiki/Barack_Obama')
        assert res == 'English (100.0%)\n'

    def test_null_argument(self):
        try:
            utils.lookup_lang('')
        except ValueError as e:
            assert str(e) == 'Command /detect_lang need an argument'

    def test_lookup_error(self, mocker):
        fake_detect_lang = {
            'message': 'Unable to download the web page, request got HTTP error code: 503',
            'code': 'error.badGateway',
            'error': True,
            'data': {}
        }
        mocker.patch(
            'csuibot.utils.detectlang.DetectLang.make_request',
            return_value=fake_detect_lang
        )
        try:
            utils.lookup_lang('http://notrealwebsite.com')
        except LookupError as e:
            assert str(e) == (
                'Unable to download the web page, request got HTTP error code: 503'
            )


class TestWeton:
    def test_weton_type_error(self):
        look = utils.lookup_weton("a", "b", "c")
        assert look == "Year/Month/Day is invalid"

    def test_weton_value_error(self):
        look = utils.lookup_weton(1995, 12, 32)
        assert look == "Year/Month/Day is invalid"
