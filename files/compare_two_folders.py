import os
from filecmp import dircmp

config = {}
config["checker"] = 'D:/Muziek/Albums'
config["to_be_checked"] = 'J:'

count = 0

for dir_path, dir_names, file_names in os.walk(config["checker"]):
    for dir_name in dir_names:
        dircmp(os.path.join(dir_path,dir_name), os.path.join(config["to_be_checked"],dir_name)).report()