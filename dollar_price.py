import requests

def get_dollar_price():
    url = 'https://www.currency.me.uk/remote/ER-CCCS2-AJAX.php?ConvertTo=UAH&ConvertFrom=USD&amount=1'
    value  = requests.get(url)
    return value.json()
