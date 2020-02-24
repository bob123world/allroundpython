import os
import json

from notion.client import NotionClient
from notion.block import HeaderBlock, TextBlock, CollectionViewBlock

class Upload:
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

        if "backtest_results" not in config:
            print("backtest_results path is missing in config.json")
            exit()
        
        self.config = config

        self.client = NotionClient(token_v2=config["notion"]["token"])
        self.cv = self.client.get_collection_view(config["notion"]["page"])

        present_strategies = self.get_collection_strategies()
        present_results = self.get_backtest_results(config["backtest_results"])
        self.compare_and_add_new(present_strategies, present_results)

    def compare_and_add_new(self, present_strategies, results):
        for result in results:
            present = False
            for strategy in present_strategies:
                if result["strategy"] in strategy:
                    present = True
            if not present:
                row = self.cv.collection.add_row()
                row.avg_profit = 0
                row.buys = 0
                row.loses = 0
                row.strategy = result["strategy"]
                row.title = result["strategy"]
                row.title_plaintext = result["strategy"]
                row.total_profit = 0
                row.wins = 0

    def calculate_report(self, trades):
        report = {}
        report["buys"] = len(trades)

        trade_info = []
        for trade in trades:
            t_info = {}
            t_info["pair"] = trade[0]
            t_info["amount"] = trade[1]
            t_info["buy_date"] = trade[2]
            t_info["sell_date"] = trade[3]
            t_info["unknown1"] = trade[4]
            t_info["duration"] = trade[5]
            t_info["buy_price"] = trade[6]
            t_info["sell_price"] = trade[7]
            t_info["unknown2"] = trade[8]
            t_info["reason"] = trade[9]
            t_info["percentage"] = (t_info["sell_price"] / t_info["buy_price"]) - 1
            t_info["mc_difference"] = (t_info["amount"] * t_info["sell_price"]) - (t_info["amount"] * t_info["buy_price"])
            trade_info.append(t_info)

        report["pairs"] = []
        report["wins"] = 0
        report["loss"] = 0
        report["total_profit"] = 0
        report["cum_profit_%"] = 0
        report["duration"] = 0
        for trade in trade_info:
            if trade["pair"] in report["pairs"]:
                report["pairs"][trade["pair"]]["buys"] += 1
                report["pairs"][trade["pair"]]["total_profit"] += trade["mc_difference"]
                report["pairs"][trade["pair"]]["cum_profit_%"] += trade["percentage"]
                report["pairs"][trade["pair"]]["duration%"] += trade["duration"]
                if t_info["mc_difference"] >= 0:
                    report["pairs"][trade["pair"]]["wins"] += 1
                else:
                    report["pairs"][trade["pair"]]["loss"] += 1
            else:
                report["pairs"][trade["pair"]] = {}
                report["pairs"][trade["pair"]]["buys"] = 1
                report["pairs"][trade["pair"]]["total_profit"] = trade["mc_difference"]
                report["pairs"][trade["pair"]]["cum_profit_%"] = trade["percentage"]
                report["pairs"][trade["pair"]]["duration"] = trade["duration"]
                if t_info["mc_difference"] >= 0:
                    report["pairs"][trade["pair"]]["loss"] = 0
                    report["pairs"][trade["pair"]]["wins"] = 1
                else:
                    report["pairs"][trade["pair"]]["loss"] = 1
                    report["pairs"][trade["pair"]]["wins"] = 0

        for rep in report["pairs"]:
            report["wins"] += rep["wins"]
            report["loss"] += rep["loss"]
            report["total_profit"] += rep["total_profit"]
            report["cum_profit_%"] += rep["cum_profit_%"]
            report["duration"] += rep["duration"]

        report["avg_profit"] = report["total_profit"] / report["buys"]
        report["avg_profit_%"] = report["cum_profit_%"] / report["buys"]

        return report, trade_info


    def get_collection_strategies(self):
        strategies = []
        for row in self.cv.collection.get_rows():
            strategies.append(row.strategy)
        return strategies

    def get_backtest_results(self, path):
        results = []
        for root, dirs, files in os.walk(path):
            for file in files:
                information = {}
                filenamelist = file.split("-")
                strategy = filenamelist[2]
                strategy = strategy.replace(".json", "")
                information["strategy"] = strategy
                try:
                    with open(os.path.join(root, file)) as f:
                        information["trades"] = json.load(f)
                except Exception as e:
                    print(e)
                results.append(information)
        return results

if __name__ == "__main__":
    try:
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"config.json")) as json_file:
            config = json.load(json_file)
    except:
        print("config.json is not found!")
        exit()

    upload = Upload(config)