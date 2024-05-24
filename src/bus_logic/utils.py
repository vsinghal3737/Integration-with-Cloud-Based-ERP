def handle_error(response):
    if response.status_code not in [200, 201]:
        raise Exception(f"API request failed with status code {response.status_code}: {response.json()}")


def create_header(access_token):
    return {
        'Authorization': f'Bearer {access_token}',
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
