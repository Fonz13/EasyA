from PIL import Image
from pix2tex.cli import LatexOCR
from os import walk


model = LatexOCR()

mypath = "data"
filenames = next(walk(mypath), (None, None, []))[2]

file_list = []
for f in filenames:
    img = Image.open(f"data/{f}")
    file_list.append(model(img))
    

