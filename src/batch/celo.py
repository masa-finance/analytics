from batch import get_mint_events

network = {
    "url": "https://api.celoscan.io/api",
    "contract_address_env": "CELOSCAN_CONTRACT_ADDRESS",
    "api_key_env": "CELOSCAN_API_KEY",
    "start_block": 17756683
}

get_mint_events(network, "celo")
