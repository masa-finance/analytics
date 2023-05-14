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

def save_last_processed_block(block_number):
    with open('last_processed_block.txt', 'w') as file:
        file.write(str(block_number))

def get_last_processed_block():
    try:
        with open('last_processed_block.txt', 'r') as file:
            return int(file.read().strip())
    except FileNotFoundError:
        return None

def get_mint_events(network):
    base_url = network['url']
    contract_address = os.getenv(network['contract_address_env'])
    api_key = os.getenv(network['api_key_env'])
    topic0 = "0x7650948236619e679e44bf502d527ec950d1d58336e6babf229f483c57d04672"

    block_step = 10000
    from_block = get_last_processed_block() or network['start_block']  
    to_block = from_block + block_step
    max_block = 45000000  
    total_logs = 0

    while from_block <= max_block:
        page = 1
        while True:  # Loop to handle pagination
            response = requests.get(base_url, params={
                "module": "logs",
                "action": "getLogs",
                "fromBlock": str(from_block),
                "toBlock": str(to_block),
                "address": contract_address,
                "topic0": topic0,
                "offset": "1000",
                "page": str(page),
                "apikey": api_key
            })

            print(f"Requested from block {from_block} to block {to_block}, page {page}. Response status: {response.status_code}")

            if response.status_code == 200 and response.text.strip():
                response_json = response.json()
                print(f"Response: {response_json}")
                logs = response_json.get('result')
                if isinstance(logs, list):
                    num_logs = len(logs)
                    total_logs += num_logs
                    if num_logs == 0:  # No more logs, break the pagination loop
                        break
                    for log in logs:
                        to_address = '0x' + log['data'][90:130]
                        add_address_to_csv(to_address)
                else:
                    print(f"Error: 'result' not found or not a list in response from {base_url}. Full response: {response_json}")
                    break  # Break the pagination loop in case of error
            else:
                print(f"Error: Received invalid response from {base_url}")
                break  # Break the pagination loop in case of error

            page += 1  # Increase page number for the next iteration

        save_last_processed_block(to_block)
        from_block = to_block + 1
        to_block = min(to_block + block_step, max_block)
        time.sleep(10)

    print(f"Number of mint events for {network}: {total_logs}")
    return total_logs
