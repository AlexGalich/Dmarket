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
    header = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
            'Cookie' : 'ActListPageSize=100; steamMachineAuth76561198314485108=7EE8F422D3417741FB4C9A392C77510C02444FB2; browserid=2549629317044310014; _ga=GA1.2.2100762397.1669573121; Steam_Language=english; cookieSettings=%7B%22version%22%3A1%2C%22preference_state%22%3A1%2C%22content_customization%22%3Anull%2C%22valve_analytics%22%3Anull%2C%22third_party_analytics%22%3Anull%2C%22third_party_content%22%3Anull%2C%22utm_enabled%22%3Atrue%7D; extproviders_730=steamanalyst; recentlyVisitedAppHubs=730; totalproviders_730=steamanalyst; timezoneOffset=7200,0; strInventoryLastContext=730_2; steamCurrencyId=18; sessionid=d801ed976c7c6cca015f3ac7; _gid=GA1.2.972757476.1685136348; steamLoginSecure=76561198314485108%7C%7CeyAidHlwIjogIkpXVCIsICJhbGciOiAiRWREU0EiIH0.eyAiaXNzIjogInI6MEQyNl8yMjU3NzVCNF9FMDUyNCIsICJzdWIiOiAiNzY1NjExOTgzMTQ0ODUxMDgiLCAiYXVkIjogWyAid2ViIiBdLCAiZXhwIjogMTY4NTIyMzUyNywgIm5iZiI6IDE2NzY0OTYzNTMsICJpYXQiOiAxNjg1MTM2MzUzLCAianRpIjogIjBEMjFfMjI5NkUyM0ZfQzU1OEMiLCAib2F0IjogMTY4MDg5NTkwMywgInJ0X2V4cCI6IDE2OTg3MDcwNzEsICJwZXIiOiAwLCAiaXBfc3ViamVjdCI6ICI2Mi4yMTQuMS4yNTAiLCAiaXBfY29uZmlybWVyIjogIjYyLjIxNC4xLjI1MCIgfQ.5vFn5OJMc7And5AX9ldVgs5oebXrWnoR0boS95N2waziLYsZfzRe5IIHo0RgNtWSBSJyu0UpJE4ulmqC8ArlAA; webTradeEligibility=%7B%22allowed%22%3A1%2C%22allowed_at_time%22%3A0%2C%22steamguard_required_days%22%3A15%2C%22new_device_cooldown_days%22%3A0%2C%22time_checked%22%3A1685136353%7D; steamCountry=CA%7Ca621bc23b38ac7c8a38c16512688b510'
        }
    time.sleep(10)
    proxy = get_proxy()   
    print(proxy)
    request = requests.get(link, proxies=proxy, headers=header)

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
        header = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
        }
        html_main = requests.get(link, headers=header)
        print("id",html_main.status_code)
        html = html_main.text
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
        print("three month url", url)
    
        
        request_main = make_requst(url)
        print("request_main",request_main.status_code)
        return_obj = request_main.json()['prices']
        print(return_obj)     #json()['prices']
      
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

        






