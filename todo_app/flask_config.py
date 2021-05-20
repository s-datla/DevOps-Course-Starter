import os


class Config:
    """Base configuration variables."""
    TRELLO_KEY = os.environ.get('TRELLO_KEY')
    if not TRELLO_KEY:
        raise ValueError("No TRELLO_KEY set for Flask application. Did you follow the setup instructions?")
