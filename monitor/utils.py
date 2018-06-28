from django.conf import settings
import requests

API_KEY = settings.ETHPLORER_API_KEY


def get_token_info(address):
    s = requests.Session()
    r = s.get(
        f"http://api.ethplorer.io/getTokenInfo/{address}?apiKey={API_KEY}")
    if r.status_code != 200:
        raise Exception(f"GET TOKEN INFO STATUSCODE _ {r.status_code}")
    data = r.json()
    # TODO обработать ошибки
    return data


