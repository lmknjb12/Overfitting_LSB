from PIL import Image

def hide_text(input_image, output_image, message):
    img = Image.open(input_image)
    img = img.convert("RGB")
    pixels = img.load()

    # 종료 표시 추가
    message += "<<<END>>>"

    # 문자열 → 비트열
    bits = ''.join(format(ord(c), '08b') for c in message)

    width, height = img.size

    if len(bits) > width * height * 3:
        raise ValueError("이미지 용량이 부족합니다.")

    bit_index = 0

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]

            rgb = [r, g, b]

            for i in range(3):
                if bit_index < len(bits):
                    rgb[i] = (rgb[i] & 0b11111110) | int(bits[bit_index])
                    bit_index += 1

            pixels[x, y] = tuple(rgb)

            if bit_index >= len(bits):
                img.save(output_image)
                print("저장 완료:", output_image)
                return

hide_text("Blue_Devil.png", "secret_lsb.png", "I_Love_You_Arona")
img = Image.open('secret_lsb.png')
img.save('convert_lsb.jpg')
print("저장 완료:", "convert_lsb.jpg")