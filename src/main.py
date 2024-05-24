from flask import Flask, redirect, request, jsonify

from src import config
from src import auth
from intuitlib.enums import Scopes

@app.route('/authorize')
def authorize():
    auth_url = auth.get_auth_url([Scopes.ACCOUNTING])
    return redirect(auth_url)


@app.route('/redirect')
def oauth_redirect():
    auth_code = request.args.get('code')
    realm_id = request.args.get('realmId')
    state = request.args.get('state')

    if not auth_code:
        return "Authorization code not found in callback URL.", 400

    # Exchange the authorization code for tokens
    tokens = auth.get_tokens(auth_code, realm_id)
    return jsonify(tokens)


# Token Management Endpoints
@app.route('/refresh_token', methods=['POST'])
def refresh_token_route():
    refresh_token_value = request.json.get('refresh_token')

    tokens = auth.refresh_token(refresh_token_value)
    return jsonify(tokens)


@app.route('/revoke_token', methods=['POST'])
def revoke_token_route():
    token = request.json.get('token')

    revoke_response = auth.revoke_token(token)
    return jsonify(revoke_response)


