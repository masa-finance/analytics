import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

def get_token_information(contract_address, api_key):
    base_url = "https://api.etherscan.io/api"
    
    # Get total supply of tokens
    response = requests.get(base_url, params={
        "module": "stats",
        "action": "tokensupply",
        "contractaddress": contract_address,
        "apikey": api_key
    })
    total_supply = int(response.json().get('result', 0))

    # Get number of token holders
    response = requests.get(base_url, params={
        "module": "account",
        "action": "tokenbalance",
        "contractaddress": contract_address,
        "address": "0x0000000000000000000000000000000000000000",  # Replace with your address
        "tag": "latest",
        "apikey": api_key
    })
    token_balance = int(response.json().get('result', 0))

    return total_supply, token_balance

contract_address = os.getenv("CONTRACT_ADDRESS")
api_key = os.getenv("ETHERSCAN_API_KEY")

total_supply, token_balance = get_token_information(contract_address, api_key)
print(f"Total supply: {total_supply}")
print(f"Token balance: {token_balance}")
