from batch import get_mint_events

network = {
    "url": "https://api.polygonscan.com/api",
    "contract_address_env": "POLYGONSCAN_CONTRACT_ADDRESS",
    "api_key_env": "POLYGONSCAN_API_KEY",
    "start_block": 39314880
}

get_mint_events(network, "polygon")
