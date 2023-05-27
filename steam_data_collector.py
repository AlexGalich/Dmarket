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
def make_requst(link):
    time.sleep(10)
    proxy = get_proxy()   
    print(proxy)
    request = requests.get(link, proxies=proxy)

    return request


class Steam():
    dollar = get_dollar_price()
    main_link = "https://steamcommunity.com/market/listings/730/"
    


    def consturct_link_new(self,item_name):
        new_string = parse.quote(item_name)

        final_link = Steam.main_link + new_string

        return final_link
    
    # finds id of the product
    def get_id(self, link):
        time.sleep(10)
        proxy = get_proxy()   
        html = requests.get(link,proxies=proxy).text
        soup = BeautifulSoup(html, 'lxml')
        id = None
        for script in soup.find_all('script'):
            id_regex = re.search('Market_LoadOrderSpread\(([ 0-9]+)\)', script.text)
            if id_regex:
                id = id_regex.groups()[0].strip()
                break
        return id
    
    def construct_data_link(self, id):
        data_link = f'https://steamcommunity.com/market/itemordershistogram?country=UA&language=english&currency=18&item_nameid={id}&two_factor=0'
        return data_link 
    

    # a function to extract a list of first 10 sellers offers

    def get_selling_price(self, item_name):
       
        just_link = self.consturct_link_new(item_name)
    

        create_id = self.get_id(just_link)
     
        data_link = self.construct_data_link(create_id)
        
    
       
        print("the data link is", data_link)
        return_d = make_requst(data_link)
        print("status", return_d.status_code)
        if return_d.status_code == 429:
            print('The program is sleeping 90 secs')
            
            return_d = make_requst(data_link)
            print("New code status", return_d.status_code)
        
        requested_obj = return_d.json()

        print("the return obj", requested_obj)
       
    
       
       

        # Convertn price from cents to full numbers
        buy_price_hrn = float(requested_obj['highest_buy_order']) / 100
        sell_price_hrn = float(requested_obj['lowest_sell_order']) / 100


        buy_price_usd = round(buy_price_hrn/ Steam.dollar,2)
        sell_price_usd = round(sell_price_hrn / Steam.dollar, 2)
        return buy_price_usd, sell_price_usd

    def get_past_month_sales(self,item_name ):

        name_encoded = parse.quote(item_name)
        url = f"https://steamcommunity.com/market/pricehistory/?appid=730&market_hash_name={name_encoded}"
    
        return_obj = make_requst(url,).json()['prices']
      
        return_obj = return_obj[::-1]
        
        return return_obj

    def get_avg_month(self, sales_list):
        dates_sum = {}
        for item in sales_list:
            date_parts = item[0].split()

            date_only = " ".join(date_parts[:3])
            dates_sum[date_only] = dates_sum.get(date_only,0) +  float(item[1])
            if len(dates_sum) >= 15:
                break
        
        dates_count = {}
        for item in sales_list:
            date_parts = item[0].split()
            date_only = " ".join(date_parts[:3])
            dates_count[date_only] =  dates_count.get(date_only, 0) +1 
            if len(dates_count) >= 15:
                break

        date_list = []
        for key in dates_sum:
            day_avg_hrn = dates_sum[key]/ dates_count[key]
            day_avg_usd = round((day_avg_hrn/ Steam.dollar),2)
            date_list.append(day_avg_usd)

        
        return  date_list[::-1]

    def calculate_grpath_sign(self, data):


        x = np.arange(len(data))  # Generate x values as indices (0, 1, 2, ...)
        slope = np.polyfit(x, data, 1)[0]
        mean_value = statistics.mean(data) 
        slope_mean_ratio = slope / mean_value

        std_mean_ration = statistics.stdev(data) / mean_value

        return slope_mean_ratio,std_mean_ration
        

    def calculate_steam_signal(self, selling_price, item_name):
       
       
       
        traget_price , offer_price = self.get_selling_price(item_name)
       
        


        if selling_price <= (offer_price - (traget_price * 0.07)):
            
            data_ext = self.get_past_month_sales(item_name)
            mean_list  = self.get_avg_month(data_ext)
            slope_mean_ratio,std_mean_ration = self.calculate_grpath_sign(mean_list)

            if slope_mean_ratio >= -0.008 :
                if std_mean_ration <= 0.06:
                    return True 
            
        return False 

        






