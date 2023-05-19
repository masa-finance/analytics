from batch import get_mint_events

network = {
    "url": "https://api.bscscan.com/api",
    "contract_address_env": "BSCSCAN_CONTRACT_ADDRESS",
    "api_key_env": "BSCSCAN_API_KEY",
    "start_block": 25684468
}

get_mint_events(network, "bnbchain")
