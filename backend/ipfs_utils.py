import ipfshttpclient2
import json
from robonomicsinterface import web_3_auth
from pinatapy import PinataPy

with open('config.json') as config_file:
    config = json.load(config_file)

def upload_file_to_local_node(path: str) -> tuple:
    with ipfshttpclient2.connect() as client:
        res = client.add(path)
    ipfs_hash = res.get("Hash")
    ipfs_size = res.get("Size")
    return ipfs_hash, ipfs_size

def upload_file(path: str) -> tuple:
    try:
        local_hash, local_size = upload_file_to_local_node(path)
        print(f"File {path} was added to local ipfs: {local_hash}")
    except Exception as e:
        print(f"Exception in pinning to local gateway: {e}")
        local_hash, local_size = None, None
    # try:
    #     usr, pwd = web_3_auth(config["seed"])
    #     client = ipfshttpclient2.connect(addr=config["ipfs_gateway_addr"], auth=(usr, pwd), session=True, timeout=5)
    #     res = client.add(path)
    #     custom_hash, custom_size = res.get('Hash'), res.get('Size')
    #     print(f"File {path} was added to multi agent ipfs: {custom_hash}")
    # except Exception as e:
    #     print(f"Error uploading to multi agent ipfs: {e}. Retrying...")
    #     custom_hash, custom_size = None, None
    res_hash = local_hash
    res_size = local_size
    return res_hash, res_size

def pin_file(file_path):
    print(f"Start pin to pinata: {file_path}")
    api_key = config["api_key"]
    secret_key = config["secret_key"]
    pinata = PinataPy(api_key, secret_key)
    res = pinata.pin_file_to_ipfs(path_to_file=file_path, save_absolute_paths=False)
    print(f"pinned to pinata: {res}, pinning to custom")
    try:
        usr, pwd = web_3_auth(config["seed"])
        client = ipfshttpclient2.connect(addr=config["ipfs_gateway_addr"], auth=(usr, pwd), session=True, timeout=5)
        res = client.add(file_path)
        custom_hash, custom_size = res.get('Hash'), res.get('Size')
        print(f"File {file_path} was added to multi agent ipfs: {custom_hash}")
    except Exception as e:
        print(f"Error uploading to multi agent ipfs: {e}. Retrying...")
        custom_hash, custom_size = None, None
    return custom_hash

if __name__ == '__main__':
    print(pin_file(config["video"]))
    print(pin_file(config["graph"]))
