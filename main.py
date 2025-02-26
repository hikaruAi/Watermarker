from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import math, sys, random, time

WATERMARK_OPACITY = 0.1

AMOUNT_FACTOR = 20
FONT_FACTOR = 80
FONT_NAME = "arial.ttf"
WATERMARK_ANGLE = -10
DEBUG=True
WATERMARK_SCALE_IMAGE=2
MIN_FONT_SIZE=10

def guess_font_size(inputImage: Image) -> int:
    return max(MIN_FONT_SIZE, math.floor(inputImage.size[1] / FONT_FACTOR))


def guess_amount_watermarks(inputImage: Image) -> int:
    return math.floor(inputImage.size[1]*WATERMARK_SCALE_IMAGE / AMOUNT_FACTOR)


def get_watermarks_positions(inputImage: Image, number_marks: int) -> list:
    w, h = inputImage.size
    squareRoot = math.floor(math.sqrt(number_marks))
    blockSize_x, blockSize_y = math.floor(w * WATERMARK_SCALE_IMAGE / squareRoot), math.floor(h* WATERMARK_SCALE_IMAGE/ squareRoot)
    squares = []
    centers = []
    for i in range(squareRoot):
        for j in range(squareRoot):
            squares.append([i * blockSize_x, j * blockSize_y])
    for s in range(number_marks):
        try:
            centers.append([squares[s][0] + (blockSize_x / random.randrange(1,2)), squares[s][1] + (blockSize_y /random.randrange(1,4))])
        except Exception:
            pass
    return centers


def create_watermarks(text: str, size_x: int, size_y: int, centers: list, fontName: str, font_size: int,
                      color=(255, 255, 255), opacity=0.2):
    empty_watermark_image = Image.new("RGBA", (size_x * WATERMARK_SCALE_IMAGE, size_y * WATERMARK_SCALE_IMAGE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(empty_watermark_image, "RGBA")
    font_object = ImageFont.truetype(fontName, font_size)
    opacity_hex = int(opacity * 255)
    for c in centers:
        if random.choice((True,False, True, True)):
            draw.text(c, text, font=font_object, fill=(color[0], color[1], color[2], opacity_hex))
        else:
            t= time.strftime("%d-%m-%y,%H:%M:%S")
            draw.text(c, t, font=font_object, fill=(color[0], color[1], color[2], opacity_hex))

    empty_watermark_image.save("temp_watermark.png", "PNG")
    return empty_watermark_image


def blend_watermark(original: Image, watermark: Image) -> Image:
    copy = original.copy()
    rotated = watermark.rotate(WATERMARK_ANGLE, resample=Image.Resampling.BICUBIC, expand=True)
    rotated.save("rotated.png","PNG")
    pad=copy.size[0]*2/(WATERMARK_SCALE_IMAGE)
    croped= rotated.crop((pad,pad,copy.size[0] +pad ,copy.size[1] + pad))
    croped.save("croped.png", "PNG")
    return Image.alpha_composite(copy, croped)


if __name__ == '__main__':
    if len(sys.argv)==1:
        print("Debug Run")
        file_name= "pexels-uriel-venegas-176524868-15321479.jpg"
        textToPut="SampleText"
    else:
        try:
            file_name = sys.argv[1]
        except IndexError:
            print("No input file, quitting")
            quit(0)
        textToPut = input('Text: ')
        WATERMARK_OPACITY= float(input("Opacity 0.01-1.0 :"))

    inputImg = Image.open(file_name).convert("RGBA")
    fontSize = guess_font_size(inputImg)
    amount = guess_amount_watermarks(inputImg)

    watermarks_centers = get_watermarks_positions(inputImg, amount)
    watermarked_Image = create_watermarks(textToPut, inputImg.size[0], inputImg.size[1], watermarks_centers, FONT_NAME,
                                          fontSize, opacity=WATERMARK_OPACITY)
    final = blend_watermark(inputImg, watermarked_Image)
    new_name = file_name.split(".")[0] + "_" + textToPut + ".png"
    final.save(new_name, "PNG")
