from Data_base_tool import DatabaseIteraction
import csv 
from dm_evaluation import calculate_dm_signal
from steam_data_collector import Steam
from dmarket_info import calculate_sale_price
from dmarket_info import claculate_price_approval

steam_connector= Steam()
db_connector = DatabaseIteraction()

def additems():
    with open(r'buff_new.csv', newline = '', encoding="utf8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        
        items = list(csv_reader)

    n = 0 
    it_count =0 
    for item in items[1:] :
            
            item = item[0]
            print(item)
            dm_signal = calculate_dm_signal(item)

            if dm_signal :
                print('dm', item)
                selling_price = calculate_sale_price(item)

                         
                it_count += 1
                price_approval = claculate_price_approval(item)
           
             
                    

                if price_approval:
                    n += 1
                    db_connector.AddItemsInOperation(str(n), item)
                    print('steam', item)
                
       
   









