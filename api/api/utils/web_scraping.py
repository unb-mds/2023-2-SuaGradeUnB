import sessions
from sessions import create_request_session
from sessions import URL
from sessions import HEADERS
from bs4 import BeautifulSoup
import requests
import requests.utils


def get_list_of_departments():
    response = sessions.get_response(create_request_session())
    soup = BeautifulSoup(response.content, "html.parser")
    departments = soup.find("select", attrs={"id": "formTurma:inputDepto"})
    if departments is not None:
        options_tag = departments.find_all("option")
        code = [option["value"] for option in options_tag]
        department_dict = dict()
        return code
    else:
        return None


class DisciplineWebScraper:
    def __init__(self, department: str, year: str, period: str, session=None, cookie=None):
        self.url = URL
        self.department = department
        self.year = year
        self.period = period
        self.data = {
            "formTurma":	"formTurma",
            "formTurma:inputNivel":	"",
            "formTurma:inputDepto":	self.department,
            "formTurma:inputAno":	self.year,
            "formTurma:inputPeriodo":	self.period,
            "formTurma:j_id_jsp_1370969402_11":	"Buscar",
            "javax.faces.ViewState":	"j_id1"}

        if session is None:
            self.session = sessions.create_request_session()
        else:
            self.session = session
        if cookie is None:
            self.cookie = sessions.get_session_cookie(self.session)
        else:
            self.cookie = cookie

    def get_response_from_disciplines_post_request(self):
        response = self.session.post(
            url=self.url, headers=HEADERS, cookies=self.cookie, data=self.data)
        return response

    def make_web_scraping_of_disciplines(self, response):
        '''Still necessary to implement this method'''

"""
This is a test of the DisciplineWebScraper class

department = get_list_of_departments()
webscrap = DisciplineWebScraper(department[2], "2023", "2")
discipline = webscrap.get_response_from_disciplines_post_request()
webscrap.make_web_scraping_of_disciplines(discipline)
 """
