from flask import Flask
from requests import get, post, put
from todo_app.flask_config import Config
from todo_app.data.ToDoItem import ToDoItem 

app = Flask(__name__)
app.config.from_object(Config)

# Constants
_BASE_PARAMS = {'key': app.config['TRELLO_KEY'], 'token':app.config['TRELLO_TOKEN']}
_BOARD_BASE_URL = 'https://api.trello.com/1/boards/GjbQrcgh/cards'
_CARDS_BASE_URL = 'https://api.trello.com/1/cards'


# Creating this local storage as session data must be serialisable which messes up with class methods
class LocalItemList:
    def __init__(self):
        self.items = []

localItemList = LocalItemList()

def get_items(force_update=False):
    """
    Fetches all saved items from the session.

    Returns:
        list: The list of saved items.
    """
    if not localItemList.items or force_update:            
        all_items = get(_BOARD_BASE_URL, params=_BASE_PARAMS)
        localItemList.items = [ToDoItem(item) for item in all_items.json()]
    return localItemList.items

def get_item(id):
    """
    Fetches the saved item with the specified ID.

    Args:
        id: The ID of the item.

    Returns:
        item: The saved item, or None if no items match the specified ID.
    """
    items = get_items()
    return next((item for item in items if item.id == id), None)


def add_item(title):
    """
    Adds a new item with the specified title to the session.

    Args:
        title: The title of the item.

    Returns:
        boolean: A boolean denoting whether the function succeeded or not.
    """
    responseBody = post(_CARDS_BASE_URL, params={ **_BASE_PARAMS, 'idList':_BASE_LIST_ID + _NOT_STARTED_LIST_ID, 'name': title })
    if responseBody.status_code == 200:
        return get_items(True)
    return False


def save_item(item):
    """
    Updates an existing item in the session. If no existing item matches the ID of the specified item, nothing is saved.

    Args:
        boolean: A boolean denoting whether the function succeeded or not.
    """
    existing_items = get_items()
    for current_item in existing_items:
        if item.id == current_item.id:
            item.moveItem()
            responseBody = put(_CARDS_BASE_URL + '/' + item.id, params={ **_BASE_PARAMS, 'idList': item.listId})
            if responseBody.status_code == 200:
                return get_items(True)
    return False
