mock_all_cards_response = """[
  {
    "id": "MockId1",
    "idList": "MockNotStartedId",
    "name": "First Mock Card"
  },
  {
    "id": "MockId2",
    "idList": "MockBeingDoneId",
    "name": "Second Mock Card"
  },
  {
    "id": "MockId3",
    "idList": "MockCompletedId",
    "name": "Third Mock Card"
  }
]"""

mock_new_card_response = """
  {
    "id": "MockId4",
    "idList": "MockNotStartedId",
    "name": "Fourth Mock Card"
  }
"""

mock_updated_card_response = """
  {
    "id": "MockId1",
    "idList": "MockBeingDoneId",
    "name": "Fourth Mock Card"
  }
"""