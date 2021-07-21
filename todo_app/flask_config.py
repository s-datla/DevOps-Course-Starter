import os
import dotenv

class Config:
    dotenv.load_dotenv()
    """Base configuration variables."""
    TRELLO_KEY = os.environ.get('TRELLO_KEY')
    TRELLO_TOKEN = os.environ.get('TRELLO_TOKEN')
    if not TRELLO_KEY or not TRELLO_TOKEN:
        raise ValueError("TRELLO_KEY and TRELLO_TOKEN are not set for Flask application. Did you follow the setup instructions?")
