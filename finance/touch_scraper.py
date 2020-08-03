import json
import os
from bs4 import BeautifulSoup

class TouchScraper():
    def __init__ (self):
        pass

    def scrape_tile_list(self, location):
        """Scrape a KBC Touch savings and investment page"""
        try:
            f = open(location, "r")
        except (OSError, IOError) as e:
            print("File was not found on the location given: " + location)
            return None
        
        text = f.read()
        soup = BeautifulSoup(text, "html.parser")
        investment_list = soup.find_all("div", attrs={"class": "orc-tile-block-container"})
        investments = []
        for inv in investment_list:
            investment = {}
            try:
                block_top = inv.find("div", attrs={"class": "touch-spabel-tile__block--top"})
                investment["title"] = block_top.find("div", attrs={"class": "touch-spabel-tile__title"}).text # Name
                block_middle = inv.find("div", attrs={"class": "touch-spabel-tile__block--middle"})                
                investment["value"] = block_middle.find("span", attrs={"class": "orc-number-display__value"}).text # Koers
                investment["suffix"] = block_middle.find("div", attrs={"class": "orc-number-display__suffix"}).text # currency
                investment["perc"] = block_middle.find("div", attrs={"class": "touch-spabel-tile__value--right"}).text # Percentage change since buy
                block_bottom = inv.find("div", attrs={"class": "touch-spabel-tile__block--bottom"})
                investment["amount"] = block_bottom.find("span", attrs={"class": "orc-number-display__value"}).text # Amount
                investment["amount_suffix"] = block_bottom.find("div", attrs={"class": "orc-number-display__suffix"}).text # Amount suffix
                investments.append([investment])
            except Exception as e:
                print(e)
        return investments

    def scrape_expense_list(self, location):
        """Scrape a KBC touch expense list page for a credit card or account overview"""
        try:
            f = open(location, "r")
        except (OSError, IOError) as e:
            print("File was not found on the location given: " + location)
            return None
        
        text = f.read()
        soup = BeautifulSoup(text, "html.parser")
        expense_list = soup.find_all(class_="orc-timeline__block orc-timeline__block--past orc-keyboard-accessible")
        expenses = []
        for exp in expense_list:
            expense = {}
            try:
                expense["date"] = exp.find(class_="orc-timeline-item__prefix-date").contents[0]
                expense["title"] = exp.find(class_="orc-timeline-item__summary-title").contents[0] # vendor
                expense["suffix"] = exp.find(class_="orc-number-display__suffix").contents[0] # currency
                expense["value"] = exp.find(class_="orc-number-display__value").contents[0] # expense
                expense["subtitle"] = exp.find(class_="orc-timeline-item__summary-subtitle").contents[0] # Country of payment
                expenses.append(expense)
            except Exception as e:
                print(e)
        return expenses

if __name__ == "__main__":
    tile_list = "C:/Users/micha/Desktop/Touch - Overzicht Sparen & Beleggen.html"
    expense_list = "C:/Users/micha/Desktop/Touch - Kredietkaart-2.html"

    ts = TouchScraper()
    result = ts.scrape_expense_list(expense_list)
    print(result)
    result = ts.scrape_tile_list(tile_list)
    print(result)