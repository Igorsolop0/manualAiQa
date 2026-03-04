#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
import os

# Створюємо тестове зображення 200x200
img = Image.new('RGB', (200, 200), color=(153, 69, 255))  # #9945FF
draw = ImageDraw.Draw(img)

# Спрощений текст (без шрифту)
draw.text((50, 80), "Test", fill=(255, 255, 255))

# Зберігаємо
img.save('test-image.jpg', 'JPEG')
print("Test image created: test-image.jpg")
print(f"Size: {os.path.getsize('test-image.jpg')} bytes")