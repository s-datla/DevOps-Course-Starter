import os


class Config:
    """Base configuration variables."""
    TRELLO_KEY = os.environ.get('TRELLO_KEY')
    TRELLO_TOKEN = os.environ.get('TRELLO_TOKEN')
    BOARD_ID = os.environ.get('BOARD_ID')
    NOT_STARTED_LIST_ID = os.environ.get('NOT_STARTED_LIST_ID')
    BEING_DONE_LIST_ID = os.environ.get('BEING_DONE_LIST_ID')
    COMPLETED_LIST_ID = os.environ.get('COMPLETED_LIST_ID')
    if not TRELLO_KEY or not TRELLO_TOKEN:
        raise ValueError("Not all environment variables set for Flask application. Did you follow the setup instructions?")
