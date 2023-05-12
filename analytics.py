import requests
import json
from dotenv import load_dotenv
import os
import time
from concurrent.futures import ThreadPoolExecutor

load_dotenv()

def get_mint_events(network):
    base_url = network['url']
    contract_address = os.getenv(network['contract_address_env'])
    api_key = os.getenv(network['api_key_env'])
    topic0 = "0x7650948236619e679e44bf502d527ec950d1d58336e6babf229f483c57d04672"

    block_step = 5000
    from_block = 16633100
    to_block = from_block + block_step
    max_block = 45000000  # Set this to the maximum block number you want to search up to
    total_logs = 0

    while from_block <= max_block:
        response = requests.get(base_url, params={
            "module": "logs",
            "action": "getLogs",
            "fromBlock": str(from_block),
            "toBlock": str(to_block),
            "address": contract_address,
            "topic0": topic0,
            "offset": "1000",
            "apikey": api_key
        })

        print(f"Requested from block {from_block} to block {to_block}. Response status: {response.status_code}")

        if response.status_code == 200 and response.text.strip():
            response_json = response.json()
            print(f"Response: {response_json}")
            logs = response_json.get('result')
            if isinstance(logs, list):
                num_logs = len(logs)

                total_logs += num_logs
            else:
                print(f"Error: 'result' not found or not a list in response from {base_url}. Full response: {response_json}")
        else:
            print(f"Error: Received invalid response from {base_url}")

        from_block = to_block + 1
        to_block = min(to_block + block_step, max_block)
        time.sleep(14)

    print(f"Number of mint events for {network}: {total_logs}")
    return total_logs

# Rest of your code...


networks = {
    "etherscan": {
        "url": "https://api.etherscan.io/api",
        "contract_address_env": "ETHERSCAN_CONTRACT_ADDRESS",
        "api_key_env": "ETHERSCAN_API_KEY",
    },
    "bscscan": {
        "url": "https://api.bscscan.com/api",
        "contract_address_env": "BSCSCAN_CONTRACT_ADDRESS",
        "api_key_env": "BSCSCAN_API_KEY",
    },
    "polygonscan": {
        "url": "https://api.polygonscan.com/api",
        "contract_address_env": "POLYGONSCAN_CONTRACT_ADDRESS",
        "api_key_env": "POLYGONSCAN_API_KEY",
    },
    "celoscan": {
        "url": "https://api.celoscan.io/api",
        "contract_address_env": "CELOSCAN_CONTRACT_ADDRESS",
        "api_key_env": "CELOSCAN_API_KEY",
    }
}

with ThreadPoolExecutor() as executor:
    mint_event_futures = {executor.submit(get_mint_events, network): network for network in networks.values()}
    total_mint_events = sum(future.result() for future in mint_event_futures)

print(f"Total number of mint events: {total_mint_events}")
