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
    session = requests.Session() # Create a persistent request session
    retry = Retry(connect=3, backoff_factor=0.5) # Create a retry object
    adapter = HTTPAdapter(max_retries=retry) # Try to make the request 3 times
    session.mount('https://', adapter) # Mount the adapter to the session
    return session

'''Get the response from the request session'''
def get_response(session: requests.Session) -> requests.Response:
    response = session.get(url=URL, headers=HEADERS) # Make a get request to the url
    return response


def get_session_cookie(session: requests.Session) -> requests.cookies.RequestsCookieJar:
    '''Get the cookie from the request session'''
    response = get_response(session) # Get the response from the request session
    cookie = response.cookies.get_dict() # Get the cookie from the response
    cookie_jar = requests.cookies.RequestsCookieJar() # Create a cookie jar
    cookie_jar.update(cookie) # Update the cookie jar with the cookie
    return cookie_jar


def get_current_year_and_period():
    '''Get the current year and period'''
    today_date = datetime.now() # Get the current date
    current_year = today_date.year # Get the current year
    if datetime(current_year, 5, 1) <= today_date <= datetime(current_year, 10, 30):
        '''If the current date is between May 1 and October 30, the period is 2, else the period is 1'''
        period = "2"
    else:
        period = "1"
    return [current_year, period]
