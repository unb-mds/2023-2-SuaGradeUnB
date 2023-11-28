from typing import Any
from requests import Response
from random import choice
from utils import sessions as sns, web_scraping as wbp
from django.core.management.base import BaseCommand
from pathlib import Path
import re
import json
import os


class Command(BaseCommand):
    """Comando para atualizar os arquivos de mock do SIGAA."""

    help = "Atualiza os arquivos do mock com as informações do SIGAA requisitadas."

    def handle(self, *args: Any, **options: Any):
        current_path = Path(__file__).parent.parent.parent.absolute()

        try:
            os.remove(current_path / f"mock/sigaa.html")
            os.remove(current_path / "mock/infos.json")
        except Exception as error:
            print('Error:', error)

        try:
            current_year, current_period = sns.get_current_year_and_period()
            departments = wbp.get_list_of_departments()
            department = choice(departments)

            with open(current_path / f"mock/sigaa.html", "a") as mock_file:
                discipline_scraper = wbp.DisciplineWebScraper(
                    department, current_year, current_period)
                response = discipline_scraper.get_response_from_disciplines_post_request()

                striped_response = self.multiple_replace(
                    self.response_decode(response))
                mock_file.write(striped_response)

            with open(current_path / "mock/infos.json", "a") as info_file:
                data = {
                    "year": current_year,
                    "period": current_period,
                    "department": department
                }
                info_file.write(json.dumps(data))

        except Exception as error:
            print('Não foi possível atualizar o mock!')
            print('Error:', error)

    def multiple_replace(self, text):
        replacement_dict = {
            '\n': '',
            '\t': '',
            '\r': '',
        }
        pattern = re.compile('|'.join(map(re.escape, replacement_dict.keys())))
        return pattern.sub(lambda match: replacement_dict[match.group(0)], text)

    def response_decode(self, response: Response) -> str:
        encoding = response.encoding if response.encoding else 'utf-8'
        return response.content.decode(encoding)
