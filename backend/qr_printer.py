import qrcode
import json
from PIL import Image, ImageDraw, ImageFont
from brother_ql import BrotherQLRaster, create_label
from brother_ql.conversion import convert
from brother_ql.backends.helpers import send


with open('config.json') as config_file:
    config = json.load(config_file)


def create_qr_code(data, size=200):
    """Generate a QR code image."""
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    return qr.make_image(fill_color="black", back_color="white").resize((size, size))

def annotate_image(image, text, font):
    """Annotate the image with the specified text using a given font."""
    draw = ImageDraw.Draw(image)
    text_width, text_height = draw.textsize(text, font=font)
    # Position the text below the image
    draw.text(((image.width - text_width) / 2, image.height - text_height - 20), text, fill="black", font=font)

def generate_qrs(data1, data2):
    """Create a combined image with two QR codes and their annotations."""
    # Create QR codes
    qr_image1 = create_qr_code(data1)
    qr_image2 = create_qr_code(data2)

    # Create a new blank image with enough space for both QR codes and annotations
    combined_width = qr_image1.width + qr_image2.width + 20  # Add some space between
    combined_height = max(qr_image1.height + 50, qr_image2.height + 50)  # Space for annotations
    combined_image = Image.new('RGB', (combined_width, combined_height), 'white')

    # Paste QR codes onto the combined image
    combined_image.paste(qr_image1, (0, 0))
    combined_image.paste(qr_image2, (qr_image1.width + 20, 0))

    # Load a larger font (you can specify your own TTF file here)
    try:
        font = ImageFont.truetype("fonts/arialmt.ttf", size=32)  # Adjust size as needed
    except IOError:
        print("Custom font not found. Using default font.")
        font = ImageFont.load_default()

    # Annotate images with larger font
    annotate_image(combined_image, "  Passport         Transaction", font)

    combined_image.save(config["qr_name"])

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
    link1 = "https://example.com/first"
    link2 = "https://example.com/second"

    # Create the combined image
    generate_qrs(link1, link2)
    # print_qrs()
    print(f"Combined QR codes saved as {config['qr_name']}.")