import os
import pandas
import json
from datetime import datetime

from ebooklib import epub
from progress.bar import Bar

class InsertBooks():
    def __init__(self, config):
        if "book_dir" not in config:
            print("book_dir key is not present in config.json!")
            exit()
        
        if not os.path.exists(config["book_dir"]):
            print("the path provided in book_dir key can not be found!")
            exit()

        if "input_dir" not in config:
            print("input_dir key is not present in config.json!")
            exit()

        if not os.path.exists(config["input_dir"]):
            print("the path provided in input_dir key can not be found!")
            exit()

        disk_dir_books = self.list_folders(config["book_dir"])
        input_dir_books = self.list_folders(config["input_dir"])

    def list_folders(self, directory):
        files = 0
        folders = 0
        folder_names = []
        for dir_path, dir_names, file_names in os.walk(directory):
            files += len(file_names)
            folders += len(dir_names)

        print("Amount of files to process: " + str(files))
        print("Amount of folders to process: " + str(folders))

        bar = Bar('Listing directories on disk: ', max=folders)
        for dir_path, dir_names, file_names in os.walk(self.book_dir):
            for folder in dir_names:
                folder_names.append(folder)
                bar.next()
        bar.finish()

        return folder_names

if __name__ == "__main__":
    root = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(root,"config.json"), "r") as file:
        config = json.load(file)
    ib = InsertBooks(config)