from sessions import URL, HEADERS, get_response, create_request_session, get_session_cookie
from bs4 import BeautifulSoup
from collections import defaultdict
from typing import List, Optional
import requests.utils
import requests

def get_list_of_departments() -> Optional[List]:
    # Retorna uma lista com os códigos dos departamentos
    response = get_response(create_request_session()) # Get the response from the request session
    soup = BeautifulSoup(response.content, "html.parser") # Create a BeautifulSoup object
    departments = soup.find("select", attrs={"id": "formTurma:inputDepto"}) # Find the <select> tag with id "formTurma:inputDepto"
    
    if departments is None:
        return None
    
    options_tag = departments.find_all("option") # Find all <option> tags (It contains all departments)
    code = [option["value"] for option in options_tag] # Create a list with the value of the option tag (The code of the department)

    return code

class DisciplineWebScraper:
    # Classe que faz o web scraping das disciplinas
    def __init__(self, department: str, year: str, period: str, session=None, cookie=None):
        self.disciplines = defaultdict(list)  # A dictionary with the disciplines
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
        '''Make the web scraping of the disciplines'''
        soup = BeautifulSoup(response.content, "html.parser")
        table = soup.find("table", attrs={"class": "listagem"}) # Find the <table> tag with class "listagem"
        tr = table.find_all("tr") # Find all <tr> tags
        """ print(tr[0])
        print(tr[1])
        print(tr[2]) """
        aux_title_and_code = ""
        if tr is not None:
            for discipline in tr:
                if discipline.find("span", attrs={"class": "tituloDisciplina"}) is not None: #Verify if the <tr> tag has a <span> tag with class "tituloDisciplina"
                    title = discipline.find("span", attrs={"class": "tituloDisciplina"})# Find the <span> tag with class "tituloDisciplina"
                    aux_title_and_code = title.get_text().strip('-')
                elif "linhaPar" in discipline.get("class", []) or "linhaImpar" in discipline.get("class", []):
                    discipline_treated = aux_title_and_code.split(' - ') # Split the title and code of the discipline to get the code and name

                    discipline_code = discipline_treated[0]
                    discipline_name = discipline_treated[1]
                    table_data = discipline.find_all("td") # Find all <td> tags
                    class_code = int(table_data[0].get_text()) # Find the <td> tag with class "turma"
                    teacher_name_with_hours = discipline.find("td",attrs={"class":"nome"}).get_text().strip().strip('\n').split(' ') # Find the <td> tag with class "professor"
                    teacher_name = ' '.join(teacher_name_with_hours[:-1])
                    class_workload = teacher_name_with_hours[-1].replace(('('), '').replace((')'), '')
                    classroom = table_data[7].get_text() # Find the <td> tag with class "sala"
                    schedule = table_data[3].get_text().strip().strip('\n').strip('\t').strip('\r') # Find the <td> tag with class "horario"

print(get_list_of_departments())
scraper = DisciplineWebScraper('640', '2023', '2')
print(scraper)