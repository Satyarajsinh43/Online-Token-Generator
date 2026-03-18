import os
import json
import hashlib
from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware
from django.conf import settings

# Attempt to load dotenv if not using a unified settings approach
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

def get_web3_instance():
    rpc_url = os.getenv("POLYGON_RPC_URL", "https://rpc-amoy.polygon.technology")
    w3 = Web3(Web3.HTTPProvider(rpc_url))
    # Inject middleware for PoA chains like Polygon
    w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)
    return w3

def load_contract(w3):
    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")
    if not contract_address:
         return None

    # Load ABI
    abi_path = os.path.join(os.path.dirname(__file__), 'TokenRegistry.json')
    try:
        with open(abi_path, 'r') as f:
            abi = json.load(f)
    except FileNotFoundError:
        print("Contract ABI not found. Please deploy the contract first.")
        return None

    return w3.eth.contract(address=contract_address, abi=abi)

def generate_token_hash(token_number, customer_name, office_id, timestamp_str):
    """
    Generate SHA-256 hash representing the token data.
    """
    data = f"{token_number}{customer_name}{office_id}{timestamp_str}"
    print(f"Hashing Data: {data}")
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def store_token_hash_on_blockchain(token_hash):
    """
    Stores the token hash on the Polygon smart contract and returns the tx hash.
    If it fails, returns None.
    """
    w3 = get_web3_instance()
    if not w3.is_connected():
        print("Failed to connect to Polygon network.")
        return None
        
    contract = load_contract(w3)
    if not contract:
        print("Failed to load smart contract!")
        return None

    private_key = os.getenv("WALLET_PRIVATE_KEY")
    if not private_key:
        print("WALLET_PRIVATE_KEY not found in environment!")
        return None

    account = w3.eth.account.from_key(private_key)
    
    try:
        # Check if already exists to save gas
        exists = contract.functions.verifyToken(token_hash).call()
        if exists:
            print("Token hash already exists on blockchain.")
            return None # Or return a specific message
            
        nonce = w3.eth.get_transaction_count(account.address)
        
        # Build transaction
        tx = contract.functions.storeTokenHash(token_hash).build_transaction({
            'chainId': 80002, # Polygon Amoy testnet. Change if using different network
            'gas': 200000,
            'gasPrice': w3.eth.gas_price,
            'nonce': nonce,
        })
        
        # Sign transaction
        signed_tx = w3.eth.account.sign_transaction(tx, private_key=private_key)
        
        # Send transaction
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        return tx_hash.hex()
        
    except Exception as e:
        print(f"Blockchain Transaction Failed: {e}")
        return None

def verify_token_on_blockchain(token_hash):
    """
    Verifies if a given token hash exists on the smart contract.
    Returns boolean.
    """
    w3 = get_web3_instance()
    if not w3.is_connected():
        return False
        
    contract = load_contract(w3)
    if not contract:
        return False
        
    try:
        exists = contract.functions.verifyToken(token_hash).call()
        return exists
    except Exception as e:
        print(f"Error calling verifyToken: {e}")
        return False
