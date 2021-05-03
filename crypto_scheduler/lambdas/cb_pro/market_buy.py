# API Docs: https://docs.pro.coinbase.com/#orders

import cbpro
from constants import secret_key, public_key, passphrase
import json

auth_client = cbpro.AuthenticatedClient(public_key, secret_key, passphrase)

def market_buy():
    currency = 'LINK-USD'
    funds = '10.00'

    print(f'Attempting market order for {currency} with {funds} USD.')

    market_order_response = auth_client.place_market_order(
        product_id=currency, 
        side='buy', 
        funds=funds
    )

    print("\nInitial market buy order response:\n\n")

    print(market_order_response)

    orderId = market_order_response['id']

    while(auth_client.get_order(orderId)['status'] != 'done'):
        pass

    completed_market_order = auth_client.get_order(orderId)

    print("\nCompleted market buy order response:\n\n")
    print(completed_market_order)

    filled_size = completed_market_order['filled_size']
    
    buy_order = f'Purchased: {filled_size} {currency}' 
    print(f'\n{buy_order}')
    return {
        'statusCode': 200,
        'body': json.dumps(buy_order)
    }
                      
def lambda_handler(event, context):
    return market_buy()
