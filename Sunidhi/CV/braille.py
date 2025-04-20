import cv2
import numpy as np

# Braille dot positions mapped to Unicode bits
BRAILLE_OFFSET = 0x2800
DOTS = [
    (0, 0),  # Dot 1
    (1, 0),  # Dot 2
    (2, 0),  # Dot 3
    (0, 1),  # Dot 4
    (1, 1),  # Dot 5
    (2, 1),  # Dot 6
    (3, 0),  # Dot 7
    (3, 1),  # Dot 8
]

def image_to_braille(image_path, output_path='braille_output.txt', threshold=127):
    # Load and convert to grayscale
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print("Failed to load image.")
        return

    # Resize to multiple of 2 (width) x 4 (height)
    new_width = (img.shape[1] // 2) * 2
    new_height = (img.shape[0] // 4) * 4
    img = cv2.resize(img, (new_width, new_height))

    # Threshold to binary
    _, binary = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY_INV)

    braille_rows = []

    # Traverse image in 4x2 blocks
    for y in range(0, binary.shape[0], 4):
        row = ''
        for x in range(0, binary.shape[1], 2):
            braille_char = 0
            for idx, (dy, dx) in enumerate(DOTS):
                py, px = y + dy, x + dx
                if py < binary.shape[0] and px < binary.shape[1]:
                    if binary[py, px] > 0:
                        braille_char |= (1 << idx)
            row += chr(BRAILLE_OFFSET + braille_char)
        braille_rows.append(row)

    # Save to text file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(braille_rows))

    print(f"Braille art saved to {output_path}")

# Example usage
image_to_braille("pic.jpg")