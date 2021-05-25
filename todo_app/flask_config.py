import os


class Config:
    """Base configuration variables."""
    TRELLO_KEY = os.environ.get('TRELLO_KEY')
    TRELLO_TOKEN = os.environ.get('TRELLO_TOKEN')
    if not TRELLO_KEY or not TRELLO_TOKEN:
        raise ValueError("No TRELLO_KEY or TRELLO_TOKEN set for Flask application. Did you follow the setup instructions?")
