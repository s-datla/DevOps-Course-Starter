from todo_app.flask_config import Config

class ToDoItem:

    def __init__(self, item):
        self.id = item['id']
        self.listId = item['idList']
        self.title = item['name']
        displayClass, status = ToDoItem.transformStatus(item['idList'])
        self.displayClass = displayClass
        self.status = status

    @staticmethod
    def transformStatus(idList):
        """
        Transforms the idList attribute of the REST API payload into a readable status and displayClass.
        DisplayClass is used for determining the item class for html rendering.
        
        """
        status = 'Not Started'
        displayClass = ''
        if idList == Config.BEING_DONE_LIST_ID:
            status = 'Being Done'
            displayClass = 'table-warning'
        if idList == Config.COMPLETED_LIST_ID:
            status = 'Completed'
            displayClass = 'table-success'
        return displayClass, status

    def moveItem(self):
        """
        Logically moves the item across the todoBoard.
        Moves status from Not Started -> Being Done -> Completed

        Returns:
            idList: the id list for the next status.
        """
        listId = Config.BEING_DONE_LIST_ID
        if self.listId == Config.BEING_DONE_LIST_ID:
            listId = Config.COMPLETED_LIST_ID
        if self.listId == Config.COMPLETED_LIST_ID:
            listId = Config.NOT_STARTED_LIST_ID
        self.listId = listId
        displayClass, status = ToDoItem.transformStatus(listId)
        self.displayClass = displayClass
        self.status = status
    