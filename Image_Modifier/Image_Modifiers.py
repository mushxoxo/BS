from wand.image import Image
from PIL import Image as PILImage
from wand.image import Image as WandImage
from io import BytesIO

def pil_to_wand(pil_img: PILImage.Image) -> WandImage:
    """
    Converts a PIL Image to a Wand Image.
    """
    buffer = BytesIO()
    pil_img.save(buffer, format="PNG")
    buffer.seek(0)
    return WandImage(blob=buffer.read())

def wand_to_pil(wand_img: WandImage) -> PILImage.Image:
    """
    Converts a Wand Image to a PIL Image.
    """
    blob = wand_img.make_blob("PNG")
    return PILImage.open(BytesIO(blob))

def Sharpener(img: Image) -> Image:

    with img as wimg:

        wimg.unsharp_mask(radius = .5, sigma = 6.25, amount= 6.25, threshold=0)
        wimg.compression_quality = 100
        return wand_to_pil(wimg)

def Compressor(img: Image, max_width, max_height):
    
    with img as img:
        
        if img.width > max_width and img.height > max_height:

            width_ratio = max_width/img.width
            height_ratio = max_height/img.height
            scale_ratio = max(width_ratio, height_ratio)

            new_width = int(img.width * scale_ratio)
            new_height = int(img.height * scale_ratio)

            img.filter = 'lanczos'
            img.resize(new_width, new_height)
            print("Resized")
        
        img.unsharp_mask(radius=0, sigma = 0.2, amount = .5, threshold= 0.05)
        img.compression = 85
        return wand_to_pil(img)

def Blur(img: Image, rad): 

    with img as img:

        img.blur(radius= rad, sigma= 3)
        return wand_to_pil(img)        
