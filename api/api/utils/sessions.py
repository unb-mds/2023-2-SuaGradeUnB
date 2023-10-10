from datetime import datetime
import json
import requests
import requests.utils
import requests.cookies
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# The url of the web page
URL = "https://sigaa.unb.br/sigaa/public/turmas/listar.jsf"
# The headers of the request
HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
}

'''Create a request session with retry and backoff_factor'''
def create_request_session() -> requests.Session:
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('https://', adapter)
    return session

'''Get the response from the request session'''
def get_response(session: requests.Session) -> requests.Response:
    response = session.get(url=URL, headers=HEADERS)
    return response


def get_session_cookie(session: requests.Session) -> requests.cookies.RequestsCookieJar:
    '''Get the cookie from the request session'''
    response = get_response(session)
    cookie = response.cookies.get_dict()
    cookie_jar = requests.cookies.RequestsCookieJar()
    cookie_jar.update(cookie)
    return cookie_jar


def get_current_year_and_period():
    '''Get the current year and period'''
    today_date = datetime.now()
    current_year = today_date.year
    if datetime(current_year, 5, 1) <= today_date <= datetime(current_year, 10, 30):
        period = "2"
    else:
        period = "1"
    return [current_year, period]
