import requests
import json
import datetime
from dotenv import load_dotenv
import os
import time
from concurrent.futures import ThreadPoolExecutor

load_dotenv()

def check_and_create_user(address, base_url):
    users_url = f"{base_url}/users/{address}"
    user_exists = requests.get(users_url)
    if user_exists.status_code == 404:  # Assuming a 404 status code means the user does not exist
        user_creation_response = requests.post(
            f"{base_url}/users",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"address": address}),
        )
        if user_creation_response.status_code != 201:  # Adjusted to check for 201 status code
            print(
                f"Failed to create user {address}. Status code: {user_creation_response.status_code}. Response: {user_creation_response.text}"
            )
        else:
            print(f"Successfully created user {address}")
    elif user_exists.status_code != 200:
        print(
            f"Error checking if user {address} exists. Status code: {user_exists.status_code}. Response: {user_exists.text}"
        )

def add_event_to_user(address, base_url, timestamp):
    event_creation_response = requests.post(
        f"{base_url}/events",
        headers={"Content-Type": "application/json"},
        data=json.dumps(
            {
                "type": "Mint: MGX-2FA",
                "user_address": address,
                "event_data": {
                    "description": "Mint MGX-2FA", # we should add the network in here from the network var
                    "date": datetime.datetime.utcfromtimestamp(timestamp).isoformat()
                },
            }
        ),
    )
    if event_creation_response.status_code != 201:  # Adjusted to check for 201 status code
        print(
            f"Failed to add event to user {address}. Status code: {event_creation_response.status_code}. Response: {event_creation_response.text}"
        )
    else:
        print(f"Successfully added event to user {address}")

def get_mint_events(network):
    base_url = network['url']
    contract_address = os.getenv(network['contract_address_env'])
    api_key = os.getenv(network['api_key_env'])
    topic0 = "0x7650948236619e679e44bf502d527ec950d1d58336e6babf229f483c57d04672"

    block_step = 5000
    from_block = network['start_block']  # Get the start block from the network dictionary
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
                for log in logs:
                    to_address = '0x' + log['data'][90:130]
                    timestamp = int(log['timeStamp'], 16)  # interpret as Unix timestamp

                    check_and_create_user(to_address, "https://zksbt-cookie-api.onrender.com")
                    add_event_to_user(to_address, "https://zksbt-cookie-api.onrender.com", timestamp)
            else:
                print(f"Error: 'result' not found or not a list in response from {base_url}. Full response: {response_json}")
        else:
            print(f"Error: Received invalid response from {base_url}")

        from_block = to_block + 1
        to_block = min(to_block + block_step, max_block)
        time.sleep(14)

    print(f"Number of mint events for {network}: {total_logs}")
    return total_logs

networks = {
    "etherscan": {
        "url": "https://api.etherscan.io/api",
        "contract_address_env": "ETHERSCAN_CONTRACT_ADDRESS",
        "api_key_env": "ETHERSCAN_API_KEY",
        "start_block": 16633100  # Add a start block for each network
    },
    "bscscan": {
        "url": "https://api.bscscan.com/api",
        "contract_address_env": "BSCSCAN_CONTRACT_ADDRESS",
        "api_key_env": "BSCSCAN_API_KEY",
        "start_block": 25684468
    },
    "polygonscan": {
        "url": "https://api.polygonscan.com/api",
        "contract_address_env": "POLYGONSCAN_CONTRACT_ADDRESS",
        "api_key_env": "POLYGONSCAN_API_KEY",
        "start_block": 39314880
    },
    "celoscan": {
        "url": "https://api.celoscan.io/api",
        "contract_address_env": "CELOSCAN_CONTRACT_ADDRESS",
        "api_key_env": "CELOSCAN_API_KEY",
        "start_block": 17756683
    }
}

with ThreadPoolExecutor() as executor:
    mint_event_futures = {executor.submit(get_mint_events, network): network for network in networks.values()}
    total_mint_events = sum(future.result() for future in mint_event_futures)

print(f"Total number of mint events: {total_mint_events}")