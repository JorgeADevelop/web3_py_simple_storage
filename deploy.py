import json
import os

from solcx import compile_standard, install_solc
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

install_solc("0.6.12")
compile_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
                }
            }
        }
    },
    solc_version="0.6.12"
)

with open("compiled_code.json", "w") as file:
    json.dump(compile_sol, file)

bytecode = compile_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]
abi = json.loads(compile_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["metadata"])["output"]["abi"]

w3 = Web3(Web3.HTTPProvider(os.getenv("W3_URL", "http://127.0.0.1:7545")))
chain_id = int(os.getenv("CHAIN_ID", 1337))
my_address = os.getenv("WALLET_ADDRESS", "")
private_key = os.getenv("PRIVATE_KEY_SIGN", "")

SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

nonce = w3.eth.get_transaction_count(my_address)

transaction = SimpleStorage.constructor().build_transaction({
    "chainId": chain_id,
    "from": my_address,
    "nonce": nonce
})

signed_transaction = w3.eth.account.sign_transaction(transaction, private_key=private_key)

tx_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

simple_storage = w3.eth.contract(address=tx_receipt.get("contractAddress"), abi=abi)

#Call -> Simulate making a call to the blockchain without sending a transaction
#Transact -> Send a transaction to the blockchain

print(simple_storage.functions.retrive().call())

store_transaction = simple_storage.functions.store(15).build_transaction({
    "chainId": chain_id,
    "from": my_address,
    "nonce": nonce + 1
})

signed_store_tx = w3.eth.account.sign_transaction(store_transaction, private_key=private_key)

send_store_tx = w3.eth.send_raw_transaction(signed_store_tx.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)

print(simple_storage.functions.retrive().call())
