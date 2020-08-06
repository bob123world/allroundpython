import os
import json

from exchangelib import Credentials, Account, Configuration, DELEGATE
from notion.client import NotionClient # Needs to be removed

from applications import domino, ubereats

class Outlook():
    def __init__(self, server, email, username, password, notion):
        """Initialize Outlook, set up connection wit O365"""
        self.account = self.connect(server, email, username, password)
        self.notion = notion
        #self.domino()
        self.ubereats()

    def connect(self, server, email, username, password):
        """Get Exchange account connection with server"""
        creds = Credentials(username=username, password=password)
        config = Configuration(server=server, credentials=creds)
        return Account(primary_smtp_address=email, autodiscover=False, config = config, access_type=DELEGATE)

    def domino(self):
        """Check Domino's Pizza promotions"""
        dpizza = domino.Domino(self.account)
        domino_data = dpizza.process()
        print(domino_data)
        dpizza.notion(self.notion, "", domino_data)

    def ubereats(self):
        """Check Uber Eats promotions"""
        ue = ubereats.UberEats(self.account)
        ue_data = ue.process()
        print(ue_data)
        ue.notion(self.notion, "", ue_data)

if __name__ == "__main__":
    notion = NotionClient(token_v2="")
    out = Outlook("outlook.office365.com", "", "", "", notion)