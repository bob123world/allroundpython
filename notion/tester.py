import os
import json
from datetime import datetime, tzinfo

from notion.client import NotionClient
from notion.block import HeaderBlock, TextBlock, CollectionViewBlock


class Tester:
    def __init__(self, config):
        if "notion" in config:
            if "token" not in config["notion"]:
                print("token for notion is not present!")
                exit()
            if "page" not in config["notion"]:
                print("page for notion is not present!")
                exit()
        else:
             print("notion is missing in config.json")
             exit()
        
        self.config = config

        self.client = NotionClient(token_v2=config["notion"]["token"])
        self.page = self.client.get_block(config["notion"]["page"])

        for child in self.page.children:
            try:
                print(child.title)
            except Exception as e:
                print(e)

        print("Parent of {} is {}".format(self.page.id, self.page.parent.id))


if __name__ == "__main__":
    try:
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"config.json")) as json_file:
            config = json.load(json_file)
    except:
        print("config.json is not found!")
        exit()

    tester = Tester(config)