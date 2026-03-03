import os
from dotenv import load_dotenv
from youtube_uploader import get_youtube_service

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
load_dotenv(os.path.join(BASE_DIR, '.env'))

client_file = os.path.join(BASE_DIR, os.environ.get('YOUTUBE_CLIENT_SECRETS_FILE', 'client_secret.json'))
token_file = os.path.join(BASE_DIR, os.environ.get('YOUTUBE_TOKEN_FILE', 'youtube_token.json'))

if not os.path.exists(client_file):
    raise FileNotFoundError(f"Missing client secrets file: {client_file}")

get_youtube_service(client_file, token_file)
print(f"YouTube OAuth complete. Token saved at: {token_file}")
