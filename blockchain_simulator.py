import os
from web3 import Web3
from eth_account.messages import encode_defunct
import json
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Connect to local Hardhat node
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

# Load ArtistPopupNFT contract ABI and address
contract_path = Path("artifacts/contracts/ArtistPopupNFT.sol/ArtistPopupNFT.json")
try:
    with open(contract_path, "r") as file:
        contract_json = json.load(file)
        contract_abi = contract_json["abi"]
except FileNotFoundError:
    logger.error(f"Contract file not found: {contract_path}")
    raise

# Use the deployed contract address
contract_address = '0x5FbDB2315678afecb367f032d93F642f64180aa3'

# Get deployed contract instance
try:
    contract = w3.eth.contract(address=contract_address, abi=contract_abi)
except Exception as e:
    logger.error(f"Failed to get contract instance: {str(e)}")
    raise

def mint_token(user_id, artwork_title, artist, description):
    try:
        tx_hash = contract.functions.mintNFT(
            w3.eth.accounts[user_id],
            f"ipfs://{artwork_title}",
            artwork_title,
            artist,
            description
        ).transact({'from': w3.eth.accounts[0]})
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        logger.info(f"Token minted for user {user_id}, artwork: {artwork_title}")
        return tx_receipt['transactionHash'].hex()
    except Exception as e:
        logger.error(f"Error minting token: {str(e)}")
        raise

def transfer_token(token_id, from_user_id, to_user_id):
    try:
        tx_hash = contract.functions.transferFrom(
            w3.eth.accounts[from_user_id],
            w3.eth.accounts[to_user_id],
            token_id
        ).transact({'from': w3.eth.accounts[from_user_id]})
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        logger.info(f"Token {token_id} transferred from user {from_user_id} to user {to_user_id}")
        return tx_receipt['status'] == 1
    except Exception as e:
        logger.error(f"Error transferring token: {str(e)}")
        return False

def get_token_owner(token_id):
    try:
        owner = contract.functions.ownerOf(token_id).call()
        logger.info(f"Owner of token {token_id}: {owner}")
        return owner
    except Exception as e:
        logger.error(f"Error getting token owner: {str(e)}")
        raise

def get_artwork_details(token_id):
    try:
        title, artist, description = contract.functions.getArtwork(token_id).call()
        logger.info(f"Artwork details for token {token_id}: Title: {title}, Artist: {artist}")
        return title, artist, description
    except Exception as e:
        logger.error(f"Error getting artwork details: {str(e)}")
        raise

def sign_message(message):
    private_key = w3.eth.account.create().privateKey
    signed_message = w3.eth.account.sign_message(encode_defunct(text=message), private_key=private_key)
    return signed_message.signature.hex()

def verify_signature(message, signature, address):
    signed_address = w3.eth.account.recover_message(encode_defunct(text=message), signature=signature)
    return signed_address.lower() == address.lower()

# Hardhat node specific functions
def get_network_id():
    return w3.net.version

def get_latest_block():
    return w3.eth.get_block('latest')

# Example usage and connection test
try:
    network_id = get_network_id()
    latest_block = get_latest_block()
    logger.info(f"Connected to network: {network_id}")
    logger.info(f"Latest block: {latest_block['number']}")
    logger.info(f"ArtistPopupNFT contract address: {contract_address}")
except Exception as e:
    logger.error(f"Failed to connect to Hardhat node: {str(e)}")
    raise
