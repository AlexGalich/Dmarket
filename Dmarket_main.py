from dmarket_info import order_evaluation, calculate_sale_price,calculate_target_update
from Data_base_tool import DatabaseIteraction
from dmarket import place_target
from dmarket import get_invetory_items, get_available_inventory, construct_dict , put_on_sale  , remove_target, update_sale_price, get_closed_offers, balance_evaluation
import datetime
from add_items import additems
import time

db_connection = DatabaseIteraction()
def initialization():
    db_connection.create_dbs()
    # add the items
    if len(db_connection.GetItemsInOperation()) == 0:
        additems()
    items_in_operation  = db_connection.GetItemsInOperation()
    for item in items_in_operation:
            
            value = order_evaluation(item[1])
            print(value)
            
           
            
            print(value[0])
            if value[0] == True:
                quantity = '5'
            
                if value[0] == True:
                    # returns the information after the item target was placed
                    placing_return = place_target(item[1],quantity , value[1])
                

                    target_id = placing_return['Result'][0]['TargetID']
                    status = placing_return['Result'][0]['Successful']
                    

                    if status ==  True :
                        # initialize variables 
                        name_id = item[0]
                        target_price = value[1]
                        offer_price = value[2]
                        current_time= round(time.time())

                        # add value to current targets db
                        db_connection.AddTarget(target_id, name_id, target_price, quantity, offer_price)

                        # Add value to targets history
                        db_connection.AddTargetHist(target_id, name_id, target_price, quantity, offer_price,current_time)
       
    
    
def sale_items():
    full_invetory = get_invetory_items()
    available_inventory = get_available_inventory(full_invetory)
    items_dictionary = construct_dict(available_inventory)
    print("dict", items_dictionary)
    for item_name in items_dictionary:
        # Check if the item is currently selling 
        print("name",item_name)
        item_id = db_connection.GetItemId(item_name)
        current_price = db_connection.GetItemCurrentSellingPrice(item_id)

        if current_price == None:
            # Calculate the selling price
            sale_price = calculate_sale_price(item_name)
        else :
            # Assign the current selling price
            sale_price = current_price[0]

        # Get a list of item_id numbers
        items_id_list = items_dictionary[item_name]['item_ids']

        # Sale the item
        for id in items_id_list:
            # Get the return information from the sale operation, which includes dictionary with offer_id , asset_id
            return_info = put_on_sale(id, sale_price) # Put the item on sale
            
            # Get the needed data for adding the record to the db 
            asset_id = return_info['Result'][0]['CreateOffer']['AssetID']
            offer_id = return_info['Result'][0]['OfferID']
            target_id = db_connection.GetTargetID(item_id)
            current_time= round(time.time())
            
            # Add the item to the db
            db_connection.AddItemOnSale(offer_id, asset_id, item_id,target_id,sale_price,current_time)

        
        # Update order amount in the db
        db_connection.UpdateOrderAmount(item_id, len(items_id_list))

        price_amount =  db_connection.GetOrderPriceAmount(item_id)
    
        highest_target_price = items_dictionary[item_name]['highest_target']
        expected_sale_price  = round(calculate_sale_price(item_name),2)
        

        if price_amount[1] == 0:

            # Delete the current starget from the db 
             # Delete the current target from the Dmarket 
            target_id = db_connection.GetTargetID(item_id)[0]

            db_connection.DeleteTarget(item_id)
            
            value = order_evaluation(item_name)
            update_target_price= value[1]
          
            quantity = 5
            eval_value  = order_evaluation(item_name, update_target_price)[0][0]
            print("evaluation value is ", eval_value)
            if eval_value == True :
                if balance_evaluation(update_target_price, int(quantity)) == True:
                    # Create a new target and save to the databese
                
                    placing_return  = place_target(item_name, quantity, update_target_price)
                    current_time= round(time.time())
                    
                    
                    status = placing_return['Result'][0]['Successful']
                    
                    new_target_id = placing_return['Result'][0]['TargetID']
                
                    if status == True : 

                        # add value to current targets db
                        db_connection.AddTarget(new_target_id, item_id, update_target_price, quantity, expected_sale_price)

                        # Add value to targets history
                        db_connection.AddTargetHist(new_target_id, item_id, update_target_price, quantity, expected_sale_price,current_time)

def  update_selling_items() :
    current_time= round(time.time())
    items_update = db_connection.GetItemsThreeDays(current_time, 3)        
    if len(items_update) == 0:
        print("there are no items to update")
        return
    else:
        for item in items_update:

            # Extract all the infromation from db request
            offer_id = item[0]
            item_id = item[1]
            name_id = item[2]

            # Get the item name
            item_name = db_connection.GetItemName(name_id)

            # Calculate the price for an update
            new_sale_price  = round(calculate_sale_price(item_name),2)

            # Update the sale price
            update_return = update_sale_price(item_id, offer_id, new_sale_price)

            success_result  = update_return['Result'][0]['Successful']
            if success_result == True:
                new_offer_id = update_return['Result'][0]['NewOfferID']
                db_connection.UpdateItemInfo(new_offer_id, new_sale_price,name_id)
def sold_items():
    # Get all the closed deals
    closed_offers = get_closed_offers()
    for offer in closed_offers:
        # Get the offer id of each deal
        closed_offer_id = offer['OfferID']

        # Check if the item with this offerID is on sale
        item_data = db_connection.GetItemsOfferID(closed_offer_id)

        if item_data == None:
            continue
        else: 
            # Delete the offer from the db
            db_connection.DeleteSaleItem(closed_offer_id)

            # Get the current time and add the record to the db
            sale_time  = round(time.time())
            db_connection.AddHistorySale(item_data[0],item_data[1],item_data[2],item_data[3],item_data[4], item_data[5],sale_time)
  # Update the sale price
def update_offers():
    # Get all offers older then 36 hours 
    current_time = round(time.time())
    id_list = db_connection.GetOldTargets(current_time)

    # Check if there is at least one 
    if len(id_list) == 0:
        return
    else:
        for i in id_list:
            target_id = i[0]

            # Get items on sale or sold from this target
            selling_items = db_connection.GetSeelingItemsByTarget(target_id)
            sold_items = db_connection.GetSoldItemsByTarget(target_id)

            # Check if there is at least one sale or buy
            if selling_items != None or sold_items != None :
                continue
            else :

                # Remove the targets
                remove_target(target_id)
                db_connection.DeleteTargetID(target_id)

    # Get items for which there is no target placed
    not_used_items = db_connection.GetNotUsedItems()   
    for item in not_used_items:
        
        value = order_evaluation(item[1])
        
        if value[0] == True:
            quantity = '5'
            # Check is there is enough money for the target to be placed
            if balance_evaluation(value[1], int(quantity))  == True:
                # returns the information after the item target was placed
                placing_return = place_target(item[1],quantity , value[1])

                target_id = placing_return['Result'][0]['TargetID']
                status = placing_return['Result'][0]['Successful']
                

                if status ==  True :
                    # initialize variables 
                    name_id = item[0]
                    target_price = value[1]
                    offer_price = value[2]
                    current_time= round(time.time())

                    # add value to current targets db
                    db_connection.AddTarget(target_id, name_id, target_price, quantity, offer_price)

                    # Add value to targets history
                    db_connection.AddTargetHist(target_id, name_id, target_price, quantity, offer_price,current_time) 

