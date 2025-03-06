from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import math, sys, random, time

SAVE_TEMP_IMAGES=False

class WatermarkConfig:

    def __init__(self):
        self.WATERMARK_OPACITY = 0.1
        self.DENSITY = 90
        self.FONT_SCALE = 90
        self.FONT_PATH = "arial.ttf"
        self.FONT_COLOR = (255, 255, 255)
        self.WATERMARK_ANGLE = -10
        self.DEBUG = True
        self.WATERMARK_SCALE_IMAGE = 2
        self.MIN_FONT_SIZE = 9
    def __str__(self):
        return str(self.__dict__)


def _get_watermarks_positions(inputImage: Image, number_marks: int, scale_multiplier) -> list:
    w, h = inputImage.size
    squareRoot = math.floor(math.sqrt(number_marks))
    blockSize_x = math.floor(w * scale_multiplier / squareRoot)
    blockSize_y = math.floor(h * scale_multiplier / squareRoot)
    squares = []
    centers = []
    for i in range(squareRoot):
        for j in range(squareRoot):
            squares.append([i * blockSize_x, j * blockSize_y])
    for s in range(number_marks):
        try:
            c_x = squares[s][0] + (blockSize_x / random.randrange(1, 2))
            c_y = squares[s][1] + (blockSize_y / random.randrange(1, 4))
            centers.append([c_x, c_y])
        except Exception:
            pass
    return centers


def _draw_temp_watermark(text: str, size_x: int, size_y: int, centers: list, fontName: str, text_font_size: int,
                         color=(255, 255, 255), opacity=0.2, scale_multiplier=2):
    empty_watermark_image = Image.new("RGBA", (size_x * scale_multiplier, size_y * scale_multiplier), (0, 0, 0, 0))
    draw = ImageDraw.Draw(empty_watermark_image, "RGBA")
    font_object = ImageFont.truetype(fontName,size=text_font_size)
    opacity_hex = int(opacity * 255)
    for c in centers:
        if random.choice((True, False, True, True)):
            draw.text(c, text, font=font_object, fill=(color[0], color[1], color[2], opacity_hex), )
        else:
            t = time.strftime("%d%m%y%H%M")
            draw.text(c, t, font=font_object, fill=(color[0], color[1], color[2], opacity_hex),
                      font_size=text_font_size)

    if SAVE_TEMP_IMAGES:
        empty_watermark_image.save("temp_watermark.png", "PNG")
    return empty_watermark_image


def _blend_watermark(original: Image, watermark: Image, scale: float, angle:float) -> Image:
    copy = original.copy()
    rotated = watermark.rotate(angle, resample=Image.Resampling.BICUBIC, expand=True)
    if SAVE_TEMP_IMAGES:
        rotated.save("rotated.png", "PNG")
    pad = copy.size[0] * 2 / scale
    croped = rotated.crop((pad, pad, copy.size[0] + pad, copy.size[1] + pad))
    if SAVE_TEMP_IMAGES:
        croped.save("croped.png", "PNG")
    return Image.alpha_composite(copy, croped)


def make_watermark(file_name: str, text: str, options: WatermarkConfig) -> Image:
    input_img = Image.open(file_name).convert("RGBA")

    # FONT SIZE
    fontSize = max(options.MIN_FONT_SIZE, math.floor(input_img.size[1] / options.FONT_SCALE))
    print("Font Size: ", fontSize)

    # Amount of watermarks
    amount = math.floor(input_img.size[1] * options.WATERMARK_SCALE_IMAGE / options.DENSITY)
    print("Amount: ", amount)

    watermarks_centers = _get_watermarks_positions(input_img, options.DENSITY, options.WATERMARK_SCALE_IMAGE)
    blank_watermark = _draw_temp_watermark(text, input_img.size[0], input_img.size[1], watermarks_centers,
                                           options.FONT_PATH,
                                           fontSize, options.FONT_COLOR, options.WATERMARK_OPACITY)
    final = _blend_watermark(input_img, blank_watermark, options.WATERMARK_SCALE_IMAGE, options.WATERMARK_ANGLE)
    new_name = file_name.split(".")[0] + "_" + text + ".png"
    final.save(new_name, "PNG")
    return final