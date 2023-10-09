import json
import requests
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup
from urllib3.util.retry import Retry

URL = "https://sigaa.unb.br/sigaa/public/turmas/listar.jsf"

""" response = requests.get(URL)
response.encoding = 'utf-8'
print("GET response:\n", response)
response_2 = requests.post(URL)
response_2.encoding = 'utf-8'
print("POST response:\n", response_2) """


def create_request_session() -> requests.Session:
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('https://', adapter)
    return session


def get_session_cookie(session: requests.Session)-> str:

    response = session.get(url=URL,)
    cookie = response.cookies.get_dict()
    return json.dumps(cookie)
