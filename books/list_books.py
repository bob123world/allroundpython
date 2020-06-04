import os
import json
import pickle
import time
from datetime import datetime

from ebooklib import epub
import gspread
from progress.bar import Bar

# import googleapiclient
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request

class BookLister():
    def __init__(self, config):
        if "book_dir" not in config:
            print("book_dir key is not present in config.json!")
            exit()
        
        if not os.path.exists(config["book_dir"]):
            print("the path provided in book_dir key can not be found!")
            exit()

        if "credentials" not in config:
            print("credentials key is not present in config.json!")
            exit()

        if not os.path.exists(config["credentials"]):
            print("the path provided in credentials key can not be found!")
            exit()

        if "spreadsheet_id" not in config:
            print("spreadsheet_id key is not present in config.json!")
            exit()

        self.book_dir = config["book_dir"]
        self.credentials = config["credentials"]
        self.spreadsheet_id = config["spreadsheet_id"]

        self.link_gsheet()

        books = self.list_books()
        self.add_books_to_gsheet(books)

    def link_gsheet(self):
        creds = None
        scopes = ['https://www.googleapis.com/auth/spreadsheets']
        self.service = gspread.service_account(filename=self.credentials, scopes=scopes)
        self.sheet = self.service.open_by_key(self.spreadsheet_id)

    def add_books_to_gsheet(self, books):
        worksheet = self.sheet.worksheet("Books")
        bar = Bar('Uploading books to google sheet: ', max=len(books))
        for i, book in enumerate(books):
            row = i + 2
            try:
                worksheet.update("A"+ str(row), book["title"])
                worksheet.update("B"+ str(row), book["author"])
                worksheet.update("C"+ str(row), book["isbn"])
                worksheet.update("D"+ str(row), book["language"])
                worksheet.update("E"+ str(row), book["pubdate"])
                worksheet.update("F"+ str(row), datetime.now().strftime("%d/%m/%Y"))
                worksheet.update("G"+ str(row), book["location"])
                bar.next()
            except Exception as e:
                #print(e)
                pass

            time.sleep(9)
        
        bar.finish()

    def list_books(self):
        files = 0
        folders = 0
        books = []
        for dir_path, dir_names, file_names in os.walk(self.book_dir):
            files += len(file_names)
            folders += len(dir_names)
        
        print("Amount of files to process: " + str(files))
        print("Amount of folders to process: " + str(folders))

        bar = Bar('Processing books on disk: ', max=folders)

        for dir_path, dir_names, file_names in os.walk(self.book_dir):
            for file in file_names:
                if file.endswith(".epub"):
                    try:
                        book = epub.read_epub(os.path.join(dir_path, file))
                    except Exception as e:
                        #print(e)
                        pass
                    book_dict = {}
                    try:
                        book_dict["title"] = book.get_metadata('DC', 'title')[0][0]
                    except:
                        book_dict["title"] = "unknown"
                    try:
                        book_dict["isbn"] = book.get_metadata('DC', 'identifier')[0][0]
                    except:
                        book_dict["isbn"] = "unknown"
                    try:
                        book_dict["author"] = book.get_metadata('DC', 'creator')[0][0]
                    except:
                        book_dict["author"] = "unknown"
                    try:
                        book_dict["pubdate"] = book.get_metadata('DC', 'date')[0][0]
                    except:
                        book_dict["pubdate"] = "unknown"
                    try:
                        book_dict["language"] = book.get_metadata('DC', 'language')[0][0]
                    except:
                        book_dict["language"] = "UND"
                    book_dict["location"] = str(os.path.join(dir_path, file))
                    books.append(book_dict)
            bar.next()

        bar.finish()

        return books
            
if __name__ == "__main__":
    try:
        root = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(root,"config.json"), "r") as file:
            config = json.load(file)
        bl = BookLister(config)
    except Exception as e:
        print(e)