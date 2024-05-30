import qrcode
from PIL import Image, ImageDraw, ImageFilter

def generate_fancy_qr_code(data,filename):
    qr = qrcode.QRCode(
        version = 1,
        error_correction = qrcode.constants.ERROR_CORRECT_H,
        box_size = 10,
        border = 2,
    )
    qr.add_data(data)
    qr.make(fit=True)

    qr_image = qr.make_image(fill_color="white",back_color="black").convert("RGBA")

    # Create a circular gradient overlay
    overlay = Image.new("RGBA", qr_image.size)
    draw = ImageDraw.Draw(overlay)
    center_x, center_y = qr_image.width // 2, qr_image.height // 2
    radius = min(qr_image.width, qr_image.height) // 2

    for r in range(radius,0,-1):
        alpha = int(255 * (1 - r / radius))
        color = (247,212,54,alpha)
        draw.ellipse(
            (center_x - r, center_y - r, center_x + r, center_y + r),
            fill = color,
            outline = None
        )

    qr_image = Image.alpha_composite(qr_image,overlay)
    
    # Add a logo
    logo = Image.open("ataglance.png")
    logo_size = (qr_image.width // 4, qr_image.height // 4)
    logo = logo.resize(logo_size, Image.ANTIALIAS)
    logo_position = (
        (qr_image.width - logo_size[0]) // 2,
        (qr_image.height - logo_size[1]) // 2
    )

    qr_image.paste(logo,logo_position,logo)
    qr_image.save(filename)

data = "https://www.youtube.com/@ataglanceofficial"
filename = "fancy_qr_code.png"
generate_fancy_qr_code(data,filename)
