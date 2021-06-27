from requests import get, post, put
from todo_app.data.ToDoItem import ToDoItem
from todo_app.data.TrelloClient import TrelloClient

apiClient = TrelloClient()

def get_items():
    """
    Fetches all saved items from the session.

    Returns:
        list: The list of saved items.
    """
    all_items = apiClient.getAllItems()
    return [ToDoItem(item) for item in all_items]

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
    response = apiClient.addNewItem(title)
    if response.status_code == 200:
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
            response = apiClient.moveItem(item.id, item.listId)
            if response.status_code == 200:
                return get_items()
    return False
