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
            report, trades = self.calculate_report(result["trades"])
            present = False
            for strategy in present_strategies:
                if result["strategy"] in strategy:
                    present = True
            if not present:
                row = self.cv.collection.add_row()
                row.avg_profit_perc = round(report["avg_profit_%"],7)
                row.buys = report["buys"]
                row.loses = report["loss"]
                row.strategy = result["strategy"]
                row.title = result["strategy"]
                row.title_plaintext = result["strategy"]
                row.cum_profit_perc = round(report["cum_profit_%"],6)
                row.total_profit_mc = round(report["total_profit"],6)
                row.wins = report["wins"]
                row.rating = ["To Do"]
                self.create_detail_page(result["strategy"], row.id, report["pairs"])

    def create_detail_page(self, strategy, id, pairs_info):
        eid = id.replace("-","")
        page = self.client.get_block("https://www.notion.so/" + strategy + "-" + eid)

        header1 = page.children.add_new(HeaderBlock)
        header1.title = "Strategy Information"
        header2 = page.children.add_new(HeaderBlock)
        header2.title = "Review"

        cv = self.client.get_collection_view(self.config["notion"]["sample"])
        collection = self.client.get_collection(cv.collection.id) # get an existing collection
        cvb = page.children.add_new(CollectionViewBlock, collection=collection)
        view = cvb.views.add_new(view_type="table")

        for pair in pairs_info:
            try:
                row = cvb.collection.add_row()
                row.pair = pair["pair"]
                row.buys = pair["buys"]
                row.wins = pair["wins"]
                row.loss = pair["loss"]
                row.avg_profit_perc = pair["avg_profit_%"]
                row.cum_profit_perc = pair["cum_profit_%"]
                row.tot_profit_mc = pair["profit"]
                row.avg_duration = pair["avg_duration"]
            except Exception as e:
                print(e)

    def calculate_report(self, trades):
        report = {}
        report["buys"] = len(trades)

        trade_info = []
        for trade in trades:
            t_info = {}
            t_info["pair"] = trade[0]
            t_info["percentage"] = trade[1]
            t_info["buy_date"] = trade[2]
            t_info["sell_date"] = trade[3]
            t_info["unknown1"] = trade[4]
            t_info["duration"] = trade[5]
            t_info["buy_price"] = trade[6]
            t_info["sell_price"] = trade[7]
            t_info["unknown2"] = trade[8]
            t_info["reason"] = trade[9]
            trade_info.append(t_info)

        report["pairs"] = []
        report["wins"] = 0
        report["loss"] = 0
        report["total_profit"] = 0
        report["cum_profit_%"] = 0
        report["duration"] = 0
        for trade in trade_info:
            present = False
            for i, rep in enumerate(report["pairs"]):
                if trade["pair"] in rep["pair"]:
                    report["pairs"][i]["buys"] += 1
                    report["pairs"][i]["cum_profit_%"] += trade["percentage"]
                    report["pairs"][i]["duration"] += trade["duration"]
                    report["pairs"][i]["profit"] += trade["percentage"] * 0.001
                    if t_info["percentage"] >= 0:
                        report["pairs"][i]["wins"] += 1
                    else:
                        report["pairs"][i]["loss"] += 1
                    present = True
            
            if not present:
                info = {}
                info["pair"] = trade["pair"]
                info["buys"] = 1
                info["cum_profit_%"] = trade["percentage"]
                info["duration"] = trade["duration"]
                info["profit"] = trade["percentage"] * 0.001
                if trade["percentage"] >= 0:
                    info["loss"] = 0
                    info["wins"] = 1
                else:
                    info["loss"] = 1
                    info["wins"] = 0
                report["pairs"].append(info)

        for rep in report["pairs"]:
            report["wins"] += rep["wins"]
            report["loss"] += rep["loss"]
            report["total_profit"] += rep["profit"]
            report["cum_profit_%"] += rep["cum_profit_%"]
            report["duration"] += rep["duration"]
            rep["avg_profit_%"] = rep["cum_profit_%"] / rep["buys"]
            rep["avg_duration"] = rep["duration"] / rep["buys"]

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