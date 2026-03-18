import os
import json
from web3 import Web3
from solcx import compile_standard, install_solc
import sys

# Load environment variables (you might need python-dotenv installed)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Ensure solc is installed
print("Installing solc compiler...")
install_solc('0.8.0')

# Path to contract
contract_path = os.path.join(os.path.dirname(__file__), 'contracts', 'TokenRegistry.sol')
with open(contract_path, 'r') as file:
    contract_source_code = file.read()

# Compile the contract
print("Compiling contract...")
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"TokenRegistry.sol": {"content": contract_source_code}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.8.0",
)

# Extract ABI and Bytecode
bytecode = compiled_sol["contracts"]["TokenRegistry.sol"]["TokenRegistry"]["evm"]["bytecode"]["object"]
abi = json.loads(compiled_sol["contracts"]["TokenRegistry.sol"]["TokenRegistry"]["metadata"])["output"]["abi"]

# Save ABI to a file so the Django app can access it
abi_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'backend', 'api', 'TokenRegistry.json')
with open(abi_path, 'w') as f:
    json.dump(abi, f, indent=4)
print(f"Saved ABI to {abi_path}")

# Connect to Polygon Mumbai (or Mainnet/Local)
rpc_url = os.getenv("POLYGON_RPC_URL", "https://rpc-amoy.polygon.technology") # Mumbai is deprecated, using Amoy as replacement or local
private_key = os.getenv("WALLET_PRIVATE_KEY")

if not private_key:
    print("Error: WALLET_PRIVATE_KEY is not set in environment variables.")
    print("Please set it before deploying (e.g. export WALLET_PRIVATE_KEY=your_key).")
    sys.exit(1)

w3 = Web3(Web3.HTTPProvider(rpc_url))
print(f"Connected to blockchain: {w3.is_connected()}")

# Setup account
account = w3.eth.account.from_key(private_key)
print(f"Deploying from address: {account.address}")
print(f"Current Balance: {w3.eth.get_balance(account.address)}")

# Deploy contract
TokenRegistry = w3.eth.contract(abi=abi, bytecode=bytecode)
nonce = w3.eth.get_transaction_count(account.address)

print("Building deployment transaction...")
transaction = TokenRegistry.constructor().build_transaction({
    "chainId": w3.eth.chain_id,
    "gasPrice": w3.eth.gas_price,
    "from": account.address,
    "nonce": nonce,
})

print("Signing transaction...")
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

print("Sending transaction...")
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction) # Changed to rawTransaction in modern web3
print(f"Deployment Transaction Hash: {tx_hash.hex()}")

print("Waiting for transaction receipt...")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(f"Contract Deployed at Address: {tx_receipt.contractAddress}")

# Save the address to a file or print it
print(f"\n--- SUCCESS ---")
print(f"Contract Address: {tx_receipt.contractAddress}")
print(f"Add this address to your backend environment variables as SMART_CONTRACT_ADDRESS")
