import os
from web3 import Web3
import json
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BlockchainSimulator:
    def __init__(self):
        self.w3 = None
        self.contract = None
        self.blockchain_available = False
        self.connect_to_blockchain()

    def connect_to_blockchain(self):
        try:
            skale_endpoint = os.environ.get('SKALE_ENDPOINT')
            if not skale_endpoint:
                raise ValueError("SKALE_ENDPOINT environment variable is not set")

            self.w3 = Web3(Web3.HTTPProvider(skale_endpoint))
            if not self.w3.is_connected():
                raise ConnectionError("Failed to connect to the SKALE node")

            contract_path = Path("artifacts/contracts/ArtistPopupNFT.sol/ArtistPopupNFT.json")
            if not contract_path.exists():
                raise FileNotFoundError(f"Contract file not found: {contract_path}")

            with open(contract_path, "r") as file:
                contract_json = json.load(file)
                contract_abi = contract_json["abi"]

            contract_address_file = Path("contract-address.txt")
            if not contract_address_file.exists():
                raise FileNotFoundError("contract-address.txt not found. Please deploy the contract first.")

            with open(contract_address_file, "r") as file:
                contract_address = file.read().strip()

            self.contract = self.w3.eth.contract(address=Web3.to_checksum_address(contract_address), abi=contract_abi)
            self.blockchain_available = True
            
            # Log the contract address and SKALE Explorer link
            skale_explorer_url = "https://giant-half-dual-testnet.explorer.testnet.skalenodes.com"
            logger.info(f"Successfully connected to the SKALE node")
            logger.info(f"ArtistPopupNFT contract address: {contract_address}")
            logger.info(f"View the contract on SKALE Explorer: {skale_explorer_url}/address/{contract_address}")
        except Exception as e:
            logger.error(f"Failed to connect to the SKALE node: {str(e)}")
            self.blockchain_available = False

    def get_contract_abi(self):
        return self.contract.abi if self.blockchain_available else None

    def get_contract_address(self):
        return self.contract.address if self.blockchain_available else None

    def get_network_id(self):
        return self.w3.eth.chain_id if self.blockchain_available else None

    def get_latest_block(self):
        if not self.blockchain_available:
            return None
        try:
            return self.w3.eth.get_block('latest')
        except Exception as e:
            logger.error(f"Error getting latest block: {str(e)}")
            return None

# Initialize the BlockchainSimulator
blockchain_simulator = BlockchainSimulator()

# Example usage and connection test
try:
    network_id = blockchain_simulator.get_network_id()
    latest_block = blockchain_simulator.get_latest_block()
    if network_id:
        logger.info(f"Connected to network: {network_id}")
    if latest_block:
        logger.info(f"Latest block: {latest_block['number']}")
    else:
        logger.warning("Failed to retrieve latest block")
except Exception as e:
    logger.error(f"Failed to connect to SKALE node: {str(e)}")
