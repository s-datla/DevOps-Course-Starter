class ViewModel:
    def __init__(self, items):
        self._items = items

    @property
    def items(self):
        return self._items

    def sortItems(self, key, reverse = False):
        sortFunction = lambda x:x.status
        if key == 'title':
            sortFunction = lambda x: x.title
        self._items = sorted(self._items, key=sortFunction, reverse=reverse)

    @property
    def notStartedItems(self):
        return [item for item in self._items if item.status == 'Not Started']

    @property
    def beingDoneItems(self):
        return [item for item in self._items if item.status == 'Being Done']

    @property
    def completedItems(self):
        return [item for item in self._items if item.status == 'Completed']    