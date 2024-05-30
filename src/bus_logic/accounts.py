import requests

from bus_logic.utils import create_header, handle_error


class AccountAPI:
    """
    A class to interact with the Account API of the financial service.
    """

    def __init__(self, base_url):
        self.base_url = base_url

    def get_all_accounts(self, access_token, realm_id):
        """
        Retrieves all accounts.

        :param access_token: The access token for authentication.
        :param realm_id: The realm ID of the company.
        :return: A list of accounts.
        """
        url = f"{self.base_url}/v3/company/{realm_id}/query"
        query = "SELECT * FROM Account"
        response = requests.get(url, headers=create_header(access_token), params={'query': query})
        handle_error(response)
        return response.json().get('QueryResponse', {}).get('Account', [])

    def get_account_by_id(self, account_id, access_token, realm_id):
        """
        Retrieves an account by its ID.

        :param account_id: The ID of the account.
        :param access_token: The access token for authentication.
        :param realm_id: The realm ID of the company.
        :return: The account data as a dictionary.
        """
        url = f"{self.base_url}/v3/company/{realm_id}/account/{account_id}"
        response = requests.get(url, headers=create_header(access_token))
        handle_error(response)
        return response.json()

    def update_account(self, account_id, update_data, access_token, realm_id):
        """
        Updates an account with new data.

        :param account_id: The ID of the account to update.
        :param update_data: The data to update the account with.
        :param access_token: The access token for authentication.
        :param realm_id: The realm ID of the company.
        :return: The updated account data as a dictionary.
        """
        # Fetch the latest account data to get the current SyncToken
        current_account_data = self.get_account_by_id(account_id)
        current_sync_token = current_account_data['Account']['SyncToken']
        update_data['SyncToken'] = current_sync_token

        url = f"{self.base_url}/v3/company/{realm_id}/account/"
        response = requests.post(url, headers=create_header(access_token), json=update_data)
        handle_error(response)
        return response.json()
