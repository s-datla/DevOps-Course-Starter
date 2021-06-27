import os
import dotenv 
import requests

class TrelloClient:
    def __init__(self):
        dotenv.load_dotenv()
        pass

    @staticmethod
    def getBoardUrl():
        return 'https://api.trello.com/1/boards/{}/cards'.format(os.getenv('BOARD_ID'))

    @staticmethod
    def getCardsUrl():
        return 'https://api.trello.com/1/cards'

    @staticmethod
    def getBaseParams():
        return {'key': os.getenv('TRELLO_KEY'), 'token': os.getenv('TRELLO_TOKEN') }

    def getAllItems(self):
        response = requests.get(self.getBoardUrl(), params=self.getBaseParams())
        return response.json()
    
    def addNewItem(self,title):
        return requests.post(self.getCardsUrl(), params={ **self.getBaseParams(), 'idList': os.getenv('NOT_STARTED_LIST_ID'), 'name': title })
    
    def moveItem(self, id, listId):
        return requests.put('{0}/{1}'.format(self.getCardsUrl(),id), params={ **self.getBaseParams(), 'idList': listId})