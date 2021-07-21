import os
import dotenv 
import requests

class TrelloClient:
    def __init__(self):
        dotenv.load_dotenv()
        pass

    @staticmethod
    def getBaseBoardUrl():
        return 'https://api.trello.com/1/boards/'

    @staticmethod
    def getBoardCardUrl():
        return 'https://api.trello.com/1/boards/{}/cards'.format(os.getenv('BOARD_ID'))

    @staticmethod
    def getBoardListUrl():
        return 'https://api.trello.com/1/boards/{}/lists'.format(os.getenv('BOARD_ID'))

    @staticmethod
    def getCardsUrl():
        return 'https://api.trello.com/1/cards'

    @staticmethod
    def getBaseParams():
        return {'key': os.getenv('TRELLO_KEY'), 'token': os.getenv('TRELLO_TOKEN') }

    def getAllItems(self):
        response = requests.get(self.getBoardCardUrl(), params=self.getBaseParams())
        return response.json()
    
    def addNewItem(self,title):
        return requests.post(self.getCardsUrl(), params={ **self.getBaseParams(), 'idList': os.getenv('NOT_STARTED_LIST_ID'), 'name': title })
    
    def deleteItem(self,id):
        return requests.delete('{0}/{1}'.format(self.getCardsUrl(),id), params={ **self.getBaseParams() })
    
    def moveItem(self, id, listId):
        return requests.put('{0}/{1}'.format(self.getCardsUrl(),id), params={ **self.getBaseParams(), 'idList': listId })

    def createNewBoard(self, name):
        return requests.post(self.getBaseBoardUrl(), params={ **self.getBaseParams(), 'name': name } )
    
    def removeBoard(self, id):
        return requests.delete('{0}{1}'.format(self.getBaseBoardUrl(),id), params={ **self.getBaseParams() } )
    
    def updateConfig(self, id):
        lists = requests.get(self.getBoardListUrl(), params={ **self.getBaseParams() }).json()
        for list in lists:
            if list['name'] == 'To Do':
                os.environ['NOT_STARTED_LIST_ID'] = list['id']
            if list['name'] == 'Doing':
                os.environ['BEING_DONE_LIST_ID'] = list['id']
            if list['name'] == 'Done':
                os.environ['COMPLETED_LIST_ID'] = list['id']