from .sessions import URL, HEADERS, create_request_session, get_session_cookie, get_response
from bs4 import BeautifulSoup
from collections import defaultdict
from typing import List, Optional, Iterator
from re import findall, finditer
from utils.functions import multiple_replace
import requests.utils
import requests
import hashlib

'''
Modo de uso:

1. É necessário ter o código do departamento escolhido.
Logo, temos a função get_list_of_departments() que retorna uma lista com os códigos dos departamentos.
2. É necessário ter o ano e o período.
3. É necessário ter uma instância da classe DisciplineWebScraper.

- Exemplo:
    department = "650"
    year = "2023"
    period = "2"
    disciplines = DisciplineWebScraper(department, year, period)
    disciplines.get_disciplines() # Retorna um dicionário com as disciplinas
'''


def get_list_of_departments(response=get_response(create_request_session())) -> Optional[tuple[list[str], list[str]]]:
    """Obtem a lista de departamentos da UnB."""
    soup = BeautifulSoup(
        response.content, "html.parser")  # Create a BeautifulSoup object
    # Find the <select> tag with id "formTurma:inputDepto"
    departments = soup.find("select", attrs={"id": "formTurma:inputDepto"})

    if departments is None:
        return None

    # Find all <option> tags (It contains all departments)
    options_tag = departments.find_all("option")
    department_ids = []
    departments_names = []
    for option in options_tag:
        value = option["value"]

        if (value != "0"):
            department_ids.append(value)
            departments_names.append(
                option.get_text().replace("\n", "").replace("\r", "").replace("\t", "").replace("- BRASÍLIA", ""))
    return department_ids, departments_names


class DisciplineWebScraper:
    # Classe que faz o web scraping das disciplinas
    def __init__(self, department: str, year: str, period: str, url=URL, session=None, cookie=None):
        self.disciplines: defaultdict[str, List[dict]] = defaultdict(
            list)  # A dictionary with the disciplines
        self.department = department  # The department code
        self.period = period  # 1 for first semester and 2 for second semester
        self.year = year
        self.url = url  # The url of the web page
        self.data = {  # This data is necessary to make the post request
            "formTurma": "formTurma",
            "formTurma:inputNivel":	"",
            "formTurma:inputDepto":	self.department,
            "formTurma:inputAno": self.year,
            "formTurma:inputPeriodo": self.period,
            "formTurma:j_id_jsp_1370969402_11":	"Buscar",
            "javax.faces.ViewState": "j_id1"
        }

        if session is None:  # pragma: no cover
            self.session = create_request_session()  # Create a request session
        else:
            self.session = session

        if cookie is None:  # pragma: no cover
            self.cookie = get_session_cookie(self.session)
        else:
            self.cookie = cookie

        self.response = None

    def get_response_from_disciplines_post_request(self) -> requests.Response:
        # Faz uma requisição POST para obter a resposta das turmas disponíveis
        self.response = self.session.post(
            self.url,
            headers=HEADERS,
            cookies=self.cookie,
            data=self.data
        )

    def get_teachers(self, data: list) -> list:
        teachers = []

        for teacher in data:
            teacher = teacher.replace("\n", "").replace(
                "\r", "").replace("\t", "")
            content = teacher.split('(')

            if (len(content) < 2):
                continue

            teachers.append(content[0].strip())

        if len(teachers) == 0:  # pragma: no cover
            teachers.append("A definir")

        return teachers

    def get_schedules_and_intervals(self, data: str) -> list[list[str], list[tuple[int, int]]]:
        regex = "\d+[MTN]\d+"
        occurrences = finditer(regex, data)
        values = [[], []]

        for value in occurrences:
            values[0].append(value.group())
            values[1].append((value.start(), value.end()))

        return values

    def check_start(self, *args, **kwargs) -> bool:
        start_index = kwargs.get("start_index")
        last_included = kwargs.get("last_included")

        end_interval = kwargs.get("interval")[1]
        already_included = kwargs["index"] + 1 > last_included
        value_start_check = kwargs.get("value").start() > end_interval

        return start_index is None and value_start_check and already_included

    def check_end(self, *args, **kwargs) -> bool:
        start_interval = kwargs.get("interval")[0]
        value_start_check = kwargs.get("value").start() < start_interval

        return value_start_check

    def get_start_index(self, intervals, last_included, value) -> Optional[int]:
        start_index = None

        for index, interval in enumerate(intervals):
            if self.check_start(start_index=start_index, last_included=last_included, interval=interval, index=index, value=value):
                start_index = index + 1

        return start_index

    def get_end_index(self, intervals, value) -> int:
        for index, interval in enumerate(intervals):
            if self.check_end(interval=interval, index=index, value=value):
                return index
        else:
            return len(intervals)

    def get_start_and_end(self, value: Iterator, intervals: list[tuple[int, int]], last_included: int) -> tuple[int, int]:
        start_index = self.get_start_index(intervals, last_included, value)
        end_index = self.get_end_index(intervals, value)
        return start_index, end_index

    def get_values_from_special_dates(self, occurrences: Iterator, intervals: list[tuple[int, int]]) -> list[list[str, int, int]]:
        last_included = -1
        values = []

        for value in occurrences:
            date = value.group()
            start, end = self.get_start_and_end(
                value, intervals, last_included)
            last_included = end
            values.append([date, start, end])

        return values

    def get_special_dates(self, data: str, intervals: list[tuple[int, int]]) -> list[list[str, int, int]]:
        date_format = "\d{2}\/\d{2}\/\d{4}"
        regex = f"{date_format}\s\-\s{date_format}"
        occurrences = finditer(regex, data)
        values = self.get_values_from_special_dates(occurrences, intervals)

        return values

    def get_week_days(self, data: str) -> list:
        hours_format = "\d+\:\d+"
        regex = f"[A-Z]\w?[a-z|ç]+\-?[a-z]*\s{hours_format}\sàs\s{hours_format}"
        occurrences = findall(regex, data)

        return occurrences

    def make_disciplines(self, rows: str) -> None:
        if rows is None or not len(rows):
            return None

        aux_title_and_code = ""

        for discipline in rows:
            if discipline.find("span", attrs={"class": "tituloDisciplina"}) is not None:
                title = discipline.find(
                    "span", attrs={"class": "tituloDisciplina"})
                aux_title_and_code = title.get_text().strip('-')

            elif "linhaPar" in discipline.get("class", []) or "linhaImpar" in discipline.get("class", []):
                code, name = aux_title_and_code.split(' - ', 1)
                tables_data = discipline.find_all("td")

                '''
                    Parâmetros a serem salvos para cada disciplina:

                    Chave: Código da disciplina (string)
                    Valor: Lista de dicionários com as seguintes chaves:
                    - name: Nome da disciplina (string)
                    - class: Turma (str)
                    - teachers: Nome dos professores (Lista de strings)
                    - schedule: Código do horário (string)
                    - days: Dias da semana com horário (Lista de strings)
                '''

                teachers_with_workload = discipline.find(
                    "td", attrs={"class": "nome"}).get_text().strip().strip().split(')')
                schedule_context = tables_data[3].get_text().strip()

                class_code = tables_data[0].get_text().strip()
                classroom = tables_data[7].get_text().strip()
                schedules_and_intervals = self.get_schedules_and_intervals(
                    schedule_context)
                special_dates = self.get_special_dates(
                    schedule_context, schedules_and_intervals[1])
                days = self.get_week_days(schedule_context)
                teachers = self.get_teachers(teachers_with_workload)

                self.disciplines[code].append({
                    "name": name,
                    "class_code": class_code,
                    "teachers": teachers,
                    "classroom": classroom,
                    "schedule": " ".join(schedules_and_intervals[0]),
                    "special_dates": special_dates,
                    "days": days
                })

    def retrieve_classes_tables(self, response):
        # Faz o web scraping das disciplinas
        soup = BeautifulSoup(response.content, "html.parser")
        # Find the <table> tag with class "listagem"
        tables = soup.find("table", attrs={"class": "listagem"})

        if tables is None:
            return None

        return tables

    def create_page_fingerprint(self):
        if not self.response:
            self.get_response_from_disciplines_post_request()

        tables = self.retrieve_classes_tables(self.response)
        if not tables:
            return "not_content"

        treated_tables = multiple_replace(tables.get_text(), replacement={
            '\n': '',
            '\t': '',
            '\r': '',
            ' ': ''
        }).strip()

        return hashlib.sha256(treated_tables.encode('utf-8')).hexdigest()

    def make_web_scraping_of_disciplines(self, response) -> None:
        tables = self.retrieve_classes_tables(response)

        if not tables:
            return None

        table_rows = tables.find_all("tr")  # Find all <tr> tags

        self.make_disciplines(table_rows)

    def get_disciplines(self) -> defaultdict[str, List[dict]]:
        # Retorna um dicionário com as disciplinas
        if not self.response:
            self.get_response_from_disciplines_post_request()
        self.make_web_scraping_of_disciplines(self.response)

        return self.disciplines
