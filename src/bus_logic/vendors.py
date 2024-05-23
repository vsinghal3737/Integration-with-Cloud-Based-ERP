import requests


def _handle_error(response):
    if response.status_code not in [200, 201]:
        raise Exception(f"API request failed with status code {response.status_code}: {response.json()}")


class VendorsAPI:
    def __init__(self, base_url, access_token, realm_id):
        self.base_url = base_url
        self.access_token = access_token
        self.realm_id = realm_id
        self.headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def get_all_vendors(self):
        url = f"{self.base_url}/v3/company/{self.realm_id}/query"
        query = "SELECT * FROM Vendor"
        response = requests.get(url, headers=self.headers, params={'query': query})
        _handle_error(response)
        return response.json().get('QueryResponse', {}).get('Vendor', [])

    def get_vendor_by_id(self, vendor_id):
        url = f"{self.base_url}/v3/company/{self.realm_id}/vendor/{vendor_id}"
        response = requests.get(url, headers=self.headers)
        _handle_error(response)
        return response.json()

    def update_vendor(self, vendor_id, update_data):
        # Fetch the latest vendor data to get the current SyncToken
        current_vendor_data = self.get_vendor_by_id(vendor_id)
        current_sync_token = current_vendor_data['Vendor']['SyncToken']
        update_data['SyncToken'] = current_sync_token

        url = f"{self.base_url}/v3/company/{self.realm_id}/vendor/"
        response = requests.post(url, headers=self.headers, json=update_data)
        _handle_error(response)
        return response.json()
