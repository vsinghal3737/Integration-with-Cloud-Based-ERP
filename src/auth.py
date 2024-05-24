from intuitlib.client import AuthClient
from intuitlib.enums import Scopes
import config

# Create an instance of the AuthClient
auth_client = AuthClient(
    client_id=config.CLIENT_ID,
    client_secret=config.CLIENT_SECRET,
    environment=config.ENV_SAND,
    redirect_uri=config.REDIRECT_URI
)


# Function to get the authorization URL
def get_auth_url(scope):
    return auth_client.get_authorization_url(scope)


# Function to exchange authorization code for tokens
def get_tokens(auth_code, realm_id):
    auth_client.get_bearer_token(auth_code, realm_id)
    return {
        'access_token': auth_client.access_token,
        'refresh_token': auth_client.refresh_token,
        'realm_id': auth_client.realm_id
    }


def refresh_token(refresh_token_value):
    auth_client.refresh(refresh_token_value)
    return {
        'access_token': auth_client.access_token,
        'refresh_token': auth_client.refresh_token,
        'realm_id': auth_client.realm_id
    }


def revoke_token(token):
    response = auth_client.revoke(token)
    return response
