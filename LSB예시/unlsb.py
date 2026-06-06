from PIL import Image

def extract_text(image_file):
    img = Image.open(image_file)
    pixels = img.load()

    width, height = img.size

    bits = ""

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]

            bits += str(r & 1)
            bits += str(g & 1)
            bits += str(b & 1)

    text = ""

    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]

        if len(byte) < 8:
            break

        text += chr(int(byte, 2))

        if text.endswith("<<<END>>>"):
            print(text[:-9])
            return
        
print("lsb 스테가노그래피")
extract_text("secret_lsb.png")
print("lsb 스테가노그래피 jpg로 바꾼거")
extract_text("convert_lsb.jpg")