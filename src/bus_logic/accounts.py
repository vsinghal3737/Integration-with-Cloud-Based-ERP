import requests

from src.bus_logic.utils import create_header, handle_error


class AccountAPI:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_all_accounts(self, access_token, realm_id):
        url = f"{self.base_url}/v3/company/{realm_id}/query"
        query = "SELECT * FROM Account"
        response = requests.get(url, headers=create_header(access_token), params={'query': query})
        handle_error(response)
        return response.json().get('QueryResponse', {}).get('Account', [])

    def get_account_by_id(self, account_id, access_token, realm_id):
        url = f"{self.base_url}/v3/company/{realm_id}/account/{account_id}"
        response = requests.get(url, headers=create_header(access_token))
        handle_error(response)
        return response.json()

    def update_account(self, account_id, update_data, access_token, realm_id):
        # Fetch the latest account data to get the current SyncToken
        current_account_data = self.get_account_by_id(account_id)
        current_sync_token = current_account_data['Account']['SyncToken']
        update_data['SyncToken'] = current_sync_token

        url = f"{self.base_url}/v3/company/{realm_id}/account/"
        response = requests.post(url, headers=create_header(access_token), json=update_data)
        handle_error(response)
        return response.json()
