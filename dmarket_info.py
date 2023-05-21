import requests 
from bs4 import BeautifulSoup
import time 
import statistics
import json
from datetime import datetime
from urllib import parse


items_on_sale = {}

# change url to prod
rootApiUrl = "https://api.dmarket.com"

# Create a function to encode item to a link
def encode_item(item_name):
    new_string = parse.quote(item_name)

    return new_string

def calculate_seconds(date_from, date_to):
   
    time_difference = date_to - date_from 
    days_sale = time_difference.days * 86400
    second_sale = time_difference.seconds
    time_difference_seconds = days_sale+ second_sale
 
    return round((time_difference_seconds / 3600) , 2)

def get_item_market_info(encoded_item):
    market_response = requests.get(f'https://api.dmarket.com/marketplace-api/v1/cumulative-price-levels?Title={encoded_item}&GameID=a8db')
    
    orders = json.loads(market_response.text)
    return orders

def extract_item_information(item_information, targets = True):
    if targets == True:
        data = 'Targets'
    else: data = 'Offers'

    extraction_data = item_information[data]

    return_obj = {'Prices': [],
                  'Amount': []}
    
    if len(extraction_data) >= 5:
        orders_amount = 5
    else: orders_amount = len(extraction_data)
   

    for i in range(orders_amount):
        return_obj['Prices'].append(float(extraction_data[i]['Price']))
        return_obj['Amount'].append(float(extraction_data[i]['Amount']))

    return return_obj
       
        


def extract_sales_history(encoded_item):
    market_response = requests.get(f'https://api.dmarket.com/marketplace-api/v1/last-sales?Title={encoded_item}&GameID=a8db&Currency=USD')
 
    sales = json.loads(market_response.text)['LastSales']

    return sales




def extract_sales_information(sales_info):
    if sales_info != None:
        return_obj = {'total_count': len(sales_info)}
        print(return_obj)
        Date = []
        Price = []
        last_record = None
        time_diff = []
        last_20_sales = []
        for sale in sales_info:

            Date.append(int(sale['Date']))
            Price.append(int(sale['Price']['Amount']))

            if len(last_20_sales) < 20:
                last_20_sales.append(int(sale['Price']['Amount'])/100)
            
            if last_record == None :
                last_record = datetime.fromtimestamp(int(sale['Date']))
               
            else: 
                new_record = datetime.fromtimestamp(int(sale['Date']))
                time_diff.append(calculate_seconds(new_record ,last_record))
                last_record = datetime.fromtimestamp(int(sale['Date']))
        try:
            return_obj['min_price'] = min(Price) /100
        except:
            return_obj['min_price'] = 0
        try:
            return_obj['max_price'] = max(Price)/100
        except :
            return_obj['max_price'] = 0 
        return_obj['mean_price'] = statistics.mean(Price) / 100
        return_obj['mode_price'] = statistics.mode(Price)/ 100
        return_obj['last_sale'] = calculate_seconds( datetime.fromtimestamp(int(sales_info[0]['Date'])), datetime.now())
        return_obj['avg_sale_time'] = statistics.mean(time_diff) 
        return_obj['last_10_sales'] = last_20_sales

        return return_obj
    return None 

tick = time.time()
def calculate_sale_price(item_name):
    sale_price = None
    encoded_item = encode_item(item_name)

    
    item_info = get_item_market_info(encoded_item)
 
    offers_information = extract_item_information(item_info, False)
    orders_information = extract_item_information(item_info, True)

    sales_history = extract_sales_history(encoded_item)
    sales_information = extract_sales_information(sales_history)


    

    # Calculate minimum offered price -7%
    offer_price_7 = round((offers_information['Prices'][0] * 0.93),2)
    offer_price_10 = round((offers_information['Prices'][0]* 1.1 ),2)



    # Calculate the number of items sold , the price of which is more then current selling price or is more then -5%
    count = 0 
    for item in sales_information['last_10_sales']:
      
        
        if  offer_price_7 >= float(item) <= offer_price_10 :
           
            count += 1
    
 
    if count < 5:
       

        # calculate mean of items sold only buy offers
        offers_sold =  [item for item in sales_information['last_10_sales'] if item not in orders_information['Prices']]
        
        try:
            offers_sold_mean = sum(offers_sold) / len(offers_sold)
            sale_price = round(((offers_sold_mean + offers_information['Prices'][0]) / 2),2)
            
        except:
            sale_price = round(((sales_information['mean_price'] + offers_information['Prices'][0]) / 2),2)


        if sale_price > offers_information['Prices'][0]:
            return round(offers_information['Prices'][0] * 0.98, 2)
       
        return sale_price
    

    
    
    else:
       
        if (offers_information['Prices'][0] * 0.32)<= (offers_information['Prices'][1] - offers_information['Prices'][0]) >= (0.20 * offers_information['Prices'][0]) and offers_information['Amount'][0] <= 4   :

            # calculate if second offer is selling actively 
            second_off_95 = offers_information['Prices'][1] * 0.95
            second_off_110 = offers_information['Prices'][1] * 1.05

            sold_second_offer = [item for item in sales_information['last_10_sales'] if second_off_95 <= item <= second_off_110]
            if len(sold_second_offer)  >= 4:
                return round(offers_information['Prices'][1] * 0.95,2)
            
            else:
                return round(offers_information['Prices'][1] * 0.87, 2)



        if (offers_information['Prices'][1] - offers_information['Prices'][0]) >= (0.06 * offers_information['Prices'][0]) and offers_information['Amount'][0] <= 2:
            

            return round(offers_information['Prices'][0] * 1.03,2) 
        
        elif (offers_information['Prices'][1] - offers_information['Prices'][0]) >=0.02 and offers_information['Amount'][0] <= 2:
        
            
            return offers_information['Prices'][0] + 0.01
        else :
            

            return offers_information['Prices'][0] - 0.01
    

            
    
def calculate_order_price(item_name):
    encoded_item = encode_item(item_name)

    
    item_info = get_item_market_info(encoded_item)
    offers_information = extract_item_information(item_info, False)
    orders_information = extract_item_information(item_info, True)

    sales_history = extract_sales_history(encoded_item)
    sales_information = extract_sales_information(sales_history)

    possible_orders = [price for price in orders_information['Prices'] if offers_information['Prices'][0] > price]

    

    # If there is no order which is smaller then offer prices 
    if len(possible_orders) == 0 :
        order_price = round(orders_information['Prices'][-1] * 0.95,2)
        
        return  order_price
    # if there is an order which is lower then offer prices 
    else: 
        sales = sales_information['last_10_sales']
        suggested_price = None
        for order_price in possible_orders:
                
                if (order_price) in sales:
                    if suggested_price == None :
                        suggested_price = order_price + 0.01

        if suggested_price == None :
            suggested_price = possible_orders[0] +0.01
            return suggested_price
        else :
            
            return suggested_price 

def get_general_item_info(item_name):
    encoded_item = encode_item(item_name)

    
    item_info = get_item_market_info(encoded_item)
    offers_information = extract_item_information(item_info, False)

    
    sales_history = extract_sales_history(encoded_item)
    sales_information = extract_sales_information(sales_history)
    
    return_obj = (sales_information['mean_price'], sales_information['avg_sale_time'])
    return return_obj

def order_evaluation(item_name, order_price = None):

    item_info = get_general_item_info(item_name)
    
    if order_price == None :
        order_price = calculate_order_price(item_name)
    else :
        order_price = order_price

    sale_price = round(calculate_sale_price(item_name),2)
    sale_price_fee = round(sale_price * 0.97,2)
    
    price_diff = sale_price_fee - order_price

    # Calculate 6% from the order price
    order_price_6 = order_price * 0.06

    if price_diff >= 0.04 and price_diff >= order_price_6:
        return (True , order_price, sale_price) , item_info
    else: 
        return (False , order_price, sale_price), item_info
    

def calculate_target_update(lowes_target, current_target, sale_price):
    
    sale_price_without_fee = round(sale_price - (0.03 * sale_price),2)
    expected_difference_prec = (sale_price_without_fee - current_target) / sale_price
    target_difference  = round((current_target - lowes_target) / current_target,2)


    if target_difference > 0.30 :
        new_target = round(current_target - (0.10 * current_target),2)
        return True, new_target
    elif target_difference > 0.1 :
        new_target = round(current_target - (0.05 * current_target),2)
        return True, new_target
    elif target_difference > 0.05 :
        new_target = round(current_target - (0.02 * current_target),2)
        return True, new_target
    else: 
        return False ,current_target


            
#print(order_evaluation('Sticker | Eternal Fire (Glitter) | Antwerp 2022'))
