import requests
import base64
import config
from urllib.parse import urlencode  # Add this import statement


class StockService:
    def __init__(self, base_url):
        self.base_url = base_url

    def login(self, username, password):
        auth = 'Basic ' + base64.b64encode(f'bourseClient:bourseSecret'.encode('utf-8')).decode('utf-8')
        headers = {
            'Authorization': auth,
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'client_id': 'bourseClient',
            'username': username,
            'password': password,
            'grant_type': 'password'
        }
        try:
            response = requests.post(f"{self.base_url}/oauth/token", headers=headers, data=data)
            response.raise_for_status()
            return response.json()['access_token']
        except requests.exceptions.RequestException as e:
            raise Exception(f"Login failed: {e}")

    def get_valeurs_by_groupe(self, token, groupe):
        headers = {
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'codeGroupe': groupe
        }
        try:
            # Encode the data in URL-encoded form
            encoded_data = urlencode(data)

            response = requests.post(f"{self.base_url}/services/rest/WsMarche/getValeursByGroupe", headers=headers,
                                     data=encoded_data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error retrieving group data: {e}")

    def get_stock_by_symbol(self, token, groupe, symbol):
        try:
            # Retrieve stock values for the given group
            stock_values = self.get_valeurs_by_groupe(token, groupe)

            # Check if stock_values is not None and symbol exists in the response
            if stock_values and any(valeur['libelle'] == symbol for valeur in stock_values['content']):
                for valeur in stock_values['content']:
                    if valeur['libelle'] == symbol:
                        return valeur['cours']  # Return the price if stock symbol matches
            else:
                return None  # Symbol not found or stock_values is None
        except Exception as e:
            # Handle any exceptions gracefully
            print(f"Error retrieving stock price: {e}")
            return None

    def get_indices(self, token):
        headers = {
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        try:
            response = requests.post(f"{self.base_url}/services/rest/WsMarche/getAllIndices", headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error retrieving indices: {e}")

    def get_palmares_baisse(self, token):
        headers = {
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        try:
            response = requests.get(f"{self.base_url}/services/rest/WsPalmares/findBaisse", headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error retrieving palmares baisse: {e}")

    def get_palmares_hausse(self, token):
        headers = {
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        try:
            response = requests.get(f"{self.base_url}/services/rest/WsPalmares/findFort", headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error retrieving palmares hausse: {e}")




