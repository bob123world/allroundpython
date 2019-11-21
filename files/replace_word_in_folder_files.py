import os
import csv
import json

config = {}
config["directory"] = '//anu-app-03/edi/SO/Error'
config["word_to_be_replaced"] = 'No lookup found ATI_WE11051656'
config["new_word"] = '08004403'

for root, dirs, files in os.walk(os.path.join(config["directory"])):
    for file in files:
        f = open(os.path.join(root, file), "r")
        data = f.read()

        data = data.replace(config["word_to_be_replaced"], config["new_word"])

        f = open(os.path.join(root,file), "w")
        f.write(data)
        f.close