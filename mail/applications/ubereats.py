import re
from datetime import datetime

class UberEats():
    def __init__(self, account):
        self.account = account
        self.ubereats_folder = self.account.inbox / 'FRANK' / 'Uber Eats'

    def process(self):
        """process the Uber Eats folder in Outlook"""
        data = []
        for item in self.ubereats_folder.all().order_by('-datetime_received')[:100]:
            ubereats = {}
            exp_date = self.get_expiration_date(item.body)
            if exp_date is not None:
                if exp_date >= datetime.now():
                    ubereats["promotion"] = item.subject
                    ubereats["expiration_date"] = self.get_expiration_date(item.body)
                    ubereats["code"] = self.get_promotions_code(item.body)
                    data.append(ubereats)
                else:
                    item.move_to_trash()
            else:
                item.move_to_trash()
        return data

    def get_promotions_code(self, body):
        """get the code for the promotion"""
        code = None
        try:
            #code = re.search("(?<=<h4 style=\"margin:0; color:#5FB709; font-family:'UberMove-Medium','HelveticaNeue',Helvetica,Arial,sans-serif; font-size:28px; font-weight:normal; line-height:34px; padding:0; padding-bottom:7px; padding-top:7px\">).*(?= <\/h4>)", body)[0]
            code = re.search("(?<=Promo code: ).*(?= <\/h4>)", body)[0]
        except Exception as e:
            print(e)
        if code is None:
            code = "Unknown"
        return code

    def get_expiration_date(self, body):
        """Get the expiration date for the Uber Eats email"""
        date = None
        try:
            date_text = re.search("\d{2}/\d{2}/\d{4}", body)[0]
            date = datetime.strptime(date_text, "%d/%m/%Y")
        except Exception as e:
            print(e)
        return date

    def notion(self, notion, table_id, data):
        """Add data to Notion Table for Uber Eats"""
        cv = notion.get_collection_view(table_id)
        for row in cv.collection.get_rows():
            row.remove()
        for prom in data:
            row = cv.collection.add_row()
            row.promotion = prom["promotion"]
            row.code = prom["code"]
            row.expiration_date = prom["expiration_date"]
            