import os, time
from threading import Thread
from pytest import fixture
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from todo_app.data.TrelloClient import TrelloClient
from todo_app.app import create_app

@fixture(scope='module')
def app_with_temp_board():
    apiClient = TrelloClient()
    # Create the new board & update the board id environment variable
    response = apiClient.createNewBoard('End_To_End_Test')
    board_id = response.json()['id']
    os.environ['BOARD_ID'] = board_id
    apiClient.updateConfig(board_id)
    # construct the new application
    application = create_app()
    # start the app in its own thread.
    thread = Thread(target=lambda:application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield application
    # Tear Down
    thread.join(1)
    apiClient.removeBoard(board_id)


@fixture(scope="module")
def driver():
    chrome_options = Options()
    chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
    chrome_options.binary_location=r'/usr/bin/google-chrome-stable'
    chrome_options.add_argument('--no-sandbox')
    with webdriver.Chrome(options=chrome_options) as driver:
        yield driver

def test_task_journey(driver, app_with_temp_board):
    driver.get('http://127.0.0.1:5000')
    assert driver.title == 'To-Do App'

def test_create_new_item(driver, app_with_temp_board):
    item_title = driver.find_element_by_name('title')
    item_title.send_keys('Test_Item')
    driver.find_element_by_id('submit-button').click()
    new_test_item = driver.find_elements_by_name('not-started-item')[0]
    assert not new_test_item == None

def test_move_item(driver, app_with_temp_board):
    item_title = driver.find_element_by_name('title')
    item_title.send_keys('Test_Item_Move')
    driver.find_element_by_id('submit-button').click()
    all_items = driver.find_elements_by_name('not-started-item')
    testable_item = [item for item in all_items if item.find_element_by_tag_name('th').text == 'Test_Item_Move'][0]
    testable_item.find_element_by_tag_name('input').click()
    new_test_item = driver.find_element_by_name('being-done-item')
    assert not new_test_item == None

def test_delete_item(driver, app_with_temp_board):
    item_title = driver.find_element_by_name('title')
    item_title.send_keys('Test_Item_Delete')
    driver.find_element_by_id('submit-button').click()
    all_items = driver.find_elements_by_name('not-started-item')
    testable_item = [item for item in all_items if item.find_element_by_tag_name('th').text == 'Test_Item_Delete'][0]
    testable_item.find_elements_by_tag_name('input')[1].click()
    all_items = driver.find_elements_by_name('not-started-item')
    testable_item = [item for item in all_items if item.find_element_by_tag_name('th').text == 'Test_Item_Delete']
    assert len(testable_item) == 0
