from todo_app.data.ViewModel import ViewModel
from pytest import fixture

class MockItem:
    def __init__(self, status):
        self._status = status
    
    @property
    def status(self):
        return self._status

@fixture
def todo_model():
    items = [ 
        MockItem('Not Started'),
        MockItem('Being Done'),
        MockItem('Being Done'),
        MockItem('Completed'),
    ]
    return ViewModel(items)
    
def test_get_items(todo_model):
    assert len(todo_model.items) == 4

def test_get_not_started_items(todo_model):
    assert len(todo_model.notStartedItems) == 1

def test_get_being_done_items(todo_model):
    assert len(todo_model.beingDoneItems) == 2

def test_get_completed_items(todo_model):
    assert len(todo_model.completedItems) == 1

