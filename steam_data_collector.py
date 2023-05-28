import requests 
from bs4 import BeautifulSoup
import re
import requests
import json
from urllib import parse 
from dollar_price import get_dollar_price
import numpy as np
import statistics
import time
from proxy import get_proxy
import datetime

class Steam():
    dollar = get_dollar_price()
    
    

    # a function to extract a list of first 10 sellers offers

    def get_selling_price(self, item_name):
        name_encoded = parse.quote(item_name)
        try:
            current_sale_price = requests.get(f'https://www.csgostocks.de/api/prices/price/keyfigures/{name_encoded}').json()['steam']['current_price']
        except: 
            print("There is no selling price for", item_name)
            current_sale_price = None
        return current_sale_price

    def get_avg_month(self, item_name):
        name_encoded = parse.quote(item_name)
        dates_sum = {}
        dates_count = {}
        return_obj = requests.get(f'https://www.csgostocks.de/api/prices/price/{name_encoded}?name={name_encoded}').json()['data'][-720:]
        for i in return_obj[::-1]:
            date_only = str(datetime.datetime.fromtimestamp(i[0])).split(' ')[0]
        
            dates_sum[date_only] = dates_sum.get(date_only,0) +  float(i[1])
            dates_count[date_only] = dates_count.get(date_only, 0) + 1
            if len(dates_sum) >= 10:
                        break
        date_list = []

        for key in dates_sum:
        
            day_avg  = round(dates_sum[key]/ dates_count[key],2)
            date_list.append(day_avg)
       

        
        return  date_list[::-1]

    def calculate_grpath_sign(self, data):


        x = np.arange(len(data))  # Generate x values as indices (0, 1, 2, ...)
        slope = np.polyfit(x, data, 1)[0]
        mean_value = statistics.mean(data) 
        slope_mean_ratio = slope / mean_value

        std_mean_ration = statistics.stdev(data) / mean_value

        return slope_mean_ratio,std_mean_ration
        

    def calculate_steam_signal(self, selling_price, item_name):
       
       
       
        offer_price = self.get_selling_price(item_name)
        if offer_price == None:
            return False


        if selling_price <= (offer_price - (offer_price * 0.1)):
            
            
            mean_list  = self.get_avg_month(item_name)
            slope_mean_ratio,std_mean_ration = self.calculate_grpath_sign(mean_list)

            if slope_mean_ratio >= -0.008 :
                if std_mean_ration <= 0.06:
                    return True 
            
        return False 

        








