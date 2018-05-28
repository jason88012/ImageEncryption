import numpy as np
from PIL import Image

"""
Traversal all pixels and convert to bit type
use np.reshape method to project to 3d bit-array
"""

global WIDTH, HIGHT, DEPTH
mode_to_bpp = {'1':1, 'L':8, 'P':8, 'RGB':24, 'RGBA':32, 'CMYK':32, 'YCbCr':24, 'I':32, 'F':32}

def toBinary(pixel):
	bit = ''
	if isinstance(pixel, int):
		bit = bin(pixel)[2:].zfill(8)
	else:
		for i in range(len(pixel)):
			b = bin(pixel[i])[2:].zfill(8)
			bit += b
	return bit

def toPixel(bit):
	pixNum = int(len(bit)/8)
	pixels = []
	for i in range(pixNum):
		b = bit[8*i : 8*(i+1)]
		pix = int(b, 2)
		pixels.append(pix)

	if len(pixels) == 1:
		return pixels[0]
	return tuple(pixels)
	

def projection(image, dim):
	global WIDTH, HIGHT, DEPTH
	WIDTH, HIGHT = image.size
	DEPTH = mode_to_bpp[image.mode]

	bit = []
	for h in range(HIGHT):
		for w in range(WIDTH):
			pix = image.getpixel((w,h))
			#print(pix)
			b = toBinary(pix)
			bit.append(list(b))
	bit = np.uint8(bit)
	bitArray = bit.reshape(dim)
	return bitArray

def inv_projection(bitArray, imgMode):
	global WIDTH, HIGHT, DEPTH
	bitArray = bitArray.astype(str)
	bitArray1D = bitArray.reshape((WIDTH*HIGHT, DEPTH))
	bitArray1D = bitArray1D.tolist()

	# Declare new piture
	new_image = Image.new(imgMode, (WIDTH, HIGHT))
	new_pix = new_image.load()

	# Convert bitvalue to pixel value
	for h in range(HIGHT):
		for w in range(WIDTH):
			b = ''.join(bitArray1D[h*WIDTH + w])
			pix = toPixel(b)
			new_pix[w, h] = pix
	return new_image

