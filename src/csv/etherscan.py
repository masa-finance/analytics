from script_template_csv import get_mint_events

network = {
    "url": "https://api.etherscan.io/api",
    "contract_address_env": "ETHERSCAN_CONTRACT_ADDRESS",
    "api_key_env": "ETHERSCAN_API_KEY",
    "start_block": 16633100  # Add a start block for each network
}

get_mint_events(network)
