from requests import Session, Response, cookies
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from datetime import datetime
from typing import List

URL = "https://sigaa.unb.br/sigaa/public/turmas/listar.jsf"
HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
}

'''Create a request session with retry and backoff_factor'''
def create_request_session() -> Session:
    session = Session() # Create a persistent request session
    retry = Retry(connect=3, backoff_factor=0.5) # Create a retry object
    adapter = HTTPAdapter(max_retries=retry) # Try to make the request 3 times
    session.mount('https://', adapter) # Mount the adapter to the session

    return session

'''Get the response from the request session'''
def get_response(session: Session) -> Response:
    response = session.get(url=URL, headers=HEADERS) # Make a get request to the url

    return response

def get_session_cookie(session: Session) -> cookies.RequestsCookieJar:
    '''Get the cookie from the request session'''
    response = get_response(session) # Get the response from the request session
    cookie = response.cookies.get_dict() # Get the cookie from the response
    cookie_jar = cookies.RequestsCookieJar() # Create a cookie jar
    cookie_jar.update(cookie) # Update the cookie jar with the cookie

    return cookie_jar

def get_current_year_and_period() -> List[int | str]:
    # Pega o ano e o período atual
    current_date = datetime.now() 
    current_year = current_date.year
    period = "1"

    # Se a data atual estiver entre 1 de maio e 30 de outubro, o período é 2.
    if datetime(current_year, 5, 1) <= current_date <= datetime(current_year, 10, 30):
        period = "2"

    return [current_year, period]