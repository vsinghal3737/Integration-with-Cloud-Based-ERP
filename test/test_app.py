import pytest
from flask import json
from src.main import app
from unittest.mock import patch


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


MOCKED_TOKEN = {'access_token': 'test_access_token', 'refresh_token': 'test_refresh_token', 'realm_id': 'test_realm_id'}


def test_authorize(client):
    with patch('auth.get_auth_url', return_value='http://mock-auth-url'):
        response = client.get('/authorize')

        # assert response.status_code == 200
        assert response.status_code == 302
        assert response.location == 'http://mock-auth-url'


def test_oauth_redirect(client):
    with patch('auth.get_tokens', return_value=MOCKED_TOKEN):
        response = client.get('/redirect?code=test_code&state=test_state&realmId=test_realm_id')
        data = json.loads(response.data)

        assert response.status_code == 200
        assert 'access_token' in data
        assert data['access_token'] == 'test_access_token'


def test_refresh_token(client):
    with patch.dict('src.main.tokens', MOCKED_TOKEN, clear=True):
        with patch('auth.refresh_token', return_value={'access_token': 'new_access_token', 'refresh_token': 'test_refresh_token', 'realm_id': 'test_realm_id'}, clear=True):
            response = client.get('/refresh_token')
            data = json.loads(response.data)
            assert response.status_code == 200
            assert 'access_token' in data
            assert data['access_token'] != 'test_access_token'
            assert data['access_token'] == 'new_access_token'


def test_revoke_token(client):
    with patch.dict('src.main.tokens', MOCKED_TOKEN, clear=True):
        with patch('auth.revoke_token', return_value={'status': 'success'}):
            response = client.get('/revoke_token')
            data = json.loads(response.data)
            assert response.status_code == 200
            assert 'status' in data
            assert data['status'] == 'success'


def test_get_accounts(client):
    with patch.dict('src.main.tokens', MOCKED_TOKEN, clear=True):
        with patch('bus_logic.accounts.AccountAPI.get_all_accounts', return_value={'accounts': []}):
            response = client.get('/accounts')
            data = json.loads(response.data)
            assert response.status_code == 200
            assert 'accounts' in data
            assert isinstance(data['accounts'], list)


def test_get_account_by_id(client):
    with patch.dict('src.main.tokens', MOCKED_TOKEN, clear=True):
        with patch('bus_logic.accounts.AccountAPI.get_account_by_id', return_value={'account': {}}):
            response = client.get('/accounts/test_account_id')
            data = json.loads(response.data)
            assert response.status_code == 200
            assert 'account' in data
            assert isinstance(data['account'], dict)


def test_update_account(client):
    with patch.dict('src.main.tokens', MOCKED_TOKEN, clear=True):
        with patch('bus_logic.accounts.AccountAPI.update_account', return_value={'account': {}}):
            response = client.post('/accounts/test_account_id', json={'update_fields': {}})
            data = json.loads(response.data)
            assert response.status_code == 200
            assert 'account' in data
            assert isinstance(data['account'], dict)


def test_get_vendors(client):
    with patch.dict('src.main.tokens', MOCKED_TOKEN, clear=True):
        with patch('bus_logic.vendors.VendorsAPI.get_all_vendors', return_value={'vendors': []}):
            response = client.get('/vendors')
            data = json.loads(response.data)
            assert response.status_code == 200
            assert 'vendors' in data
            assert isinstance(data['vendors'], list)


def test_get_vendor_by_id(client):
    with patch.dict('src.main.tokens', MOCKED_TOKEN, clear=True):
        with patch('bus_logic.vendors.VendorsAPI.get_vendor_by_id', return_value={'vendor': {}}):
            response = client.get('/vendors/test_vendor_id')
            data = json.loads(response.data)
            assert response.status_code == 200
            assert 'vendor' in data
            assert isinstance(data['vendor'], dict)


def test_update_vendor(client):
    with patch.dict('src.main.tokens', MOCKED_TOKEN, clear=True):
        with patch('bus_logic.vendors.VendorsAPI.update_vendor', return_value={'vendor': {}}):
            response = client.post('/vendors/test_vendor_id', json={'update_fields': {}})
            data = json.loads(response.data)
            assert response.status_code == 200
            assert 'vendor' in data
            assert isinstance(data['vendor'], dict)

