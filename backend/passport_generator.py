from jinja2 import Environment, FileSystemLoader
import json
import os
import robonomicsinterface

import mongodb_util
import ipfs_utils
import qr_printer

with open('config.json') as config_file:
    config = json.load(config_file)


def generate_passport(name: str, description: str, esp_addr: str, video_cid: str, graph_cid: str):
    file_loader = FileSystemLoader('.')
    env = Environment(loader=file_loader)

    # Load the template file
    template = env.get_template(config["template_name"])
    data = {
        "name": name,
        "description": description,
        "source_address": robonomicsinterface.Account(seed=config["seed"]).get_address(),
        "esp_address": esp_addr,
        "video_cid": video_cid,
        "graph_cid": graph_cid
    }

    rendered_html = template.render(data)

    output_file_path = config["passport_name_template"].replace("NAME", name)
    with open(output_file_path, 'w') as output_file:
        output_file.write(rendered_html)

    print(f"Rendered HTML saved to {output_file_path}")
    return os.path.abspath(output_file_path)

if __name__ == '__main__':
    video = ipfs_utils.pin_file(config["video_name"])
    print(f'video: {video}')
    graph = ipfs_utils.pin_file(config["graph"])
    print(f'graph: {graph}')

    mongo = mongodb_util.MongoDBUtil(config['mongo_connection_uri'], config['database_name'], "esp_data")
    esp_data = mongo.get_esp_data()
    esp_addr = esp_data[0]
    mongo = mongodb_util.MongoDBUtil(config['mongo_connection_uri'], config['database_name'], "pictures")
    item = mongo.get_latest_item()

    passport_path = generate_passport(item["name"], item["description"], esp_addr, video, graph)
    passport_cid = ipfs_utils.pin_file(passport_path)
    print(f'passport: {passport_cid}')
    passport_link = f"{config['ipfs_prefix']}{passport_cid}"


    robonomics = robonomicsinterface.Account(seed=config["seed"], remote_ws=config["remote_ws"])
    datalog = robonomicsinterface.Datalog(robonomics)
    transaction = f"{config['explorer_prefix']}{datalog.record(passport_link)}"

    qr_printer.generate_qrs([passport_link, transaction])
    qr_printer.print_qrs()
    qr_printer.print_qrs()