import cv2
import numpy as np

def image_to_braille(image_path, output_txt_path, threshold=127)
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"Cannot find image at {image_path}")

    h, w = img.shape
    new_w = w - (w % 2)
    new_h = h - (h % 4)
    img = cv2.resize(img, (new_w, new_h))

    _, binary = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY_INV)

    def pixels_to_braille(block):
        dot_positions = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80]
        value = 0
        index = 0
        for col in range(2): 
            for row in range(4):
                if block[row, col] > 0:
                    value |= dot_positions[index]
                index += 1
        return chr(0x2800 + value)

    braille_lines = []
    for y in range(0, new_h, 4):
        line = ""
        for x in range(0, new_w, 2):
            block = binary[y:y+4, x:x+2]
            if block.shape != (4, 2):
                block = np.pad(block, ((0, 4 - block.shape[0]), (0, 2 - block.shape[1])), mode='constant')
            char = pixels_to_braille(block)
            line += char
        braille_lines.append(line)

    with open(output_txt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(braille_lines))

    print(f"Braille Art written to {output_txt_path}")

image_to_braille("input.jpg", "sample.txt")
