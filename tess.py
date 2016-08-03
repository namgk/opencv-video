#!/usr/bin/env python
from PIL import Image
import pytesseract

print(pytesseract.image_to_string(Image.open('test_small.jpg')))
