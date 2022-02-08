
import asyncio
import aiohttp
import traceback
from time import sleep

#chia
from chia.util.config import load_config
from chia.util.default_root import DEFAULT_ROOT_PATH
from chia.rpc.full_node_rpc_client import FullNodeRpcClient
from chia.rpc.wallet_rpc_client import WalletRpcClient
from chia.util.ints import uint16
from chia.util.ints import uint32

from chia.util.bech32m import encode_puzzle_hash, decode_puzzle_hash

async def run_test() -> None:
    try:
        config = load_config(DEFAULT_ROOT_PATH, "config.yaml")
        self_hostname = config["self_hostname"]
        rpc_port = config["wallet"]["rpc_port"]
        #client = await WalletRpcClient.create(self_hostname, uint16(rpc_port), DEFAULT_ROOT_PATH, config)
        client = await WalletRpcClient.create(self_hostname, rpc_port, DEFAULT_ROOT_PATH, config)
        wallet_state = await client.get_sync_status()
        if wallet_state is None:
            print("  There is no wallet_state found yet. Try again shortly")
            return
        else:
            print('Wallet RPC connect success. \nListing Addresses:')

        transaction_record = await client.get_transactions('1')
        
        address_set = set()
        for transaction in transaction_record:
            address = encode_puzzle_hash(transaction.to_puzzle_hash,'xch')
            address_set.add(address)
            
        #not really a useful set of addresses
        for address in address_set:
            print(f'{address}')


    except Exception as e:
        tb = traceback.format_exc()
        print(f"Exception trying to run test: {tb}")
        return
    finally:
        try:
            client.close()
            await client.await_closed()
        except Exception as e:
            tb = traceback.format_exc()
            print(f"Exception trying to close client connection: {tb}")



async def main():
    await run_test()
        


if __name__ == "__main__":
    asyncio.run(main())