from Data_base_tool import DatabaseIteraction
import csv 
from dm_evaluation import calculate_dm_signal
from steam_data_collector import Steam
from dmarket_info import calculate_sale_price
steam_connector= Steam()
db_connector = DatabaseIteraction()

def additems():
    with open(r'Dmarket_traiding_bot\buff_new.csv', newline = '', encoding="utf8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        
        items = list(csv_reader)

    dm_list = []
    for item in items[1:] :
        try:
            dm_signal = calculate_dm_signal()

            if dm_signal :
                dm_list.append(item)
        except :
            continue
    n = 0 
    for dm_item in dm_list():
        try:
            selling_price = calculate_sale_price(dm_item)
            
            steam_signal = steam_connector.calculate_steam_signal(selling_price, dm_item)

            if steam_signal:

                n+= 1 
                db_connector.AddItemsInOperation(str(n), dm_item)
        except: continue










