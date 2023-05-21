from Data_base_tool import DatabaseIteraction

from Dmarket_main import initialization,sale_items, update_selling_items ,sold_items,update_offers
import time

def main():
    initialization()
    
    n = 0 
    while True :
        
        time.sleep(900)
        n += 1
        sale_items()
        update_selling_items()
        sold_items()
        if n % 144 == 0 :
            update_offers()

main()