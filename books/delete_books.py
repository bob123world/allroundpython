import os
import json

from progress.bar import Bar

class DeleteBooks():
    def __init__(self, config):
        if "book_dir" not in config:
            print("book_dir key is not present in config.json!")
            exit()
        
        if not os.path.exists(config["book_dir"]):
            print("the path provided in book_dir key can not be found!")
            exit()

        self.book_dir = config["book_dir"]
        self.delete_unwanted_books()
    def delete_unwanted_books(self, books=None):
        files = 0
        folders = 0

        for dir_path, dir_names, file_names in os.walk(self.book_dir):
            files += len(file_names)
            folders += len(dir_names)
        
        print("Amount of files to process: " + str(files))
        print("Amount of folders to process: " + str(folders))

        bar = Bar('Processing books on disk: ', max=folders)

        for dir_path, dir_names, file_names in os.walk(self.book_dir):
            for file in file_names:
                if file.endswith(".epub") and "DESKTOP-U3QENOB" in file:
                    try:
                        os.remove(os.path.join(dir_path, file))
                    except Exception as e:
                        print(e)
                        pass
            bar.next()

        bar.finish()

        return books

if __name__ == "__main__":
    root = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(root,"config.json"), "r") as file:
        config = json.load(file)
    db = DeleteBooks(config)
