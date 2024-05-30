import requests

from bus_logic.utils import handle_error, create_header


class VendorsAPI:
    """
    A class to interact with the Vendor API of the financial service.
    """

    def __init__(self, base_url):
        self.base_url = base_url

    def get_all_vendors(self, access_token, realm_id):
        """
        Retrieves all vendors.

        :param access_token: The access token for authentication.
        :param realm_id: The realm ID of the company.
        :return: A list of vendors.
        """
        url = f"{self.base_url}/v3/company/{realm_id}/query"
        query = "SELECT * FROM Vendor"
        response = requests.get(url, headers=create_header(access_token), params={'query': query})
        handle_error(response)
        return response.json().get('QueryResponse', {}).get('Vendor', [])

    def get_vendor_by_id(self, vendor_id, access_token, realm_id):
        """
        Retrieves a vendor by its ID.

        :param vendor_id: The ID of the vendor.
        :param access_token: The access token for authentication.
        :param realm_id: The realm ID of the company.
        :return: The vendor data as a dictionary.
        """
        url = f"{self.base_url}/v3/company/{realm_id}/vendor/{vendor_id}"
        response = requests.get(url, headers=create_header(access_token))
        handle_error(response)
        return response.json()

    def update_vendor(self, vendor_id, update_data, access_token, realm_id):
        """
        Updates a vendor with new data.

        :param vendor_id: The ID of the vendor to update.
        :param update_data: The data to update the vendor with.
        :param access_token: The access token for authentication.
        :param realm_id: The realm ID of the company.
        :return: The updated vendor data as a dictionary.
        """
        # Fetch the latest vendor data to get the current SyncToken
        current_vendor_data = self.get_vendor_by_id(vendor_id)
        current_sync_token = current_vendor_data['Vendor']['SyncToken']
        update_data['SyncToken'] = current_sync_token

        url = f"{self.base_url}/v3/company/{realm_id}/vendor/"
        response = requests.post(url, headers=create_header(access_token), json=update_data)
        handle_error(response)
        return response.json()
