from flask import template_rendered
from pytest import fixture
from contextlib import contextmanager
import dotenv
import json

from todo_app.app import create_app
from unittest.mock import patch, Mock
from todo_app.tests.integration_tests.mock_responses import *

@fixture
def client():
    # Use our test integration config instead of the 'real' version
    file_path = dotenv.find_dotenv('.env.test')
    dotenv.load_dotenv(file_path, override=True)
    # Create the new app.
    test_app = create_app()
    # Use the app to create a test_client that can be used in our tests.
    yield test_app

# Using flask template_rendered helper: https://flask.palletsprojects.com/en/1.1.x/signals/?highlight=template_rendered
@contextmanager
def captured_templates(client):
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))

    template_rendered.connect(record, client)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, client)


@patch('requests.get')
def test_index_page(mock_get_requests, client):
    # Replace call to requests.get(url) with our own function
    mock_get_requests.side_effect = mock_get_all_cards
    with captured_templates(client) as templates:
        response = client.test_client().get('/')
        assert response.status_code == 200
        assert len(templates) == 1
        template, context = templates[0]
        assert template.name == 'index.html'
        assert len(context['view_model'].items) == 3

@patch('requests.post')
@patch('requests.get')
def test_add_item_endpoint(mock_get_requests, mock_post_requests, client):
    mock_post_requests.side_effect = mock_post_new_card
    mock_get_requests.side_effect = mock_get_all_cards
    with captured_templates(client) as templates:
        headers = { 'Content-Type': 'application/x-www-form-urlencoded'}
        payload = {'title':'Mock Card', 'submit': 'Submit'}
        response = client.test_client().post('/', data=payload, headers=headers)
        assert response.status_code == 302
        assert len(templates) == 0

@patch('requests.delete')
@patch('requests.get')
def test_delete_item_endpoint(mock_get_requests, mock_delete_requests, client):
    mock_delete_requests.side_effect = mock_delete_existing_card
    mock_get_requests.side_effect = mock_get_all_cards
    with captured_templates(client) as templates:
        response = client.test_client().get('/delete/MockId1')
        assert response.status_code == 302
        assert len(templates) == 0

@patch('requests.put')
@patch('requests.get')
def test_move_item_endpoint(mock_get_requests, mock_put_requests, client):
    mock_get_requests.side_effect = mock_get_all_cards
    mock_put_requests.side_effect = mock_put_updated_card
    with captured_templates(client) as templates:
        response = client.test_client().get('/move/MockId1')
        assert response.status_code == 302
        assert len(templates) == 0


def mock_get_all_cards(url, params):
    if url == 'https://api.trello.com/1/boards/MockBoardId/cards':
        response = Mock()
        response.json.return_value = json.loads(mock_all_cards_response)
        response.status_code = 200
        return response
    return None

def mock_post_new_card(url, params):
    if url == 'https://api.trello.com/1/cards':
        response = Mock()
        response.json.return_value = json.loads(mock_new_card_response)
        response.status_code = 200
        return response
    return None

def mock_put_updated_card(url, params):
    if url == 'https://api.trello.com/1/cards/MockId1':
        response = Mock()
    # sample_trello_lists_response should point to some test response data
        response.json.return_value = json.loads(mock_updated_card_response)
        response.status_code = 200
        return response
    return None

def mock_delete_existing_card(url, params):
    if url == 'https://api.trello.com/1/cards/MockId1':
        response = Mock()
    # sample_trello_lists_response should point to some test response data
        response.json.return_value = json.loads(mock_deleted_card_response)
        response.status_code = 200
        return response
    return None