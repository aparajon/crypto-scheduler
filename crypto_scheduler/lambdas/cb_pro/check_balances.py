import cbpro
from constants import secret_key, public_key, passphrase

auth_client = cbpro.AuthenticatedClient(public_key, secret_key, passphrase)

account_currencies_tracking = {'LINK': 0, 'ETH': 0, 'USD': 0} # Add currencies you care about here
accounts = auth_client.get_accounts()

for account in accounts:
    currency = account['currency']
    if currency in account_currencies_tracking:
        account_currencies_tracking[currency] = account['balance']
    
print(account_currencies_tracking)
