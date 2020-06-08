import os
import pandas
import json
from datetime import datetime

from ebooklib import epub
from progress.bar import Bar

class CSVCreate():
    def __init__(self, config):
        if "book_dir" not in config:
            print("book_dir key is not present in config.json!")
            exit()
        
        if not os.path.exists(config["book_dir"]):
            print("the path provided in book_dir key can not be found!")
            exit()

        if "output_csv" not in config:
            print("output_csv key is not present in config.json!")
            exit()

        self.book_dir = config["book_dir"]
        self.output_csv = config["output_csv"]

        books = None
        if os.path.exists(config["output_csv"]):
            books = pandas.read_csv(filepath_or_buffer=config["output_csv"], sep=";", header=0)
            books = self.list_books(books)
        else:
            books = self.list_books()

        self.create_csv(books)

    def create_csv(self, books_df):
        try:
            books_df = books_df.sort_values(by=["Location"])
            books_df.to_csv(path_or_buf=self.output_csv, sep=";", index=False)
            print("CSV file written to location: " + str(self.output_csv))
        except Exception as e:
            print(e)

    def list_books(self, books=None):
        files = 0
        folders = 0
        columns = ["Title", "Author", "ISBN","Language","Publish Date", "Addition Date", "Location"]
        if books is None:
            books = pandas.DataFrame(columns=columns)

        for dir_path, dir_names, file_names in os.walk(self.book_dir):
            files += len(file_names)
            folders += len(dir_names)
        
        print("Amount of files to process: " + str(files))
        print("Amount of folders to process: " + str(folders))

        bar = Bar('Processing books on disk: ', max=folders)

        for dir_path, dir_names, file_names in os.walk(self.book_dir):
            for file in file_names:
                if file.endswith(".epub"):
                    if str(os.path.join(dir_path,file)) not in books.Location.values:
                        try:
                            book = epub.read_epub(os.path.join(dir_path, file))
                        except Exception as e:
                            #print(e)
                            pass
                        book_dict = {}
                        try:
                            book_dict["Title"] = book.get_metadata('DC', 'title')[0][0]
                        except:
                            book_dict["Title"] = "unknown"
                        try:
                            book_dict["ISBN"] = book.get_metadata('DC', 'identifier')[0][0]
                        except:
                            book_dict["ISBN"] = "unknown"
                        try:
                            book_dict["Author"] = book.get_metadata('DC', 'creator')[0][0]
                        except:
                            book_dict["Author"] = "unknown"
                        try:
                            book_dict["Publish Date"] = book.get_metadata('DC', 'date')[0][0]
                        except:
                            book_dict["Publish Date"] = "unknown"
                        try:
                            book_dict["Language"] = book.get_metadata('DC', 'language')[0][0]
                        except:
                            book_dict["Language"] = "UND"
                        book_dict["Addition Date"] = datetime.now().strftime("%d/%m/%Y")
                        book_dict["Location"] = str(os.path.join(dir_path, file))
                        books = books.append(book_dict, ignore_index=True)
            bar.next()

        bar.finish()

        return books

if __name__ == "__main__":
    root = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(root,"config.json"), "r") as file:
        config = json.load(file)
    csvc = CSVCreate(config)
