import requests 
from bs4 import BeautifulSoup
import json
from datetime import datetime
from urllib import parse





# change url to prod
rootApiUrl = "https://api.dmarket.com"
public_key = "4376fe330686cec7a76f1f6709db960009d56547329c76a117fbcb5eb4b17357"

# change url to prod
rootApiUrl = "https://api.dmarket.com"

# Create a function to encode item to a link
def encode_item(item_name):
    new_string = parse.quote(item_name)

    return new_string


# Get the balance in the usd cents (1 dollar = 100)
def get_balance():
    header = {'authorization': 'eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiIyMTJlMDEzMC03ZjQ4LTQwNGMtODE5NC1jMWViMTBmZDZlM2YiLCJleHAiOjE2ODg0MDcyNTIsImlhdCI6MTY4NTgxNTI1Miwic2lkIjoiMDk4ODkwZjctNjI1OC00ZTcxLWJkY2ItZTQ4Y2Y4MmE1ZGZhIiwidHlwIjoiYWNjZXNzIiwiaWQiOiIxNjViMWE3Yy1kZDZmLTQ0YzYtYjI2MC02OGU1NTA4OTFiMTAiLCJwdmQiOiJtcCIsInBydCI6IjIzMDYiLCJhdHRyaWJ1dGVzIjp7IndhbGxldF9pZCI6Ijc2YWYwMjU5MmMzZGRmZDFkNGFlOTZmYmQ1NmM4ZGJmOWVmOGZlNTUwMjZlZGJlMjg4MzBiMmE3ZTcxOTRkZTMiLCJzYWdhX3dhbGxldF9hZGRyZXNzIjoiMHgxMDBmM2UwZDBkRDRhQjE3NDJmRWVGMjA3NzcwNEU3MjM0YzVmYmRjIiwiYWNjb3VudF9pZCI6IjM2YzljOTEzLWQwYWQtNGRjYy05NDUzLTEyNGIyZjE0OGU5OSJ9fQ.Sh3wEQxX_oCyV9XEbViyTRWF3a-NoEsZDh-TgIpwe2e3T1jnva2zurjQdHNJJV1jJrhI0ipVGk0fx-m3zhVZLQ'}
    market_response = requests.get('https://api.dmarket.com/account/v1/balance',headers=header)
    try:
        balance = json.loads(market_response.text)
    except:
        return None
    return balance


def get_invetory_items():
    header = {'authorization': 'eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiIyMTJlMDEzMC03ZjQ4LTQwNGMtODE5NC1jMWViMTBmZDZlM2YiLCJleHAiOjE2ODg0MDcyNTIsImlhdCI6MTY4NTgxNTI1Miwic2lkIjoiMDk4ODkwZjctNjI1OC00ZTcxLWJkY2ItZTQ4Y2Y4MmE1ZGZhIiwidHlwIjoiYWNjZXNzIiwiaWQiOiIxNjViMWE3Yy1kZDZmLTQ0YzYtYjI2MC02OGU1NTA4OTFiMTAiLCJwdmQiOiJtcCIsInBydCI6IjIzMDYiLCJhdHRyaWJ1dGVzIjp7IndhbGxldF9pZCI6Ijc2YWYwMjU5MmMzZGRmZDFkNGFlOTZmYmQ1NmM4ZGJmOWVmOGZlNTUwMjZlZGJlMjg4MzBiMmE3ZTcxOTRkZTMiLCJzYWdhX3dhbGxldF9hZGRyZXNzIjoiMHgxMDBmM2UwZDBkRDRhQjE3NDJmRWVGMjA3NzcwNEU3MjM0YzVmYmRjIiwiYWNjb3VudF9pZCI6IjM2YzljOTEzLWQwYWQtNGRjYy05NDUzLTEyNGIyZjE0OGU5OSJ9fQ.Sh3wEQxX_oCyV9XEbViyTRWF3a-NoEsZDh-TgIpwe2e3T1jnva2zurjQdHNJJV1jJrhI0ipVGk0fx-m3zhVZLQ'}
    market_response = requests.get('https://api.dmarket.com/exchange/v1/user/items?side=user&orderBy=updated&orderDir=desc&treeFilters=&gameId=a8db&limit=100&currency=USD',headers=header)
    
    inventory = json.loads(market_response.text)['objects']

    return inventory

def get_available_inventory(items):

    return_items_list = []
    for item in items :
        if item['inMarket'] == True:
            item_info = {'ItemID': item['itemId'],
                        'ItemName': item['title'],
                        'InstantPrice': item['instantPrice']['USD'],
                        'suggested_price': item['price']['USD']}
            
            return_items_list.append(item_info) 

    return return_items_list



        


def get_market_value():
    header = {'authorization': 'eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiIyMTJlMDEzMC03ZjQ4LTQwNGMtODE5NC1jMWViMTBmZDZlM2YiLCJleHAiOjE2ODg0MDcyNTIsImlhdCI6MTY4NTgxNTI1Miwic2lkIjoiMDk4ODkwZjctNjI1OC00ZTcxLWJkY2ItZTQ4Y2Y4MmE1ZGZhIiwidHlwIjoiYWNjZXNzIiwiaWQiOiIxNjViMWE3Yy1kZDZmLTQ0YzYtYjI2MC02OGU1NTA4OTFiMTAiLCJwdmQiOiJtcCIsInBydCI6IjIzMDYiLCJhdHRyaWJ1dGVzIjp7IndhbGxldF9pZCI6Ijc2YWYwMjU5MmMzZGRmZDFkNGFlOTZmYmQ1NmM4ZGJmOWVmOGZlNTUwMjZlZGJlMjg4MzBiMmE3ZTcxOTRkZTMiLCJzYWdhX3dhbGxldF9hZGRyZXNzIjoiMHgxMDBmM2UwZDBkRDRhQjE3NDJmRWVGMjA3NzcwNEU3MjM0YzVmYmRjIiwiYWNjb3VudF9pZCI6IjM2YzljOTEzLWQwYWQtNGRjYy05NDUzLTEyNGIyZjE0OGU5OSJ9fQ.Sh3wEQxX_oCyV9XEbViyTRWF3a-NoEsZDh-TgIpwe2e3T1jnva2zurjQdHNJJV1jJrhI0ipVGk0fx-m3zhVZLQ'}
    market_response = requests.get('https://api.dmarket.com/exchange/v1/user/offers?side=user&orderBy=updated&orderDir=desc&title=&priceFrom=0&priceTo=0&treeFilters=&gameId=a8db&cursor=&limit=100&currency=USD&platform=browser',headers=header)

    market_sale = json.loads(market_response.text)['objects']

    item_prices = 0
    
    for item in market_sale:
        item_prices += int(item['price']['USD'])

    return item_prices 

def get_selling_items():
    header = {'authorization': 'eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiIyMTJlMDEzMC03ZjQ4LTQwNGMtODE5NC1jMWViMTBmZDZlM2YiLCJleHAiOjE2ODg0MDcyNTIsImlhdCI6MTY4NTgxNTI1Miwic2lkIjoiMDk4ODkwZjctNjI1OC00ZTcxLWJkY2ItZTQ4Y2Y4MmE1ZGZhIiwidHlwIjoiYWNjZXNzIiwiaWQiOiIxNjViMWE3Yy1kZDZmLTQ0YzYtYjI2MC02OGU1NTA4OTFiMTAiLCJwdmQiOiJtcCIsInBydCI6IjIzMDYiLCJhdHRyaWJ1dGVzIjp7IndhbGxldF9pZCI6Ijc2YWYwMjU5MmMzZGRmZDFkNGFlOTZmYmQ1NmM4ZGJmOWVmOGZlNTUwMjZlZGJlMjg4MzBiMmE3ZTcxOTRkZTMiLCJzYWdhX3dhbGxldF9hZGRyZXNzIjoiMHgxMDBmM2UwZDBkRDRhQjE3NDJmRWVGMjA3NzcwNEU3MjM0YzVmYmRjIiwiYWNjb3VudF9pZCI6IjM2YzljOTEzLWQwYWQtNGRjYy05NDUzLTEyNGIyZjE0OGU5OSJ9fQ.Sh3wEQxX_oCyV9XEbViyTRWF3a-NoEsZDh-TgIpwe2e3T1jnva2zurjQdHNJJV1jJrhI0ipVGk0fx-m3zhVZLQ'}
    market_response = requests.get('https://api.dmarket.com/exchange/v1/user/offers?side=user&orderBy=updated&orderDir=desc&title=&priceFrom=0&priceTo=0&treeFilters=&gameId=a8db&cursor=&limit=100&currency=USD&platform=browser',headers=header)
    
    selling_items = json.loads(market_response.text)['objects']
    return selling_items
    
    

def put_on_sale(item_id, price):
    header = {'authorization': 'eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiIyMTJlMDEzMC03ZjQ4LTQwNGMtODE5NC1jMWViMTBmZDZlM2YiLCJleHAiOjE2ODg0MDcyNTIsImlhdCI6MTY4NTgxNTI1Miwic2lkIjoiMDk4ODkwZjctNjI1OC00ZTcxLWJkY2ItZTQ4Y2Y4MmE1ZGZhIiwidHlwIjoiYWNjZXNzIiwiaWQiOiIxNjViMWE3Yy1kZDZmLTQ0YzYtYjI2MC02OGU1NTA4OTFiMTAiLCJwdmQiOiJtcCIsInBydCI6IjIzMDYiLCJhdHRyaWJ1dGVzIjp7IndhbGxldF9pZCI6Ijc2YWYwMjU5MmMzZGRmZDFkNGFlOTZmYmQ1NmM4ZGJmOWVmOGZlNTUwMjZlZGJlMjg4MzBiMmE3ZTcxOTRkZTMiLCJzYWdhX3dhbGxldF9hZGRyZXNzIjoiMHgxMDBmM2UwZDBkRDRhQjE3NDJmRWVGMjA3NzcwNEU3MjM0YzVmYmRjIiwiYWNjb3VudF9pZCI6IjM2YzljOTEzLWQwYWQtNGRjYy05NDUzLTEyNGIyZjE0OGU5OSJ9fQ.Sh3wEQxX_oCyV9XEbViyTRWF3a-NoEsZDh-TgIpwe2e3T1jnva2zurjQdHNJJV1jJrhI0ipVGk0fx-m3zhVZLQ'}
    data = {
        "Offers": [
            {
            "AssetID": item_id,
            "Price": {
                "Currency": "USD",
                "Amount": price
            }
            }
        ]
        }
    url = 'https://api.dmarket.com/marketplace-api/v1/user-offers/create'
    response = requests.post(url, headers=header, json = data)

    return response.json()

def remove_item_from_sale(item_id, offer_id , price):
    header = {'authorization': 'eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiIyMTJlMDEzMC03ZjQ4LTQwNGMtODE5NC1jMWViMTBmZDZlM2YiLCJleHAiOjE2ODg0MDcyNTIsImlhdCI6MTY4NTgxNTI1Miwic2lkIjoiMDk4ODkwZjctNjI1OC00ZTcxLWJkY2ItZTQ4Y2Y4MmE1ZGZhIiwidHlwIjoiYWNjZXNzIiwiaWQiOiIxNjViMWE3Yy1kZDZmLTQ0YzYtYjI2MC02OGU1NTA4OTFiMTAiLCJwdmQiOiJtcCIsInBydCI6IjIzMDYiLCJhdHRyaWJ1dGVzIjp7IndhbGxldF9pZCI6Ijc2YWYwMjU5MmMzZGRmZDFkNGFlOTZmYmQ1NmM4ZGJmOWVmOGZlNTUwMjZlZGJlMjg4MzBiMmE3ZTcxOTRkZTMiLCJzYWdhX3dhbGxldF9hZGRyZXNzIjoiMHgxMDBmM2UwZDBkRDRhQjE3NDJmRWVGMjA3NzcwNEU3MjM0YzVmYmRjIiwiYWNjb3VudF9pZCI6IjM2YzljOTEzLWQwYWQtNGRjYy05NDUzLTEyNGIyZjE0OGU5OSJ9fQ.Sh3wEQxX_oCyV9XEbViyTRWF3a-NoEsZDh-TgIpwe2e3T1jnva2zurjQdHNJJV1jJrhI0ipVGk0fx-m3zhVZLQ'}
    data = {
        "force": True,
        "objects": [
            {
            "itemId": item_id,
            "offerId": offer_id,
            "price": {
                "amount": price,
                "currency": "USD"
            }
            }
        ]
        }
        
    url = 'https://api.dmarket.com/exchange/v1/offers'
    response = requests.delete(url, headers=header, json = data)
    return response.json()

def update_sale_price(item_id, offer_id , price):
    header = {'authorization': 'eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiIyMTJlMDEzMC03ZjQ4LTQwNGMtODE5NC1jMWViMTBmZDZlM2YiLCJleHAiOjE2ODg0MDcyNTIsImlhdCI6MTY4NTgxNTI1Miwic2lkIjoiMDk4ODkwZjctNjI1OC00ZTcxLWJkY2ItZTQ4Y2Y4MmE1ZGZhIiwidHlwIjoiYWNjZXNzIiwiaWQiOiIxNjViMWE3Yy1kZDZmLTQ0YzYtYjI2MC02OGU1NTA4OTFiMTAiLCJwdmQiOiJtcCIsInBydCI6IjIzMDYiLCJhdHRyaWJ1dGVzIjp7IndhbGxldF9pZCI6Ijc2YWYwMjU5MmMzZGRmZDFkNGFlOTZmYmQ1NmM4ZGJmOWVmOGZlNTUwMjZlZGJlMjg4MzBiMmE3ZTcxOTRkZTMiLCJzYWdhX3dhbGxldF9hZGRyZXNzIjoiMHgxMDBmM2UwZDBkRDRhQjE3NDJmRWVGMjA3NzcwNEU3MjM0YzVmYmRjIiwiYWNjb3VudF9pZCI6IjM2YzljOTEzLWQwYWQtNGRjYy05NDUzLTEyNGIyZjE0OGU5OSJ9fQ.Sh3wEQxX_oCyV9XEbViyTRWF3a-NoEsZDh-TgIpwe2e3T1jnva2zurjQdHNJJV1jJrhI0ipVGk0fx-m3zhVZLQ'}
    data ={
        "Offers": [
            {
            "OfferID": offer_id,
            "AssetID": item_id,
            "Price": {
                "Currency": "USD",
                "Amount": price
            }
            }
        ]
        }
        
    url = 'https://api.dmarket.com/marketplace-api/v1/user-offers/edit'
    response = requests.post(url, headers=header, json = data)

    return response.json()



def place_target(item_name,order_amount, order_price, ):
    header = {'authorization': 'eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiIyMTJlMDEzMC03ZjQ4LTQwNGMtODE5NC1jMWViMTBmZDZlM2YiLCJleHAiOjE2ODg0MDcyNTIsImlhdCI6MTY4NTgxNTI1Miwic2lkIjoiMDk4ODkwZjctNjI1OC00ZTcxLWJkY2ItZTQ4Y2Y4MmE1ZGZhIiwidHlwIjoiYWNjZXNzIiwiaWQiOiIxNjViMWE3Yy1kZDZmLTQ0YzYtYjI2MC02OGU1NTA4OTFiMTAiLCJwdmQiOiJtcCIsInBydCI6IjIzMDYiLCJhdHRyaWJ1dGVzIjp7IndhbGxldF9pZCI6Ijc2YWYwMjU5MmMzZGRmZDFkNGFlOTZmYmQ1NmM4ZGJmOWVmOGZlNTUwMjZlZGJlMjg4MzBiMmE3ZTcxOTRkZTMiLCJzYWdhX3dhbGxldF9hZGRyZXNzIjoiMHgxMDBmM2UwZDBkRDRhQjE3NDJmRWVGMjA3NzcwNEU3MjM0YzVmYmRjIiwiYWNjb3VudF9pZCI6IjM2YzljOTEzLWQwYWQtNGRjYy05NDUzLTEyNGIyZjE0OGU5OSJ9fQ.Sh3wEQxX_oCyV9XEbViyTRWF3a-NoEsZDh-TgIpwe2e3T1jnva2zurjQdHNJJV1jJrhI0ipVGk0fx-m3zhVZLQ'}
    data = {
        "GameID": "a8db",
        "Targets": [
            {
            "Amount": order_amount,
            "Price": {
                "Currency": "USD",
                "Amount": order_price
            },
            "Title": item_name
            }
        ]
        }
    url = 'https://api.dmarket.com/marketplace-api/v1/user-targets/create'
    response = requests.post(url, headers=header, json = data)

    return response.json()

def remove_target(target_id):
    header = {'authorization': 'eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiIyMTJlMDEzMC03ZjQ4LTQwNGMtODE5NC1jMWViMTBmZDZlM2YiLCJleHAiOjE2ODg0MDcyNTIsImlhdCI6MTY4NTgxNTI1Miwic2lkIjoiMDk4ODkwZjctNjI1OC00ZTcxLWJkY2ItZTQ4Y2Y4MmE1ZGZhIiwidHlwIjoiYWNjZXNzIiwiaWQiOiIxNjViMWE3Yy1kZDZmLTQ0YzYtYjI2MC02OGU1NTA4OTFiMTAiLCJwdmQiOiJtcCIsInBydCI6IjIzMDYiLCJhdHRyaWJ1dGVzIjp7IndhbGxldF9pZCI6Ijc2YWYwMjU5MmMzZGRmZDFkNGFlOTZmYmQ1NmM4ZGJmOWVmOGZlNTUwMjZlZGJlMjg4MzBiMmE3ZTcxOTRkZTMiLCJzYWdhX3dhbGxldF9hZGRyZXNzIjoiMHgxMDBmM2UwZDBkRDRhQjE3NDJmRWVGMjA3NzcwNEU3MjM0YzVmYmRjIiwiYWNjb3VudF9pZCI6IjM2YzljOTEzLWQwYWQtNGRjYy05NDUzLTEyNGIyZjE0OGU5OSJ9fQ.Sh3wEQxX_oCyV9XEbViyTRWF3a-NoEsZDh-TgIpwe2e3T1jnva2zurjQdHNJJV1jJrhI0ipVGk0fx-m3zhVZLQ'}
    data = {
        "Targets": [
            {
            "TargetID": target_id
            }
        ]
        }
    url = 'https://api.dmarket.com/marketplace-api/v1/user-targets/delete'
    response = requests.post(url, headers=header, json = data)

    return response.json()

def construct_dict(items_list):
    dictionary = {}

    for item in items_list:
        target_price = float(item['InstantPrice']) /100
        item_id = item['ItemID']

        if dictionary.get(item['ItemName'], False):

            if dictionary[item['ItemName']]['highest_target'] < target_price :
                dictionary[item['ItemName']]['highest_target'] = target_price
            dictionary[item['ItemName']]['item_ids'].append(item_id)
            

        else :
            schema = {'highest_target': target_price,
                        'item_ids' : [item_id]}
            

            dictionary[item['ItemName']] = schema
    return dictionary


def get_item_id(item):
    item_id = item['itemId']
    return item_id

def get_offer_id(item):
    offer_id  = item['extra']['offerId']
    return offer_id

def get_item_name(item):
    item_name = item['title']
    return item_name



def get_closed_offers():
    header = {'authorization': 'eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiIyMTJlMDEzMC03ZjQ4LTQwNGMtODE5NC1jMWViMTBmZDZlM2YiLCJleHAiOjE2ODg0MDcyNTIsImlhdCI6MTY4NTgxNTI1Miwic2lkIjoiMDk4ODkwZjctNjI1OC00ZTcxLWJkY2ItZTQ4Y2Y4MmE1ZGZhIiwidHlwIjoiYWNjZXNzIiwiaWQiOiIxNjViMWE3Yy1kZDZmLTQ0YzYtYjI2MC02OGU1NTA4OTFiMTAiLCJwdmQiOiJtcCIsInBydCI6IjIzMDYiLCJhdHRyaWJ1dGVzIjp7IndhbGxldF9pZCI6Ijc2YWYwMjU5MmMzZGRmZDFkNGFlOTZmYmQ1NmM4ZGJmOWVmOGZlNTUwMjZlZGJlMjg4MzBiMmE3ZTcxOTRkZTMiLCJzYWdhX3dhbGxldF9hZGRyZXNzIjoiMHgxMDBmM2UwZDBkRDRhQjE3NDJmRWVGMjA3NzcwNEU3MjM0YzVmYmRjIiwiYWNjb3VudF9pZCI6IjM2YzljOTEzLWQwYWQtNGRjYy05NDUzLTEyNGIyZjE0OGU5OSJ9fQ.Sh3wEQxX_oCyV9XEbViyTRWF3a-NoEsZDh-TgIpwe2e3T1jnva2zurjQdHNJJV1jJrhI0ipVGk0fx-m3zhVZLQ'}
    market_response = requests.get('https://api.dmarket.com/marketplace-api/v1/user-offers/closed',headers=header)
   
    
    return market_response.json()['Trades']


def balance_evaluation(item_price, item_quanity):
    balance_cents = int(get_balance())
    balance  = balance_cents / 100

    if (item_price * item_quanity) < balance :
        return True 
    else :
        return False 
    
def get_sales_history(item_name):
    item_encoded = encode_item(item_name)
    header = {'authorization': 'eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiIyMTJlMDEzMC03ZjQ4LTQwNGMtODE5NC1jMWViMTBmZDZlM2YiLCJleHAiOjE2ODg0MDcyNTIsImlhdCI6MTY4NTgxNTI1Miwic2lkIjoiMDk4ODkwZjctNjI1OC00ZTcxLWJkY2ItZTQ4Y2Y4MmE1ZGZhIiwidHlwIjoiYWNjZXNzIiwiaWQiOiIxNjViMWE3Yy1kZDZmLTQ0YzYtYjI2MC02OGU1NTA4OTFiMTAiLCJwdmQiOiJtcCIsInBydCI6IjIzMDYiLCJhdHRyaWJ1dGVzIjp7IndhbGxldF9pZCI6Ijc2YWYwMjU5MmMzZGRmZDFkNGFlOTZmYmQ1NmM4ZGJmOWVmOGZlNTUwMjZlZGJlMjg4MzBiMmE3ZTcxOTRkZTMiLCJzYWdhX3dhbGxldF9hZGRyZXNzIjoiMHgxMDBmM2UwZDBkRDRhQjE3NDJmRWVGMjA3NzcwNEU3MjM0YzVmYmRjIiwiYWNjb3VudF9pZCI6IjM2YzljOTEzLWQwYWQtNGRjYy05NDUzLTEyNGIyZjE0OGU5OSJ9fQ.Sh3wEQxX_oCyV9XEbViyTRWF3a-NoEsZDh-TgIpwe2e3T1jnva2zurjQdHNJJV1jJrhI0ipVGk0fx-m3zhVZLQ'}
    market_response = requests.get(f'https://api.dmarket.com/marketplace-api/v1/sales-history?Title={item_encoded}&GameID=a8db&Period=7D&Currency=USD',headers=header)
    try:
        hist = json.loads(market_response.text)
      
        return hist['SalesHistory']
    
    except:
        return None



#print('===================================================')
#print(put_on_sale('b7ecd156-8eee-5427-9d5d-67671aa426cd',0.87))
#{'Result': [{'CreateOffer': {'AssetID': 'b7ecd156-8eee-5427-9d5d-67671aa426cd', 'Price': {'Currency': 'USD', 'Amount': 0.87}}, 'OfferID': '98dec468-d245-481d-b4c5-70749bbffd6c', 'Successful': True, 'Error': None}]}
#print(remove_target('6ab1c715-894c-41fe-8d7b-a097ad29d945'))
#place_target()
#invetory = len(get_invetory_items())
#print(invetory)
#print(get_closed_offers()[:5])
#avb_inv = get_available_inventory(invetory)
#invetory_dictionary = construct_dict(avb_inv)

#print(remove_item_from_sale('e48d211f-9282-59e9-a254-afd54deb79be','ba8b62ef-3df6-4b3a-aa94-4e5a94b7fec6','41' ))
#(put_on_sale('e48d211f-9282-59e9-a254-afd54deb79be',0.41))

#print(update_sale_price('f708cbfc-b0a5-5050-bdfb-bd2fa3b98155','475121ba-7cce-44a7-b9f7-fa44dc91c001', 1.1 ))



