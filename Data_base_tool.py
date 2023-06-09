import psycopg2
class DatabaseIteraction:

    hostname = 'containers-us-west-31.railway.app'
    database = 'railway'
    username = 'postgres'
    pwd = 'uLyKfRFAiiWeV0mFOMkB.'
    port_id = 7341
    DB_URI = 'postgresql://postgres:uLyKfRFAiiWeV0mFOMkB@containers-us-west-31.railway.app:7341/railway'

    def connect(self):
        conn = psycopg2.connect(DatabaseIteraction.DB_URI)
        return conn
    
    def create_dbs(self):
        conn = self.connect()
        cur = conn.cursor()

        items_in_operation = ''' CREATE TABLE IF NOT EXISTS items_operation(
                    name_id varchar(128) NOT NULL,
                    item_name   varchar(128) NOT NULL
            )'''
        

        items_on_sale = '''CREATE TABLE IF NOT EXISTS item_on_sale(
                    offer_id varchar(128),
                    item_id varchar(128),
                    name_id varchar(128) NOT NULL,
                    target_id varchar(128),
                    offer_price float(8),
                    buy_time int
                    )'''

        price_update_hist = '''CREATE TABLE IF NOT EXISTS price_update_hist(
                    offer_id varchar(128),
                    old_price float(8),
                    new_price float(8),
                    update_time int
                    )'''
        
        sold_items = '''CREATE TABLE IF NOT EXISTS sold_items(
                    offer_id varchar(128),
                    item_id varchar(128),
                    name_id varchar(128) NOT NULL,
                    target_id varchar(128),
                    offer_price float(8),
                    buy_time int,
                    sale_time int
                    )'''


        targets  = '''CREATE TABLE IF NOT EXISTS targets(
                    target_id varchar(128) NOT NULL,
                    name_id   varchar(128) NOT NULL,
                    target_price float(8) NOT NULL,
                    target_amount int NOT NULL,
                    offer_price float(8))'''
        

        
        
        targets_hist = '''CREATE TABLE IF NOT EXISTS target_hist(
                    target_id varchar(128) NOT NULL,
                    name_id   varchar(128) NOT NULL,
                    target_price float(8) NOT NULL,
                    target_amount int NOT NULL,
                    offer_price float(8),
                    time int
                    )'''
        

        cur.execute(items_in_operation)
        cur.execute(items_on_sale)
        cur.execute(price_update_hist)
        cur.execute(sold_items)
        cur.execute(targets)
        cur.execute(targets_hist)
    
        conn.commit()

        cur.close()
        conn.close()
    # Returns a list of tuples(id, item_name)
    def GetItemsInOperation(self):

        conn = self.connect()
        cur = conn.cursor()
        
        check_script = '''SELECT *
                            FROM items_operation;'''

        cur.execute(check_script)

        items = cur.fetchall()

        conn.commit()

        return items
    # name_id is taken as an integer , and item_name -> string
    def AddItemsInOperation(self,name_id, item_name):
        conn = self.connect()
        cur = conn.cursor()

        add_record = '''Insert into items_operation values(%s,%s)'''
        

        cur.execute(add_record,(name_id,item_name,))
        conn.commit()

        cur.close()
        conn.close()

    # returns an integer value of of the last id number
    def GetLastItemId(self,):
        
        id = DatabaseIteraction().GetItemsInOperation()[-1][0]
        return id

    # takes in a item_name in string format
    def DeleteItems(self, item_name):
        conn = self.connect()
        cur = conn.cursor()

        add_record = '''DELETE FROM items_operation
                        WHERE item_name = (%s)'''
        

        cur.execute(add_record,(item_name,))
        conn.commit()

        cur.close()
        conn.close()

    # returns an id number as an integer 
    def GetItemId(self, item_name):

        conn = self.connect()
        cur = conn.cursor()
        
        check_script = '''SELECT name_id
                            FROM items_operation
                            WHERE item_name = %s;'''

        cur.execute(check_script, (item_name,))

        items = cur.fetchone()[0]

        conn.commit()

        return items 
    
    def GetItemName(self, item_id):
        conn = self.connect()
        cur = conn.cursor()
        
        check_script = '''SELECT item_name
                            FROM items_operation
                            WHERE name_id = %s;'''

        cur.execute(check_script, (item_id,))

        items = cur.fetchone()[0]

        conn.commit()

        return items

    def GetNotUsedItems(self):
        conn = self.connect()
        cur = conn.cursor()
        
        check_script = '''Select *
                        From items_operation
                        WHERE name_id NOT IN
                                (SELECT name_id  
                                FROM targets)'''

        cur.execute(check_script)

        items = cur.fetchall()

        conn.commit()

        return items
        
    # TARGETS ---------------------------------------------------------------
    def AddTarget(self,targe_id, name_id, target_price, target_amount, offer_price):
        
        conn = self.connect()
        cur = conn.cursor()

        add_record_script = '''Insert into targets values(%s,%s,%s,%s,%s)'''
        
        add_values = (targe_id, name_id, target_price, target_amount, offer_price,)
        
        cur.execute(add_record_script,(add_values))
        conn.commit()

        cur.close()
        conn.close()

    

    def DeleteTarget(self,name_id):
        conn = self.connect()
        cur = conn.cursor()

        add_record = '''DELETE FROM targets
                        WHERE name_id = (%s)'''
        

        cur.execute(add_record,(name_id,))
        conn.commit()

        cur.close()
        conn.close()

    def DeleteTargetID(self,target_id):
        conn = self.connect()
        cur = conn.cursor()

        add_record = '''DELETE FROM targets
                        WHERE target_id = %s'''
        

        cur.execute(add_record,(target_id,))
        conn.commit()

        cur.close()
        conn.close()

    def UpdateOrderAmount(self, name_id, order_amount):
        conn = self.connect()
        cur = conn.cursor()

        update_record_script = '''UPDATE targets
                        SET target_amount  =  target_amount - %s
                        WHERE name_id = (%s)'''
        

        cur.execute(update_record_script,(order_amount, name_id,))
        conn.commit()

        cur.close()
        conn.close()

    def GetOrderPriceAmount(self, item_id):
        conn = self.connect()
        cur = conn.cursor()
        
        check_script = '''SELECT target_price, target_amount
                            FROM targets
                            WHERE name_id = %s ;'''

        cur.execute(check_script, (item_id,))

        items = cur.fetchone()

        conn.commit()

        return items 

        
    def GetOldTargets(self, current_time):
        

        conn = self.connect()
        cur = conn.cursor()
        
        check_script = '''select targets.target_id 
                    from targets
                    JOIN target_hist as th
                    ON th.target_id = targets.target_id
                    WHERE (%s - th.time) > 129600 '''

        cur.execute(check_script, (current_time,))

        items = cur.fetchall()

        conn.commit()

        return items 
    
    def GetTargetID(self, item_id):
        conn = self.connect()
        cur = conn.cursor()
        
        check_script = '''SELECT target_id
                            FROM targets
                            WHERE name_id = %s;'''

        cur.execute(check_script, (item_id, ))

        items = cur.fetchone()

        conn.commit()

        return items



    def AddTargetHist(self,targe_id, name_id, target_price, target_amount, offer_price, time):
        
        conn = self.connect()
        cur = conn.cursor()

        add_record_script = '''Insert into target_hist values(%s,%s,%s,%s,%s,%s)'''
        
        add_values = (targe_id, name_id, target_price, target_amount, offer_price, time)
        
        cur.execute(add_record_script,(add_values))
        conn.commit()

        cur.close()
        conn.close()

    # ITEMS ON SALE -----------------------------------------------------------
    def AddItemOnSale(self,offer_id, item_id,name_id, target_id, offer_price, buy_time):
        conn = self.connect()
        cur = conn.cursor()

        add_record_script = '''Insert into item_on_sale values(%s,%s,%s,%s,%s,%s)'''
        
        
        
        cur.execute(add_record_script,(offer_id, item_id,name_id, target_id, offer_price, buy_time,))
        conn.commit()

        cur.close()
        conn.close()

    def DeleteSaleItem(self, offer_id):
        conn = self.connect()
        cur = conn.cursor()

        add_record = '''DELETE FROM item_on_sale
                        WHERE offer_id = (%s)'''
        

        cur.execute(add_record,(offer_id,))
        conn.commit()

        cur.close()
        conn.close()

    def GetItemsThreeDays(self, current_date, n_days):
        conn = self.connect()
        cur = conn.cursor()
        
        check_script = '''SELECT offer_id, item_id, name_id
                            FROM item_on_sale
                            WHERE ((%s- buy_time) / (86400 * %s)) > %s ;'''

        cur.execute(check_script, (current_date,n_days,n_days))

        items = cur.fetchall()
        conn.commit()

        return items


    def GetItemCurrentSellingPrice(self,name_id):
        # returns an id number as an integer 
    
        conn = self.connect()
        cur = conn.cursor()
        
        check_script = '''SELECT offer_price
                            FROM item_on_sale
                            WHERE name_id = %s;'''

        cur.execute(check_script, (name_id,))

        items = cur.fetchone()
        conn.commit()

        return items
    
    def UpdateItemInfo(self,new_offer_id, new_price, name_id):
        
        conn = self.connect()
        cur = conn.cursor()

        update_record_script = '''UPDATE item_on_sale
                        SET offer_id = %s,
                            offer_price = %s
                        WHERE name_id = %s'''
        

        cur.execute(update_record_script,(new_offer_id, new_price, name_id,))
        conn.commit()

        cur.close()
        conn.close()

    def GetItemsOfferID(self, offer_id):
        conn = self.connect()
        cur = conn.cursor()
        
        check_script = '''SELECT *
                            FROM item_on_sale
                            WHERE offer_id = %s'''

        cur.execute(check_script, (offer_id,))

        items = cur.fetchone()
        conn.commit()

        return items
    # Get the selling or sold items filetered by target id
    def GetSeelingItemsByTarget(self, target_id):
        conn = self.connect()
        cur = conn.cursor()
        
        check_script = '''SELECT item_id
                            FROM item_on_sale
                            WHERE  target_id = %s'''

        cur.execute(check_script, (target_id,))

        items = cur.fetchone()
        conn.commit()

        return items
    
    def GetSoldItemsByTarget(self, target_id):
        conn = self.connect()
        cur = conn.cursor()
        
        check_script = '''SELECT item_id
                            FROM sold_items
                            WHERE  target_id = %s'''

        cur.execute(check_script, (target_id,))

        items = cur.fetchone()
        conn.commit()

        return items

# Sale history
    def AddHistorySale(self,offer_id, item_id,name_id, target_id, offer_price, buy_time, sale_time):
        conn = self.connect()
        cur = conn.cursor()

        add_record_script = '''Insert into sold_items values(%s,%s,%s,%s,%s,%s,%s)'''
        
        add_values = (offer_id, item_id,name_id, target_id, offer_price, buy_time,sale_time)
        
        cur.execute(add_record_script,(add_values))
        conn.commit()

        cur.close()
        conn.close()







