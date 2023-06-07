from Data_base_tool import DatabaseIteraction
import csv 
from dm_evaluation import calculate_dm_signal
from steam_data_collector import Steam
from dmarket_info import calculate_sale_price
from dmarket_info import claculate_price_approval
import time 

steam_connector= Steam()
db_connector = DatabaseIteraction()

def additems():
    special_add_list = []
    n =0 
    if len(special_add_list) > 0 :
        for i in special_add_list:
            n += 1 
            db_connector.AddItemsInOperation(str(n), i)
        return

        
    with open(r'buff_new.csv', newline = '', encoding="utf8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        
        items = list(csv_reader)

    n = 0 
    it_count =0 
   
    for item in items[1:] :
            it_count+= 1
            item = item[0]
            if it_count % 10  == 0:
                time.sleep(5)
            dm_signal = calculate_dm_signal(item)
            

            if dm_signal :
                

                n += 1
                db_connector.AddItemsInOperation(str(n), item)
             
                
                
       
   









