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
        self.domino()
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
        dpizza.notion(self.notion, "https://www.notion.so/d94a9acd41754a3ba43545b0e7bed199?v=e0409003d42c436fac08c84d4a373714", domino_data)

    def ubereats(self):
        """Check Uber Eats promotions"""
        ue = ubereats.UberEats(self.account)
        ue_data = ue.process()
        print(ue_data)
        ue.notion(self.notion, "https://www.notion.so/13e537d605984f3ead8c7e5cfaf21837?v=5148a103639d46aeaa6fa5e8c9c14793", ue_data)

if __name__ == "__main__":
    notion = NotionClient(token_v2="bea5393b895d0c89774e5f4386f03ab29d9a9fb3dfa26629aeca418915a173f26b6db581cdf27b623f258c5f70356fba2272d65d5b1fb717c9bd837511fb32226dfe0883c78d0672c7d93a0dd6be")
    out = Outlook("outlook.office365.com", "deboeure.s@hotmail.com", "deboeure.s@hotmail.com", "Neeters6175097out", notion)