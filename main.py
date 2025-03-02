from watermarker import *

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Debug Run")
        file_name = "pexels-uriel-venegas-176524868-15321479.jpg"
        textToPut = "SampleText"
    else:
        try:
            file_name = sys.argv[1]
            print("Arguments")
        except IndexError:
            print("No input file, quitting")
            quit(0)
        textToPut = input('Text: ')
    options = WatermarkConfig()
    options.WATERMARK_OPACITY = float(input("Opacity 0.01-1.0 :"))
    options.DENSITY = int(input("Density 10-100 :"))
    options.FONT_SIZE_FACTOR = int(input("Size 10-100 :"))
    make_watermark(file_name, textToPut, options)
