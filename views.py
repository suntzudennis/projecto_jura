from django.shortcuts import render

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json


def ValidUserDNI( user_dni):
    clave='.........codigo......'
    url = 'http://dniruc.apisperu.com/api/v1/dni/'+user_dni+'?token='+clave

    headers={}
 
    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url)
        data_reniec = json.loads(response.text)
        return data_reniec

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
        return False

     