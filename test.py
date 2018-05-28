import sys
import math
import timeit as t
import matplotlib.pyplot as plt

from chaos import *
from PIL import Image

global n, WIDTH, HIGHT

from encrypt import *
from decrypt import *

def buildNewImage(size):
	new = Image.new('L', size)
	newPix = new.load()

	for h in range(size[1]):
		for w in range(size[0]):
			newPix[w, h] = w
	return new

def printPix_(img):
	imgPix = img.load()
	for h in range(img.size[1]):
		print("")
		for w in range(img.size[0]):
			print(imgPix[w, h], end=' ')

img = Image.open(sys.argv[1])
print(img.getpixel((0,0))[0], img.getpixel((0,0))[1], img.getpixel((0,0))[2])





