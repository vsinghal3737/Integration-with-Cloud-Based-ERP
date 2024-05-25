import requests

from bus_logic.utils import handle_error, create_header


class VendorsAPI:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_all_vendors(self, access_token, realm_id):
        url = f"{self.base_url}/v3/company/{realm_id}/query"
        query = "SELECT * FROM Vendor"
        response = requests.get(url, headers=create_header(access_token), params={'query': query})
        handle_error(response)
        return response.json().get('QueryResponse', {}).get('Vendor', [])

    def get_vendor_by_id(self, vendor_id, access_token, realm_id):
        url = f"{self.base_url}/v3/company/{realm_id}/vendor/{vendor_id}"
        response = requests.get(url, headers=create_header(access_token))
        handle_error(response)
        return response.json()

    def update_vendor(self, vendor_id, update_data, access_token, realm_id):
        # Fetch the latest vendor data to get the current SyncToken
        current_vendor_data = self.get_vendor_by_id(vendor_id)
        current_sync_token = current_vendor_data['Vendor']['SyncToken']
        update_data['SyncToken'] = current_sync_token

        url = f"{self.base_url}/v3/company/{realm_id}/vendor/"
        response = requests.post(url, headers=create_header(access_token), json=update_data)
        handle_error(response)
        return response.json()
