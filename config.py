import os

def get_api_url():
    host = os.environ.get('API_HOST', 'localhost')
    if host == 'localhost':
        return f"http://{host}:5005"
    else:
        return host