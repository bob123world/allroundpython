import os
import json

from notion.client import NotionClient

def main(config):
    # Obtain the `token_v2` value by inspecting your browser cookies on a logged-in session on Notion.so
    client = NotionClient(token_v2=config["notion"]["token"])

    # Replace this URL with the URL of the page you want to edit
    page = client.get_block(config["notion"]["database"])

    print("The old title is:", page.title)

    # Access a database using the URL of the database page or the inline block
    cv = client.get_collection_view(config["notion"]["database"])

    for row in cv.collection.get_rows():
        print(row)

    # Add a new record
    row = cv.collection.add_row()
    row.name = "Just some data"
    row.is_confirmed = True
    row.estimated_value = 399
    row.files = ["https://www.birdlife.org/sites/default/files/styles/1600/public/slide.jpg"]
    row.person = client.current_user
    row.tags = ["A", "C"]
    row.where_to = "https://learningequality.org"


if __name__ == "__main__":
    try:
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"config.json")) as json_file:
            config = json.load(json_file)
    except:
        print("config.json is not found!")
        exit()

    main(config)