import requests
import json
import datetime
from dotenv import load_dotenv
import os
import time
import csv

load_dotenv()

def add_address_to_csv(address):
    with open('addresses.csv', mode='a') as file:
        writer = csv.writer(file)
        writer.writerow([address])

def get_mint_events(network):
    base_url = network['url']
    contract_address = os.getenv(network['contract_address_env'])
    api_key = os.getenv(network['api_key_env'])
    topic0 = "0x7650948236619e679e44bf502d527ec950d1d58336e6babf229f483c57d04672"

    block_step = 5000
    from_block = network['start_block']  
    to_block = from_block + block_step
    max_block = 45000000  
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
                for log in logs:
                    to_address = '0x' + log['data'][90:130]
                    add_address_to_csv(to_address)
            else:
                print(f"Error: 'result' not found or not a list in response from {base_url}. Full response: {response_json}")
        else:
            print(f"Error: Received invalid response from {base_url}")

        from_block = to_block + 1
        to_block = min(to_block + block_step, max_block)
        time.sleep(10)

    print(f"Number of mint events for {network}: {total_logs}")
    return total_logs
