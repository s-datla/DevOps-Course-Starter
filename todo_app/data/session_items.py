from requests import get, post, put
from todo_app.flask_config import Config
from todo_app.data.ToDoItem import ToDoItem 

# Constants
_BASE_PARAMS = {'key': Config.TRELLO_KEY, 'token': Config.TRELLO_TOKEN }
_BOARD_BASE_URL = 'https://api.trello.com/1/boards/{}/cards'.format(Config.BOARD_ID)
_CARDS_BASE_URL = 'https://api.trello.com/1/cards'


def get_items():
    """
    Fetches all saved items from the session.

    Returns:
        list: The list of saved items.
    """
    all_items = get(_BOARD_BASE_URL, params=_BASE_PARAMS)        
    return [ToDoItem(item) for item in all_items.json()]

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
    responseBody = post(_CARDS_BASE_URL, params={ **_BASE_PARAMS, 'idList': Config.NOT_STARTED_LIST_ID, 'name': title })
    if responseBody.status_code == 200:
        return get_items()
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
                return get_items()
    return False
