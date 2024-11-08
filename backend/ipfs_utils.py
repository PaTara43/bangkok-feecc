import ipfshttpclient2
import json
from robonomicsinterface import web_3_auth
from pinatapy import PinataPy

with open('config.json') as config_file:
    config = json.load(config_file)

def upload_file(path: str) -> tuple:
    try:
        usr, pwd = web_3_auth(config["seed"])
        client = ipfshttpclient2.connect(addr=config["ipfs_gateway_addr"], auth=(usr, pwd), session=True, timeout=5)
        res = client.add(path)
        return res['Hash'], res['Size']
    except Exception as e:
        print(f"Error uploading to ipfs: {e}. Retrying...")
        return upload_file(path)

def pin_file(file_path):
    api_key = config["api_key"]
    secret_key = config["secret_key"]
    pinata = PinataPy(api_key, secret_key)
    pinata.pin_file_to_ipfs(path_to_file=file_path)
    print("pinned to pinata")