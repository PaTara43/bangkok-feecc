import qrcode
import json
from PIL import Image
from brother_ql import BrotherQLRaster, create_label
from brother_ql.conversion import convert
from brother_ql.backends.helpers import send


with open('config.json') as config_file:
    config = json.load(config_file)


def create_qr_code(url, size=200):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img = img.resize((size, size))  # Resize QR code to desired size
    return img


# Function to combine images and QR codes vertically
def generate_qrs(urls):
    # Load images
    image_paths = ['logos/ipfs.jpg', 'logos/robonomics.jpg']
    images = [Image.open(path) for path in image_paths]

    # Create QR codes
    qr_codes = [create_qr_code(url) for url in urls]

    # Resize images to be 25% of QR code size
    qr_size = qr_codes[0].size[0]  # Assuming both QR codes are the same size
    new_image_size = int(qr_size * 0.25)
    resized_images = [img.resize((round(img.width/(img.height/new_image_size)), round(img.height/(img.height/new_image_size)))) for img in images]

    # Calculate total height for the final image
    total_height = sum(qr.size[1] + img.size[1] for qr, img in zip(qr_codes, resized_images)) + 20

    # Create a new blank image with the calculated height
    final_image = Image.new('RGB', (qr_size, total_height), (255, 255, 255))

    # Paste images and QR codes into the final image
    y_offset = 0
    for qr, img in zip(qr_codes, resized_images):
        final_image.paste(qr, (0, y_offset))
        y_offset += qr.size[1]
        final_image.paste(img, (int((qr_size - img.width) / 2), y_offset))  # Center image below QR code
        y_offset += img.size[1]

    final_image.save(config["qr_name"])

def print_qrs():
    printer_identifier = config["printer_usb_addr"]
    printer_model = config["printer_model"]
    label_size = config["paper_width"]

    qlr = BrotherQLRaster(printer_model)
    im = Image.open(config["qr_name"])
    instructions = convert(qlr=qlr, images=[im], label=label_size, cut=True)
    send(instructions, printer_identifier)


if __name__ == '__main__':

    # Data for QR codes and their labels
    urls = ['https://example.com/url1', 'https://example.com/url2']
    generate_qrs(urls)
    # print_qrs()
    print(f"Combined QR codes saved as {config['qr_name']}.")