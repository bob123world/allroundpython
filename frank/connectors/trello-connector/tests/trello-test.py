from __future__ import with_statement, print_function
from datetime import datetime, timedelta
import unittest
import os
import json
from trello.trelloclient import TrelloClient
# from py-trello import TrelloClient, ResourceUnavailable

class TrelloTestCase(unittest.TestCase):
    """
    Tests for TrelloClient API. Note these test are in order to
    preserve dependencies, as an API integration cannot be tested
    independently.
    """
    def setUp(self):
        try:
            ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

            with open(os.path.join(ROOT_DIR,"config.json"), "r") as file:
                config = json.load(file)
        except Exception as e:
            print(e)
            exit()

        self.board_name = "test-board"
        self.list_name = "test-list"

        self.trello = TrelloClient(config["trello"]["key"], token = config["trello"]["token"])
        for b in self.trello.list_boards():
            if b.name in self.board_name:
                self.board = b
                break
        if not self.board:
             self.board = self.trello.add_board(board_name=self.board_name)

    def _add_card(self, name, description=None):
        try:
            card = self._list.add_card(name, description)
            self.assertIsNotNone(card, msg="card is None")
            self.assertIsNotNone(card.id, msg="id not provided")
            self.assertEqual(card.name, name)
            return card
        except Exception as e:
            print(str(e))
            self.fail("Caught Exception adding card")
    

def suite():
    return unittest.TestLoader().loadTestsFromTestCase(TrelloTestCase)

if __name__ == "__main__":
    unittest.main()