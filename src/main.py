from flask import Flask, redirect, request, jsonify, abort
import logging

import config
import auth
from bus_logic.accounts import AccountAPI
from bus_logic.vendors import VendorsAPI

from intuitlib.enums import Scopes

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

account_api = AccountAPI(config.BASE_URL)
vendors_api = VendorsAPI(config.BASE_URL)
tokens = {}


@app.route('/authorize')
def authorize():
    try:
        auth_url = auth.get_auth_url([Scopes.ACCOUNTING])
        logging.debug(f"Authorization URL: {auth_url}")
        return redirect(auth_url)
    except Exception as e:
        logging.error(f"Error generating authorization URL: {e}")
        return str(e), 500


@app.route('/redirect')
def oauth_redirect():
    logging.info('oauth_redirect(): Init')
    global tokens
    try:
        auth_code = request.args.get('code')
        realm_id = request.args.get('realmId')
        state = request.args.get('state')
        logging.debug(f"Received auth_code: {auth_code}, realm_id: {realm_id}, state: {state}")

        if not auth_code:
            logging.error('oauth_redirect(): Fin with Exception')
            logging.error("Authorization code not found in callback URL.")
            return "Authorization code not found in callback URL.", 400

        tokens = auth.get_tokens(auth_code, realm_id)
        logging.info('oauth_redirect(): Fin with Success')
        return jsonify(tokens)
    except Exception as e:
        logging.error('oauth_redirect(): Fin with Exception')
        logging.error(f"Error exchanging authorization code for tokens: {e}")
        return str(e), 500


@app.route('/refresh_token')
def refresh_token_route():
    logging.info('refresh_token_route(): Init')
    global tokens
    try:
        tokens = auth.refresh_token(tokens['refresh_token'])
        logging.info('refresh_token_route(): Fin with Success')
        return jsonify(tokens)
    except Exception as e:
        logging.error('refresh_token_route(): Fin with Exception')
        logging.error(f"Error refreshing token: {e}")
        return str(e), 500


@app.route('/revoke_token')
def revoke_token_route():
    logging.info('revoke_token_route(): Init')
    global tokens
    try:
        _check_token()
        revoke_response = auth.revoke_token()
        logging.info('revoke_token_route(): Fin with Success')
        tokens = {}
        return jsonify(revoke_response)
    except Exception as e:
        logging.error('revoke_token_route(): Fin with Exception')
        logging.error(f"Error revoking token: {e}")
        return str(e), 500


# Account Endpoints
@app.route('/accounts', methods=['GET'])
def get_accounts():
    logging.info('get_accounts(): Init')
    try:
        _check_token()
        accounts_data = account_api.get_all_accounts(tokens['access_token'], tokens['realm_id'])
        logging.info('get_accounts(): Fin with Success')
        return jsonify(accounts_data)
    except Exception as e:
        logging.error('get_accounts(): Fin with Exception')
        logging.error(f"Error getting accounts: {e}")
        return str(e), 500


@app.route('/accounts/<account_id>', methods=['GET'])
def get_account_by_id(account_id):
    logging.info(f'get_account_by_id({account_id}): Init')
    try:
        _check_token()
        account_data = account_api.get_account_by_id(account_id, tokens['access_token'], tokens['realm_id'])
        logging.info(f'get_account_by_id({account_id}): Fin with Success')
        return jsonify(account_data)
    except Exception as e:
        logging.error(f'get_account_by_id({account_id}): Fin with Exception')
        logging.error(f"Error getting account by ID: {e}")
        return str(e), 500


@app.route('/accounts/<account_id>', methods=['POST'])
def update_account(account_id):
    logging.info(f'update_account({account_id}): Init')
    try:
        _check_token()
        update_fields = request.json.get('update_fields')
        updated_account = account_api.update_account(account_id, update_fields, tokens['access_token'], tokens['realm_id'])
        logging.info(f'update_account({account_id}): Fin with Success')
        return jsonify(updated_account)
    except Exception as e:
        logging.error(f'update_account({account_id}): Fin with Exception')
        logging.error(f"Error updating account: {e}")
        return str(e), 500


# Vendor Endpoints
@app.route('/vendors', methods=['GET'])
def get_vendors():
    logging.info('get_vendors(): Init')
    try:
        _check_token()
        vendors_data = vendors_api.get_all_vendors(tokens['access_token'], tokens['realm_id'])
        logging.info('get_vendors(): Fin with Success')
        return jsonify(vendors_data)
    except Exception as e:
        logging.error('get_vendors(): Fin with Exception')
        logging.error(f"Error getting vendors: {e}")
        return str(e), 500


@app.route('/vendors/<vendor_id>', methods=['GET'])
def get_vendor_by_id(vendor_id):
    logging.info(f'get_vendor_by_id({vendor_id}): Init')
    try:
        _check_token()
        vendor_data = vendors_api.get_vendor_by_id(vendor_id, tokens['access_token'], tokens['realm_id'])
        logging.info(f'get_vendor_by_id({vendor_id}): Fin with Success')
        return jsonify(vendor_data)
    except Exception as e:
        logging.error(f'get_vendor_by_id({vendor_id}): Fin with Exception')
        logging.error(f"Error getting vendor by ID: {e}")
        return str(e), 500


@app.route('/vendors/<vendor_id>', methods=['POST'])
def update_vendor(vendor_id):
    logging.info(f'update_vendor({vendor_id}): Init')
    try:
        _check_token()
        update_fields = request.json.get('update_fields')
        updated_vendor = vendors_api.update_vendor(vendor_id, update_fields, tokens['access_token'], tokens['realm_id'])
        logging.info(f'update_vendor({vendor_id}): Fin with Success')
        return jsonify(updated_vendor)
    except Exception as e:
        logging.error(f'update_vendor({vendor_id}): Fin with Exception')
        logging.error(f"Error updating vendor: {e}")
        return str(e), 500


def _check_token():
    global tokens
    if not tokens:
        logging.error("Tokens not available. Authorize first.")
        abort(401, description="Tokens not available. Authorize first.")


if __name__ == "__main__":
    print("Visit the following URL to authorize the application:")
    print(auth.get_auth_url([Scopes.ACCOUNTING]))
    app.run(port=5000)
