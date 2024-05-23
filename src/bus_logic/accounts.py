import requests


def _handle_error(response):
    if response.status_code not in [200, 201]:
        raise Exception(f"API request failed with status code {response.status_code}: {response.json()}")


class AccountAPI:
    def __init__(self, base_url, access_token, realm_id):
        self.base_url = base_url
        self.access_token = access_token
        self.realm_id = realm_id
        self.headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def get_all_accounts(self):
        url = f"{self.base_url}/v3/company/{self.realm_id}/query"
        query = "SELECT * FROM Account"
        response = requests.get(url, headers=self.headers, params={'query': query})
        _handle_error(response)
        return response.json().get('QueryResponse', {}).get('Account', [])

    def get_account_by_id(self, account_id):
        url = f"{self.base_url}/v3/company/{self.realm_id}/account/{account_id}"
        response = requests.get(url, headers=self.headers)
        _handle_error(response)
        return response.json()

    def update_account(self, account_id, update_data):
        # Fetch the latest account data to get the current SyncToken
        current_account_data = self.get_account_by_id(account_id)
        current_sync_token = current_account_data['Account']['SyncToken']
        update_data['SyncToken'] = current_sync_token

        url = f"{self.base_url}/v3/company/{self.realm_id}/account/"
        response = requests.post(url, headers=self.headers, json=update_data)
        _handle_error(response)
        return response.json()
