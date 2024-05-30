import pytest
from flask import json
from src.main import app, tokens
from unittest.mock import patch

# Constants
MOCKED_TOKEN = {'access_token': 'test_access_token', 'refresh_token': 'test_refresh_token', 'realm_id': 'test_realm_id'}

# Endpoint URLs
AUTHORIZE_URL = '/authorize'
REDIRECT_URL = '/redirect?code=test_code&state=test_state&realmId=test_realm_id'
REFRESH_TOKEN_URL = '/refresh_token'
REVOKE_TOKEN_URL = '/revoke_token'
GET_ACCOUNTS_URL = '/accounts'
GET_ACCOUNT_BY_ID_URL = '/accounts/test_account_id'
UPDATE_ACCOUNT_URL = '/accounts/test_account_id'
GET_VENDORS_URL = '/vendors'
GET_VENDOR_BY_ID_URL = '/vendors/test_vendor_id'
UPDATE_VENDOR_URL = '/vendors/test_vendor_id'


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


@pytest.fixture
def mock_tokens():
    with patch.dict('src.main.tokens', MOCKED_TOKEN, clear=True):
        yield


def test_authorize(client):
    with patch('auth.get_auth_url', return_value='http://mock-auth-url'):
        response = client.get(AUTHORIZE_URL)
        assert response.status_code == 302
        assert response.location == 'http://mock-auth-url'


def test_oauth_redirect(client):
    with patch('auth.get_tokens', return_value=MOCKED_TOKEN):
        response = client.get(REDIRECT_URL)
        data = json.loads(response.data)
        assert response.status_code == 200
        assert 'access_token' in data
        assert data['access_token'] == MOCKED_TOKEN['access_token']


def test_refresh_token(client, mock_tokens):
    with patch('auth.refresh_token',
               return_value={'access_token': 'new_access_token',
                             'refresh_token': 'test_refresh_token',
                             'realm_id': 'test_realm_id'}):
        response = client.get(REFRESH_TOKEN_URL)
        data = json.loads(response.data)
        assert response.status_code == 200
        assert 'access_token' in data
        assert data['access_token'] == 'new_access_token'


def test_revoke_token(client, mock_tokens):
    with patch('auth.revoke_token', return_value={'status': 'success'}):
        response = client.get(REVOKE_TOKEN_URL)
        data = json.loads(response.data)
        assert response.status_code == 200
        assert 'status' in data
        assert data['status'] == 'success'
        assert tokens == {}


def test_get_accounts(client, mock_tokens):
    with patch('bus_logic.accounts.AccountAPI.get_all_accounts', return_value={'accounts': []}):
        response = client.get(GET_ACCOUNTS_URL)
        data = json.loads(response.data)
        assert response.status_code == 200
        assert 'accounts' in data
        assert isinstance(data['accounts'], list)


def test_get_account_by_id(client, mock_tokens):
    with patch('bus_logic.accounts.AccountAPI.get_account_by_id', return_value={'account': {}}):
        response = client.get(GET_ACCOUNT_BY_ID_URL)
        data = json.loads(response.data)
        assert response.status_code == 200
        assert 'account' in data
        assert isinstance(data['account'], dict)


def test_update_account(client, mock_tokens):
    with patch('bus_logic.accounts.AccountAPI.update_account', return_value={'account': {}}):
        response = client.post(UPDATE_ACCOUNT_URL, json={'update_fields': {}})
        data = json.loads(response.data)
        assert response.status_code == 200
        assert 'account' in data
        assert isinstance(data['account'], dict)


def test_get_vendors(client, mock_tokens):
    with patch('bus_logic.vendors.VendorsAPI.get_all_vendors', return_value={'vendors': []}):
        response = client.get(GET_VENDORS_URL)
        data = json.loads(response.data)
        assert response.status_code == 200
        assert 'vendors' in data
        assert isinstance(data['vendors'], list)


def test_get_vendor_by_id(client, mock_tokens):
    with patch('bus_logic.vendors.VendorsAPI.get_vendor_by_id', return_value={'vendor': {}}):
        response = client.get(GET_VENDOR_BY_ID_URL)
        data = json.loads(response.data)
        assert response.status_code == 200
        assert 'vendor' in data
        assert isinstance(data['vendor'], dict)


def test_update_vendor(client, mock_tokens):
    with patch('bus_logic.vendors.VendorsAPI.update_vendor', return_value={'vendor': {}}):
        response = client.post(UPDATE_VENDOR_URL, json={'update_fields': {}})
        data = json.loads(response.data)
        assert response.status_code == 200
        assert 'vendor' in data
        assert isinstance(data['vendor'], dict)
