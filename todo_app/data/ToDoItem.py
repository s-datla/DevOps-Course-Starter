_BASE_LIST_ID = '60a6c184fd2064526bdf740'
_NOT_STARTED_LIST_ID = 'b'
_BEING_DONE_LIST_ID = 'c'
_COMPLETED_LIST_ID = 'd'

class ToDoItem:

    def __init__(self, item):
        self.id = item['id']
        self.listId = item['idList']
        self.title = item['name']
        self.transformStatus(item['idList'])

    def transformStatus(self, idList=None):
        """
        Transforms the idList attribute of the REST API payload into a readable status and displayClass.
        DisplayClass is used for determining the item class for html rendering.
        
        """
        if not idList:
            idList = self.listId 
        idListEnding = idList[-1:] 
        status = 'Not Started'
        displayClass = ''
        if idListEnding == _BEING_DONE_LIST_ID:
            status = 'Being Done'
            displayClass = 'table-warning'
        if idListEnding == _COMPLETED_LIST_ID:
            status = 'Completed'
            displayClass = 'table-success'
        self.displayClass = displayClass
        self.status = status

    def moveItem(self):
        """
        Logically moves the item across the todoBoard.
        Moves status from Not Started -> Being Done -> Completed

        Returns:
            idList: the id list for the next status.
        """
        ending = _BEING_DONE_LIST_ID
        if self.listId[-1:] == _BEING_DONE_LIST_ID:
            ending = _COMPLETED_LIST_ID
        if self.listId[-1:] == _COMPLETED_LIST_ID:
            ending = _NOT_STARTED_LIST_ID
        self.listId = _BASE_LIST_ID + ending
        self.transformStatus()
    