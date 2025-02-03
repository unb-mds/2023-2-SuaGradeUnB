from string import ascii_letters as letters, digits
from bs4 import BeautifulSoup
from collections import defaultdict
from rest_framework.test import APITestCase
from utils import web_scraping as wbp
from django.urls import reverse
from pathlib import Path
from django.core.cache import cache
import random
import json


class WebScrapingTest(APITestCase):

    def setUp(self):
        # Clean cache
        for key in cache.keys("*"):
            cache.delete(key)

    def cookie(self):
        cookie = ""
        for _ in range(32):
            cookie += random.choice(letters + digits)

        return cookie

    def generate_args(self, path_name: str):
        current_path = Path(__file__).parents[1].absolute()
        infos_path = current_path / f"mock/infos.json"

        with open(infos_path) as json_file:
            data = json.load(json_file)

            year = data.get('year')
            period = data.get('period')
            department = data.get('department')

        url = reverse(f'utils:sigaa', kwargs={"path": path_name})
        args = [department, year, period, url, self.client, self.cookie()]

        return args

    def make_disciplines_request(self, path_name: str):
        args = self.generate_args(path_name)

        scraper = wbp.DisciplineWebScraper(*args)
        disciplines = scraper.get_disciplines()

        return disciplines

    def create_fingerprint(self, path_name: str):
        args = self.generate_args(path_name)

        scraper = wbp.DisciplineWebScraper(*args)

        return scraper.create_page_fingerprint()

    def test_get_list_of_departments(self):
        response = self.client.get(
            reverse('utils:sigaa', kwargs={"path": "sigaa"}))

        departments = wbp.get_list_of_departments(response)
        self.assertEqual(type(list()), type(departments))
        if len(departments):
            self.assertEqual(type(str()), type(departments[0]))

    def test_get_list_of_departments_when_empty(self):
        response = self.client.get(
            reverse('utils:sigaa', kwargs={"path": "empty"}))

        departments = wbp.get_list_of_departments(response)
        self.assertIsNone(departments)

    def test_get_department_disciplines(self):
        disciplines = self.make_disciplines_request('sigaa')

        self.assertEqual(type(disciplines), type(defaultdict(str)))
        if len(disciplines):
            keys = list(disciplines.keys())
            class_discipline = disciplines.get(keys[0])[0]

            self.assertTrue('name' in class_discipline)
            self.assertTrue('class_code' in class_discipline)
            self.assertTrue('teachers' in class_discipline)
            self.assertTrue('schedule' in class_discipline)
            self.assertTrue('days' in class_discipline)

    def test_get_department_disciplines_when_empty(self):
        disciplines = self.make_disciplines_request('empty')

        self.assertFalse(len(disciplines))

    def test_get_department_disciplines_when_without_tr_html_tag(self):
        disciplines = self.make_disciplines_request('table')

        self.assertFalse(len(disciplines))

    def test_do_not_find_nonexisting_fingerprint(self):
        cache_value = cache.get('0000/2023.1')

        self.assertEqual(cache_value, None)

    def test_find_existing_fingerprint(self):
        fingerprint = self.create_fingerprint('sigaa')

        key = '0000/2023.1'
        cache.set(key, fingerprint)

        self.assertEqual(cache.get(key), fingerprint)

    def test_find_existing_fingerprint_from_empty(self):
        fingerprint = self.create_fingerprint('empty')

        key = '0001/2023.1'
        cache.set(key, fingerprint)

        self.assertEqual(cache.get(key), 'not_content')
    
    def test_make_disciplines_rows_is_None(self):
        self.scraper = wbp.DisciplineWebScraper('0000','2024','2')
        self.scraper.make_disciplines(None)
        self.assertTrue(len(self.scraper.disciplines) == 0)
    
    def test_make_disciplines_rows_is_empty(self):
        self.scraper = wbp.DisciplineWebScraper('0000','2024','2')
        self.scraper.make_disciplines('')
        self.assertTrue(len(self.scraper.disciplines) == 0)
    
    def test_make_disciplines_linhaPar(self):
        test_html = """
        <html>
            <body>
                <table class="listagem">
                    <tr>
                        <td>
                            <span class="tituloDisciplina">ABC0000 - NOME DA MATERIA</span>
                        </td>
                    </tr>
                    <tr class="linhaPar">
                        <td align="center" class="turma"> 01</td>
                        <td align="center" class="anoPeriodo">2023.2</td>
                        <td class="nome"> Professor (20h) </td>
                        <td> 4M1234 </td>
                        <td> </td>
                        <td style="text-align: center;">42</td>
                        <td style="text-align: center;">0</td>
                        <td align="center" nowrap="nowrap"> TES - Módulo X sala Y</td>
                        <td style="text-align: center;">0</td>
                        <td style="text-align: center;">0</td>
                    </tr>
                </table>
            </body>
        </html>
        """
        self.scraper = wbp.DisciplineWebScraper('650','2023','2')
        soup = BeautifulSoup(test_html, 'html.parser')
        rows = soup.find_all('tr')
        self.scraper.make_disciplines(rows)
        disciplines = self.scraper.get_disciplines()
        self.assertIn("ABC0000",disciplines)
        self.assertTrue(len(disciplines["ABC0000"]) == 1)

    def test_make_disciplines_linhaImpar(self):
        test_html = """
        <html>
            <body>
                <table class="listagem">
                    <tr>
                        <td>
                            <span class="tituloDisciplina">ABC0000 - NOME DA MATERIA</span>
                        </td>
                    </tr>
                    <tr class="linhaImpar">
                        <td align="center" class="turma"> 01</td>
                        <td align="center" class="anoPeriodo">2023.2</td>
                        <td class="nome"> Professor (20h) </td>
                        <td> 4M1234 </td>
                        <td> </td>
                        <td style="text-align: center;">42</td>
                        <td style="text-align: center;">0</td>
                        <td align="center" nowrap="nowrap"> TES - Módulo X sala Y</td>
                        <td style="text-align: center;">0</td>
                        <td style="text-align: center;">0</td>
                    </tr>
                </table>
            </body>
        </html>
        """
        self.scraper = wbp.DisciplineWebScraper('650','2023','2')
        soup = BeautifulSoup(test_html, 'html.parser')
        rows = soup.find_all('tr')
        self.scraper.make_disciplines(rows)
        disciplines = self.scraper.get_disciplines()
        self.assertIn("ABC0000",disciplines)
        self.assertTrue(len(disciplines["ABC0000"]) == 1)
    
    def test_make_disciplines_without_class_linha(self):
        test_html = """
        <html>
            <body>
                <table class="listagem">
                    <tr>
                        <td>
                            <span class="tituloDisciplina">ABC0000 - NOME DA MATERIA</span>
                        </td>
                    </tr>
                    <tr class="invalida">
                        <td align="center" class="turma"> 01</td>
                        <td align="center" class="anoPeriodo">2023.2</td>
                        <td class="nome"> Professor (20h) </td>
                        <td> 4M1234 </td>
                        <td> </td>
                        <td style="text-align: center;">42</td>
                        <td style="text-align: center;">0</td>
                        <td align="center" nowrap="nowrap"> TES - Módulo X sala Y</td>
                        <td style="text-align: center;">0</td>
                        <td style="text-align: center;">0</td>
                    </tr>
                </table>
            </body>
        </html>
        """
        self.scraper = wbp.DisciplineWebScraper('650','2023','2')
        soup = BeautifulSoup(test_html, 'html.parser')
        rows = soup.find_all('tr')
        self.scraper.make_disciplines(rows)
        disciplines = self.scraper.get_disciplines()
        self.assertTrue(len(disciplines) == 0)