#import numpy as np
import sys
import math
import timeit as t

from PIL import Image
from chaos import *

global n, WIDTH, HIGHT

'''
This file implement a diffusion algorithm
Included eXOR(extended XOR) and temp value diffusion
'''

def eXOR(x, r):
	result = []
	bin_x = bin(x)[2:].zfill(8)
	bin_r = bin(r)[2:].zfill(9)
	for i in range(len(bin_x)):
		xi, ri, rii = bool(int(bin_x[i])), bool(int(bin_r[i])), bool(int(bin_r[i+1]))
		result.append(str(int(not(xi^ri^rii))))
	return int(''.join(result), 2)

# Transform 1d index to 2d position
def locate(index):
	global WIDTH, HIGHT
	w = int(index % WIDTH)
	h = int(index / WIDTH)
	return (w, h)

# Calculate temp key
def get_r0(plain_pix, x):
	if x <= plain_pix:
		r0 = ((float(x) + 127.0) / (float(plain_pix) + 255.0))
	else:
		r0 = ((float(plain_pix) + 127.0) / (float(x) + 255.0))
	return r0

def calc_temp_key(r0):
	keys = runLogisticMap(init=r0)
	r  = int(math.floor(keys[0] * 10**3) % 512)
	r_ = int(math.floor(keys[1] * 10**3) % 512)
	return r, r_

# Single pixel diffusion operation
def diff(_p, p, _c, x):
	r0 = get_r0(_p, x)
	r, r_ = calc_temp_key(r0)
	c = int((eXOR(p, r) + eXOR(_c, r_)) % 256)
	return c

def inv_diff(_c, c, _p, x):
	r0 = get_r0(_p, x)
	r, r_ = calc_temp_key(r0)
	p = eXOR(int((c - eXOR(_c, r_))%256), r)
	return p

# Check rgb or grayscale
def encrypt(_p, p, _c, x):
	pixels = []
	if isinstance(p, int):
		return diff(_p, p, _c, x)
	else:
		if isinstance(_p, int):
			_p = [_p]*len(p)
			_c = [_c]*len(p)
		for i in range(len(p)):
			c = diff(_p[i], p[i], _c[i], x)
			pixels.append(c)
	return tuple(pixels)

def decrypt(_c, c, _p, x):
	pixels = []
	if isinstance(c, int):
		return inv_diff(_c, c, _p, x)
	else:
		if isinstance(_c, int):
			_c = [_c]*len(c)
			_p = [_p]*len(c)		
		for i in range(len(c)):
			p = inv_diff(_c[i], c[i], _p[i], x)
			pixels.append(p)
	return tuple(pixels)

# Iterate to encrypt or decrypt
def diff_round1(perImg, prns):
	global n
	# Defined initial condition
	m0 = prns[n+1]
	p0 = prns[n]

	# Declare new piture
	tempImg = Image.new(perImg.mode, perImg.size)
	tempPix = tempImg.load()

	# Calculate first encrypt pixel use defined initial condition
	tempPix[0, 0] = encrypt(p0, perImg.getpixel(locate(0)), m0, prns[0])

	# Encrypt image in sequential (i = 1 ~ n-1)
	for i in range(1, n):
		tempPix[locate(i)] = encrypt(perImg.getpixel(locate(i-1)), perImg.getpixel(locate(i)), tempImg.getpixel(locate(i-1)), prns[i])
	return tempImg

def diff_round2(tempImg, prns):
	global n
	# Defined initial condition
	m_n = prns[n+3]
	c_n = prns[n+2]

	# Declare new image
	cipherImg = Image.new(tempImg.mode, tempImg.size)
	cipherPix = cipherImg.load()

	# Calculate last encrypt pixel use defined initial condition
	cipherPix[locate(n-1)] = encrypt(m_n, tempImg.getpixel(locate(n-1)), c_n, prns[0])

	# Encrypt image in sequential reversely (i = n-1 ~ 0)
	for i in range(n-2, -1, -1):
		cipherPix[locate(i)] = encrypt(tempImg.getpixel(locate(i+1)), tempImg.getpixel(locate(i)), cipherPix[locate(i+1)], prns[n-i-1])
	return cipherImg

def inv_diff_r1(cipherImg, prns):
	global n
	# Defined initial condition
	m_n = prns[n+3]
	c_n = prns[n+2]

	# Declare new image
	tempImg = Image.new(cipherImg.mode, cipherImg.size)
	tempPix = tempImg.load()

	# Decrypt last encrypted pixel use defined initial condition
	tempPix[locate(n-1)] = decrypt(c_n, cipherImg.getpixel(locate(n-1)), m_n, prns[0])
	# Decrypt other pixels in sequential reversely (i = n-1 ~ 0)
	for i in range(n-2, -1, -1):
		tempPix[locate(i)] = decrypt(cipherImg.getpixel(locate(i+1)), cipherImg.getpixel(locate(i)), tempPix[locate(i+1)], prns[n-i-1])
	return tempImg

def inv_diff_r2(tempImg, prns):
	global n
	# Defined initial condition
	m0 = prns[n+1]
	p0 = prns[n]

	# Declare new piture
	perImg = Image.new(tempImg.mode, tempImg.size)
	perPix = perImg.load()

	# Calculate first encrypt pixel use defined initial condition
	perPix[0, 0] = decrypt(m0, tempImg.getpixel(locate(0)), p0, prns[0])
	# decrypt other pixels in sequential (i = 1 ~ n-1)
	for i in range(1, n):
		perPix[locate(i)] = decrypt(tempImg.getpixel(locate(i-1)), tempImg.getpixel(locate(i)), perPix[locate(i-1)], prns[i])
	return perImg

def diffusion(perImg, chaos_system):
	global n, WIDTH, HIGHT
	n = perImg.size[0] * perImg.size[1]
	WIDTH = perImg.size[0]
	HIGHT = perImg.size[1]

	PRNS = chaos_system.generate_seq1d(step(math.ceil((n+4)/3)+1000))
	print("round1 encryption...")
	tempImg = diff_round1(perImg, PRNS)
	print("round2 encryption...")
	cipher = diff_round2(tempImg, PRNS)
	return cipher

def inv_diffusion(cipherImg, chaos_system):
	global n, WIDTH, HIGHT
	n = cipherImg.size[0] * cipherImg.size[1]
	WIDTH = cipherImg.size[0]
	HIGHT = cipherImg.size[1]

	PRNS = chaos_system.generate_seq1d(step(math.ceil((n+4)/3)+1000))
	print("round1 decryption...")
	tempImg = inv_diff_r1(cipherImg, PRNS)
	print("round2 decryption...")
	perImg = inv_diff_r2(tempImg, PRNS)
	return perImg




###================================================================================

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


def test_diff():
	key = [0.22521231547896, 0.58749654123587, 0.98564123475621]
	chen_system = chaosSystem3d(key)
	img = Image.open(sys.argv[1])

	diff_img = diffusion(img, chen_system)
	name = input("Please input saving name: ")
	name += ".bmp"
	diff_img.save(name)

def test_invdiff():
	key = [0.22521231547896, 0.58749654123587, 0.98564123475621]
	chen_system = chaosSystem3d(key)
	img = Image.open(sys.argv[1])

	p_img = inv_diffusion(img, chen_system)
	name = input("Please input saving name: ")
	name += ".bmp"
	p_img.save(name)



if __name__ == '__main__':
	if len(sys.argv) == 2:
		test_diff()
	else:
		test_invdiff()






