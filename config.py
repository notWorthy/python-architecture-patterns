import os

def get_api_url():
    host = os.environ.get('API_HOST', 'localhost')
    port = os.environ.get('API_PORT', 5000)
    return f'http://{host}:{port}'