from PIL import Image
import gzip

def extract_file(stego_image, output_file):
    img = Image.open(stego_image).convert("RGB")
    pixels = img.load()

    bits = []

    width, height = img.size

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]

            bits.append(str(r & 1))
            bits.append(str(g & 1))
            bits.append(str(b & 1))

    bits = ''.join(bits)

    compressed_size = int(bits[:32], 2)

    start = 32
    end = start + compressed_size * 8

    compressed_data = bytearray()

    for i in range(start, end, 8):
        compressed_data.append(
            int(bits[i:i+8], 2)
        )

    original_data = gzip.decompress(
        bytes(compressed_data)
    )

    with open(output_file, "wb") as f:
        f.write(original_data)

    print("복원 완료:", output_file)

# 사용 예시
extract_file(
    "stego.jpg",
    "recovered.pth"
)