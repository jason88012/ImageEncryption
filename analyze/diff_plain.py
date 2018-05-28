from PIL import Image
import random
import sys
import os

def diff_image(PATH):
	img = Image.open(PATH)
	# Random choose location and pixel value
	w = random.randint(0, img.size[0])
	h = random.randint(0, img.size[1])
	diff_pix = random.randint(0, 255)
	img.putpixel((w, h), diff_pix)
	print("Change pixe (%d,%d) to value %d" % (w, h, diff_pix))
	return img

def main():
	if len(sys.argv) != 2:
		raise "Usage: python3 diff_plain.py [plain image]"
	IMG_PATH = sys.argv[1]
	d = diff_image(IMG_PATH)
	name = input("Please specify output image's name: ")
	d.save(name+".bmp")
	print("save output file to %s" % os.path.dirname(os.path.abspath(__file__)))

if __name__ == '__main__':
	main()