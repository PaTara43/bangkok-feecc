import ipfshttpclient2
import json
from robonomicsinterface import web_3_auth

with open('config.json') as config_file:
    config = json.load(config_file)

def upload_file(path: str) -> tuple:
    usr, pwd = web_3_auth(config["seed"])
    client = ipfshttpclient2.connect(addr=config["ipfs_gateway_addr"], auth=(usr, pwd), session=True, timeout=5)
    res = client.add(path)
    return res['Hash'], res['Size']