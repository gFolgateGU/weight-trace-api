from requests.exceptions import RequestException
import requests

class HttpRequest:
    def __init__(self):
        pass

    def get_data(self, http_endpoint, http_auth_hdr=None):
        try:
            response = requests.get(http_endpoint, headers=http_auth_hdr)
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                print("Request failed with code: ", response.status_code)
                data = {}
                return data

        except RequestException as e:
            print('An error occurred during the request', e)
            data = {}


