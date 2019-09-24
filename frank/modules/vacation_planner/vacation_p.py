import os
import json
from trello.trelloclient import TrelloClient

class VacationPlanner(object):
    def __init__(self, name, *args, **kwargs):
        self.name = name
    