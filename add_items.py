from Data_base_tool import DatabaseIteraction
import csv 
from dm_evaluation import calculate_dm_signal
from steam_data_collector import Steam
from dmarket_info import calculate_sale_price
from dmarket_info import claculate_price_approval

steam_connector= Steam()
db_connector = DatabaseIteraction()

def additems():
    special_add_list = ['AK-47 | Elite Build (Battle-Scarred)', 'Dual Berettas | Cobalt Quartz (Factory New)',
    'Desert Eagle | Bronze Deco (Factory New)','Desert Eagle | Bronze Deco (Minimal Wear)',
    'MP9 | Goo (Field-Tested)','StatTrak™ AK-47 | Elite Build (Field-Tested)','StatTrak™ Desert Eagle | Oxide Blaze (Field-Tested)',
    'UMP-45 | Exposure (Field-Tested)','USP-S | Torque (Minimal Wear)','PP-Bizon | Candy Apple (Factory New)',
    'StatTrak™ AK-47 | Uncharted (Minimal Wear)','Shattered Web Case','SCAR-20 | Enforcer (Minimal Wear)',
    'MAC-10 | Allure (Well-Worn)','MP5-SD | Kitbash (Field-Tested)','MAG-7 | Carbon Fiber (Factory New)',
    'Desert Eagle | Trigger Discipline (Well-Worn)','Stockholm 2021 Contenders Sticker Capsule','Sticker | Team Liquid (Holo) | Stockholm 2021',
    'Antwerp 2022 Challengers Autograph Capsule','Rio 2022 Challengers Sticker Capsule','Rio 2022 Champions Autograph Capsule','M4A1-S | Emphorosaur-S (Minimal Wear)',
    'MAC-10 | Sakkaku (Field-Tested)','M4A1-S | Mud-Spec (Minimal Wear)','Paris 2023 Contenders Sticker Capsule','Paris 2023 Challengers Sticker Capsule',
    'Sticker | Vitality (Glitter) | Paris 2023','Paris 2023 Mirage Souvenir Package']
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
    print(len(items))
    for item in items[1:] :
            
            item = item[0]
            
            dm_signal = calculate_dm_signal(item)
            print(item, dm_signal)

            if dm_signal :
                print('dm', item)
                selling_price = calculate_sale_price(item)

                         
                it_count += 1
                price_approval = claculate_price_approval(item)
           
             
                    

                if price_approval:
                    n += 1
                    db_connector.AddItemsInOperation(str(n), item)
                    print('steam', item)
                
       
   









