import json
import os
from bs4 import BeautifulSoup

config = {}
config["path"] = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Touch - Kredietkaart.html")

def main():
    f = open(config["path"], "r")
    text = f.read()
    soup = BeautifulSoup(text, "html.parser")
    money_list = soup.fin_all(class_="orc-timeline__block orc-timeline__block--past orc-keyboard-accessible")
    expenses = []
    for money_info in money_list:
        expense = {}
        expense["date"] = money_info.find(class_="orc-timeline-item__prefix-date")
        expense["vendor"] = money_info.find(class_="orc-timeline-item__summary-title")
        expense["currency"] = money_info.find(class_="orc-number-display__suffix")
        expense["cost"] = money_info.find(class_="orc-timeline-item__info-col--amount")
        expense["country"] = money_info.find(class_="orc-timeline-item__summary-subtitle")
        expenses.append(expense)

    print(expenses)
if __name__ == '__main__':
    main()