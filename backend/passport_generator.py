from jinja2 import Environment, FileSystemLoader
import json
import os
import robonomicsinterface

with open('config.json') as config_file:
    config = json.load(config_file)


def generate_passport(name: str, esp_addr: str, video_cid: str, graph_cid: str):
    file_loader = FileSystemLoader('.')
    env = Environment(loader=file_loader)

    # Load the template file
    template = env.get_template(config["template_name"])
    data = {
        "name": name,
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
    generate_passport("123")