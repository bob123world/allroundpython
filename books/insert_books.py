import os
import pandas
import json
from datetime import datetime
from distutils.dir_util import copy_tree
import shutil

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

        new_dirs, existing_dirs = self.compare_folders(disk_dir_books, input_dir_books)
        self.copy_new_folders(config["input_dir"], new_dirs, config["book_dir"])
        self.compare_contents_folders(config["input_dir"], existing_dirs, config["book_dir"])

    def copy_new_folders(self, copy_location, copy_list, dest_location):
        bar = Bar('Copying folders to root directory: ', max=len(copy_list))
        for folder in copy_list:
            try:
                copy_tree(os.path.join(copy_location, folder), os.path.join(dest_location, folder))
            except Exception as e:
                # print(e)
                pass
            bar.next()
        bar.finish()

    def compare_contents_folders(self, input_location, compare_folders, base_location):
        bar = Bar('Comparing folders in root directory: ', max=len(compare_folders))
        for folder in compare_folders:
            in_folder = []
            try:
                for file in os.listdir(os.path.join(input_location, folder)):
                    in_folder.append(file)
            except Exception as e:
                # print(e)
                pass
            base_folder = []
            try:
                for file in os.listdir(os.path.join(base_location, folder)):
                    base_folder.append(file)
            except Exception as e:
                # print(e)
                pass

            set_base_folder = set(base_folder)
            for file in in_folder:
                if file not in set_base_folder:
                    try:
                        shutil.copyfile(os.path.join(input_location, folder, file), os.path.join(base_location, folder, file))
                    except Exception as e:
                        # print(e)
                        pass
            bar.next()
        bar.finish()


    def compare_folders(self, base, in_folders):
        """Check the folder names of the new in_folders with the existing base folder list. Returns two lists containting the new_folders and the existing_folders"""
        new_folders = []
        existing_folders = []
        set_base = set(base)

        bar = Bar('Comparing new directories with already exisiting ones: ', max=len(in_folders))
        for folder in in_folders:
            if folder in set_base:
                existing_folders.append(folder)
            else:
                new_folders.append(folder)
            bar.next()
        
        bar.finish()
        return new_folders, existing_folders

    def list_folders(self, directory):
        """Lists the folder names in folder_names for a root directory give by directory"""
        files = 0
        folders = 0
        folder_names = []
        for dir_path, dir_names, file_names in os.walk(directory):
            files += len(file_names)
            folders += len(dir_names)

        print("Amount of files to process: " + str(files))
        print("Amount of folders to process: " + str(folders))

        bar = Bar('Listing directories on disk: ', max=folders)
        for dir_path, dir_names, file_names in os.walk(directory):
            for folder in dir_names:
                if "Updates" not in folder:
                    folder_names.append(folder)
                bar.next()
        bar.finish()

        return folder_names

if __name__ == "__main__":
    root = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(root,"config.json"), "r") as file:
        config = json.load(file)
    ib = InsertBooks(config)