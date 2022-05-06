import json
import requests
import argparse
import pandas as pd
#import plotext as plt
import matplotlib.pyplot as plt



class Plotter(object):
    """

    This is class used to plot the graph of number of active users per date

    input parameters:
    url : This is the url that contains the data needed.
    start_date: used to filter the data to get the first date needed
    end_date: used to filter the data to get the last date needed
    graph_type: used to display graph in either bar format or pie format


    """
    
    def __init__(self, url, start_date, end_date, graph_type = "bar"):
        self.url = url
        self.start_date = start_date
        self.end_date = end_date
        self.keys_ = None
        self.values_ =None
        self.plt_type = graph_type
        
    def get_data_(self):
        data = requests.get(self.url)
        assert data.status_code == 200, f"status code is not 200, received status code is: {data.status_code}"
        data = json.loads(data.text)
        return data
    
    def extract_key_value_(self, data):
        self.keys_ = data.keys()
        self.values_ = data.values()
        return 
        
    def extract_data_(self):
        key_list = list(self.keys_)
        val_list = list(self.values_)    
        start_index = key_list.index(self.start_date)
        end_index = key_list.index(self.end_date) + 1
        self.keys_ = key_list[start_index: end_index]
        self.values_ = val_list[start_index: end_index]
        return 
        
    def plot_graph_(self):
        
        if self.plt_type == "bar":
            plt.bar(self.keys_, self.values_)
            plt.xticks(rotation=90)
            plt.show(block=True)
        else:
            plt.pie(self.values_, labels=self.keys_)
            plt.show(block=True)
        return 
        
    
    def plot(self):
        
        self.extract_key_value_(self.get_data_())
        
        assert self.start_date in self.keys_, f"The provided start date does not exist, earliest date available is: {list(self.keys_)[0]}."
        assert self.end_date in self.keys_, f"The provided end date does not exist, latest date available is: {list(self.keys_)[-1]}."
        
        #This function updates the key value parameters with the new info
        self.extract_data_()
        self.plot_graph_()
        
        return 


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-sd', '--start_date', action='store', type=str, required=True, help="Start date")
    parser.add_argument('-ed','--end_date', action='store', type=str, required=True, help="End date")
    parser.add_argument('-gt','--graph_type', action='store', type=str, required=False, help="Plot type, choose between bar and pie, default bar")
    args = parser.parse_args()
    url = "http://sam-user-activity.eu-west-1.elasticbeanstalk.com/"


    if args.graph_type:
        result = Plotter(url, start_date = args.start_date, end_date = args.end_date, graph_type=args.graph_type)
    else:
        result = Plotter(url, start_date = args.start_date, end_date = args.end_date)
    result.plot()
