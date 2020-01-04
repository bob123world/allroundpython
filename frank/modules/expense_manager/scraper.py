import json
import os
from bs4 import BeautifulSoup

config = {}
config["path"] = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Touch - Kredietkaart.html")

def main():
    f = open(config["path"], "r")
    text = f.read()
    soup = BeautifulSoup(text, "html.parser")
    money_list = soup.find_all(class_="orc-timeline__block orc-timeline__block--past orc-keyboard-accessible")
    expenses = []
    for money_info in money_list:
        expense = {}
        try:
            expense["date"] = money_info.find(class_="orc-timeline-item__prefix-date").contents[0]
            expense["vendor"] = money_info.find(class_="orc-timeline-item__summary-title").contents[0]
            expense["currency"] = money_info.find(class_="orc-number-display__suffix").contents[0]
            expense["cost"] = money_info.find(class_="orc-number-display__value").contents[0]
            expense["country"] = money_info.find(class_="orc-timeline-item__summary-subtitle").contents[0]
            expenses.append(expense)
        except Exception as e:
            print(e)

    print(expenses)
    money = 0
    for expense in expenses:
        money += float(expense["cost"].replace(",", "."))
    print(str(money))
if __name__ == '__main__':
    main()