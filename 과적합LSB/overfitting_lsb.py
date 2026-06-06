from PIL import Image
import math
import gzip

def hide_file_auto_expand(input_image, input_file, output_image):
    # 파일 읽기
    with open(input_file, "rb") as f:
        file_data = f.read()

    # gzip 압축
    compressed = gzip.compress(file_data)

    print(f"원본 크기: {len(file_data):,} bytes")
    print(f"압축 크기: {len(compressed):,} bytes")

    # 크기 헤더(4바이트) 추가
    payload = len(compressed).to_bytes(4, "big") + compressed

    img = Image.open(input_image).convert("RGB")
    width, height = img.size

    required_bits = len(payload) * 8
    capacity = width * height * 3

    # 용량 부족하면 자동 확장
    if capacity < required_bits:
        required_pixels = math.ceil(required_bits / 3)

        # 여유 5% 추가
        required_pixels = math.ceil(required_pixels * 1.05)

        new_side = math.ceil(math.sqrt(required_pixels))

        print(
            f"이미지 확장: {width}x{height} → "
            f"{new_side}x{new_side}"
        )

        expanded = Image.new(
            "RGB",
            (new_side, new_side),
            (255, 255, 255)
        )

        expanded.paste(img, (0, 0))
        img = expanded

        width, height = img.size

    pixels = img.load()

    # 비트열 생성
    bits = ''.join(
        f'{byte:08b}'
        for byte in payload
    )

    bit_index = 0

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]

            rgb = [r, g, b]

            for i in range(3):
                if bit_index < len(bits):
                    rgb[i] = (
                        rgb[i] & 0b11111110
                    ) | int(bits[bit_index])

                    bit_index += 1

            pixels[x, y] = tuple(rgb)

            if bit_index >= len(bits):
                img.save(output_image)
                print("저장 완료:", output_image)
                return

# 사용 예시
hide_file_auto_expand(
    "MyGirl.png",
    "balanced_spike_model.pth",
    "stego.png"
)