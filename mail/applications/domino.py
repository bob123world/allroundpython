import re
from datetime import datetime

class Domino():
    def __init__(self, account):
        self.account = account
        self.domino_folder = self.account.inbox / 'FRANK' / 'Domino\'s Pizza'

    def process(self):
        """process the domino's pizza folder in Outlook"""
        #print(self.domino_folder.total_count)
        data = []
        for item in self.domino_folder.all().order_by('-datetime_received')[:100]:
            domino = {}
            exp_date = self.get_expiration_date(item.body)
            if exp_date >= datetime.now():
                domino["promotion"] = item.subject
                domino["expiration_date"] = self.get_expiration_date(item.body)
                domino["link"] = self.get_promotions_url(item.body)
                data.append(domino)
            else:
                item.move_to_trash()
        return data

    def get_promotions_url(self, body):
        """get the url to the promotion"""
        url = None
        try:
            url = re.search("(?<=href=\").*(?=\">Klik hier voor de webversie)", body)[0]
        except Exception as e:
            print(e)
        return url

    def get_expiration_date(self, body):
        """Get the expiration date for the Domino's Pizza email"""
        date = None
        try:
            date_text = re.search("\d{2}-\d{2}-\d{4}", body)[0]
            date = datetime.strptime(date_text, "%d-%m-%Y")
        except Exception as e:
            print(e)
        return date

    def notion(self, notion, table_id, data):
        """Add data to Notion Table for Domino Pizza's"""
        cv = notion.get_collection_view(table_id)
        for row in cv.collection.get_rows():
            row.remove()
        for prom in data:
            row = cv.collection.add_row()
            row.promotion = prom["promotion"]
            row.expiration_date = prom["expiration_date"]
            row.link = prom["link"]