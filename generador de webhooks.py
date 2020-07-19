import requests
from dotenv import load_dotenv
from pathlib import Path  # python3 only
import os

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# Token del bot y link de la página de heroku que tiene el código
TOKEN = os.environ['TOKEN']

destination = os.environ['destination']
print(requests.post('https://api.telegram.org/bot{}/setWebhook'.format(TOKEN), data={'url':destination}))

