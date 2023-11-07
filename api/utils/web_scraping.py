from .sessions import URL, HEADERS, get_response, create_request_session, get_session_cookie
from bs4 import BeautifulSoup
from collections import defaultdict
from typing import List, Optional
from re import search
import requests.utils
import requests

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

def get_list_of_departments(response = get_response(create_request_session())) -> Optional[List]:
    """Obtem a lista de departamentos da UnB."""
    soup = BeautifulSoup(response.content, "html.parser") # Create a BeautifulSoup object
    departments = soup.find("select", attrs={"id": "formTurma:inputDepto"}) # Find the <select> tag with id "formTurma:inputDepto"

    if departments is None:
        return None

    options_tag = departments.find_all("option") # Find all <option> tags (It contains all departments)
    department_ids = []

    for option in options_tag:
        value = option["value"]

        if(value != "0"):
            department_ids.append(value)

    return department_ids

def get_department_disciplines(department_id: str, current_year: str, current_period: str):
    """Obtem as disciplinas de um departamento"""
    discipline_scraper = DisciplineWebScraper(department_id, current_year, current_period)
    disciplines = discipline_scraper.get_disciplines()

    return disciplines

class DisciplineWebScraper:
    # Classe que faz o web scraping das disciplinas
    def __init__(self, department: str, year: str, period: str, session=None, cookie=None):
        self.disciplines: defaultdict[str, List[dict]] = defaultdict(list)  # A dictionary with the disciplines
        self.department = department  # The department code
        self.period = period  # 1 for first semester and 2 for second semester
        self.year = year
        self.url = URL  # The url of the web page
        self.data = {  # This data is necessary to make the post request
            "formTurma": "formTurma",
            "formTurma:inputNivel":	"",
            "formTurma:inputDepto":	self.department,
            "formTurma:inputAno": self.year,
            "formTurma:inputPeriodo": self.period,
            "formTurma:j_id_jsp_1370969402_11":	"Buscar",
            "javax.faces.ViewState": "j_id1"
        }

        if session is None:
            self.session = create_request_session()  # Create a request session
        else:
            self.session = session

        if cookie is None:
            self.cookie = get_session_cookie(self.session)
        else:
            self.cookie = cookie

    def get_response_from_disciplines_post_request(self) -> requests.Response:
        # Faz uma requisição POST para obter a resposta das turmas disponíveis
        response = self.session.post(
            url=self.url,
            headers=HEADERS,
            cookies=self.cookie,
            data=self.data
        )

        return response

    def make_web_scraping_of_disciplines(self, response):
        # Faz o web scraping das disciplinas
        soup = BeautifulSoup(response.content, "html.parser")
        tables = soup.find("table", attrs={"class": "listagem"}) # Find the <table> tag with class "listagem"

        if tables is None:
            return None

        table_rows = tables.find_all("tr") # Find all <tr> tags

        aux_title_and_code = ""

        if table_rows is None:
            return None

        for discipline in table_rows:
            if discipline.find("span", attrs={"class": "tituloDisciplina"}) is not None:
                title = discipline.find("span", attrs={"class": "tituloDisciplina"})
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
                    - workload: Carga horária (int). Se não houver, o valor é -1!
                    - classroom: Sala (string)
                    - schedule: Código do horário (string)
                    - days: Dias da semana com horário (Lista de strings)
                '''

                teachers_with_workload = discipline.find("td",attrs={"class":"nome"}).get_text().strip().strip().split(')')
                teachers = []
                days = []

                for teacher in teachers_with_workload:
                    teacher = teacher.replace("\n", "").replace("\r", "").replace("\t", "")
                    content = teacher.split('(')

                    if(len(content) < 2):
                        continue

                    teachers.append(content[0].strip())

                if len(teachers) == 0:
                    teachers.append("A definir")

                class_code = tables_data[0].get_text()
                classroom = tables_data[7].get_text().strip()

                schedule = "A definir"
                week_days = "A definir"

                if len(tables_data[3].get_text().strip().split(maxsplit=1)) == 2:
                    schedule, week_days = tables_data[3].get_text().strip().split(maxsplit=1)

                workload = self.calc_hours(schedule)
                sep = week_days.rfind("\t")

                if(sep != -1):
                    week_days = week_days[sep+1:]

                for character in week_days:
                    if(character.isupper()):
                        days.append(character)
                    else:
                        days[-1] += character

                self.disciplines[code].append({
                    "name": name,
                    "class_code": class_code,
                    "teachers": teachers,
                    "workload": workload,
                    "classroom": classroom,
                    "schedule": schedule,
                    "days": days
                })

    def calc_hours(self, schedule: str) -> int:
        # Calcula a carga horária de uma disciplina
        match = search(r'[a-zA-Z]', schedule)
        hours = match.start() * (len(schedule) - match.start() - 1) * 15

        return hours

    def get_disciplines(self):
        # Retorna um dicionário com as disciplinas
        response = self.get_response_from_disciplines_post_request()
        self.make_web_scraping_of_disciplines(response)

        return self.disciplines
