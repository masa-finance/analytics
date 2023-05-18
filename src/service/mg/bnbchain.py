from mg import get_mint_events
import requests
import os

network = {
    "url": "https://api.bscscan.com/api",
    "contract_address_env": "BSCSCAN_CONTRACT_ADDRESS",
    "api_key_env": "BSCSCAN_API_KEY",
}

def fetch_latest_block_number(api_key):
    response = requests.get(
        "https://api.bscscan.com/api",
        params={
            "module": "proxy",
            "action": "eth_blockNumber",
            "apikey": api_key
        }
    )
    latest_block = int(response.json()["result"], 16)
    return max(0, latest_block - 100000)

api_key = os.getenv(network['api_key_env'])
start_block = fetch_latest_block_number(api_key)

network["start_block"] = start_block

get_mint_events(network, "bnbchain")
