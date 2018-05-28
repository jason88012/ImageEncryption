import sys
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

mode_to_bpp = {'1':1, 'L':8, 'P':8, 'RGB':24, 'RGBA':32, 'CMYK':32, 'YCbCr':24, 'I':32, 'F':32}

def calc_ylim(size):
	avg = size[0]*size[1] / 256
	lim = 0
	while lim < avg:
		lim += 500
	return lim*3

def draw_histogram(img, name):
	plt.clf()
	if len(img.shape) == 2:
		# Greyscale image
		plt.hist(img.ravel(), bins=256, range=(0, 255))
		axis = plt.axes()
		axis.set_xlim(0, 255)
		axis.set_ylim(0, calc_ylim(img.shape[:2]))
		plt.title('histogram')
		plt.ylabel("pixel numbers")
		plt.xlabel("pixel gray level")
		plt.savefig(name+"_histogram")
	else:
		# RGB image
		_COLOR = ['red', 'green', 'blue']
		for i in range(3):
			plt.clf()
			lum_img = img[:,:,i]
			plt.hist(lum_img.ravel(), bins=256, range=(0, 255), fc=_COLOR[i], ec=_COLOR[i])
			axis = plt.axes()
			axis.set_xlim(0, 255)
			axis.set_ylim(0, calc_ylim(img.shape[:2]))
			plt.title('histogram')
			plt.ylabel("pixel numbers")
			plt.xlabel("pixel %s level" % (_COLOR[i]))
			plt.savefig("%s_%s_histogram" % (name, _COLOR[i]))


def draw_distribution(x, y, name, p):
	x_label = "pixel grayvalue in location(x,y)"
	y_label = ""
	plt.clf()
	plt.scatter(x,y,s=0.2)
	plt.xlim([0, 255])
	plt.ylim([0, 255])
	#plt.axis('square')
	if p == "horizontal":
		y_label = "pixel grayvalue in location(x+1,y)"
	elif p == "vertical":
		y_label = "pixel grayvalue in location(x,y+1)"
	elif p == "diagonal":
		y_label = "pixel grayvalue in location(x+1,y+1)"
	plt.xlabel(x_label)
	plt.ylabel(y_label)
	file_name = "%s_%s_distribute" % (p, name)
	plt.savefig(file_name, dpi=1200)

def calc_diff(c, diff_c):
	if c.size != diff_c.size:
		raise "Input image has different size (W, H)"

	# NPCR: Number of Pixel Changing Rate
	# UACI: Unified Average Changed Intensify
	depth = int(mode_to_bpp[c.mode]/8)

	if depth == 1:
		# gray scale
		npc = 0
		uci = 0
		for w in range(c.size[0]):
			for h in range(c.size[1]):
				c_pix = c.getpixel((w, h))
				d_pix = diff_c.getpixel((w, h))
				uci += abs(c_pix - d_pix)
				if c_pix != d_pix:
					npc += 1
		npcr = npc / (c.size[0] * c.size[1]) * 100
		uaci = uci / (c.size[0] * c.size[1] * 256) * 100
	else:
		# RGB scale
		npc = [0, 0, 0]
		uci = 0
		for w in range(c.size[0]):
			for h in range(c.size[1]):
				c_pix = c.getpixel((w, h))
				d_pix = diff_c.getpixel((w, h))
				for i in range(len(c_pix)):
					uci += abs(c_pix[i] - d_pix[i])
					if c_pix[i] != d_pix[i]:
						npc[i] += 1
		npcr = [x/(c.size[0] * c.size[1])*100 for x in npc]
		uaci = uci / (c.size[0] * c.size[1] * 256 * depth) * 100

	if isinstance(npcr, list):
		NPCR = [str(round(x, 6))+"%" for x in npcr]
	else:
		NPCR = str(round(npcr, 6)) + "%"
	UACI = str(round(uaci, 6)) + "%"
	return NPCR, UACI

def calc_entropy(img, mode):
	size = img.size[0] * img.size[1]
	hist = img.histogram()
	depth = len(hist) / 256
	H = 0
	for i in hist:
		if i == 0:
			H += 0
			continue
		pi = i / size
		H += pi * math.log2(pi)
	return -H/depth

def calc_correlation(img, name, policy):
	x = []
	y = []
	if policy == "horizontal":
		for w in range(0, img.size[0]-1):
			for h in range(0, img.size[1]):
				x.extend(list(img.getpixel((w, h))))
				y.extend(list(img.getpixel((w+1, h))))

	elif policy == "vertical":
		for w in range(0, img.size[0]):
			for h in range(0, img.size[1]-1):
				x.extend(list(img.getpixel((w, h))))
				y.extend(list(img.getpixel((w, h+1))))

	elif policy == "diagonal":
		for w in range(0, img.size[0]-1):
			for h in range(0, img.size[1]-1):
				x.extend(list(img.getpixel((w, h))))
				y.extend(list(img.getpixel((w+1, h+1))))

	#draw_distribution(x, y, name, policy)
	N = len(x)
	x_ = sum(x) / N
	y_ = sum(y) / N
	frac = 0
	nume_x = 0
	nume_y = 0
	for i in range(N):
		frac += (x[i] - x_)*(y[i] - y_)
		nume_x += (x[i] - x_)**2
		nume_y += (y[i] - y_)**2
	cov = (frac/N) / math.sqrt( (nume_x/N)*(nume_y/N) )
	return abs(cov)

def calc_psnr(plain, r_plain):
	if plain.size != r_plain.size:
		raise "Input image has different size (W, H)"

	e = 0
	pixNum = len(plain.getpixel((0,0)))
	if pixNum == 1:
		# greyscale
		for h in range(plain.size[1]):
			for w in range(plain.size[0]):
				d = abs(plain.getpixel((w, h)) - r_plain.getpixel((w, h))) ** 2
				e += d
	else:
		# RGB scale
		for h in range(plain.size[1]):
			for w in range(plain.size[0]):
				d = 0
				for p in range(pixNum):
					d += abs(plain.getpixel((w, h))[p] - r_plain.getpixel((w, h))[p]) ** 2
				e += d

	mse = e / (plain.size[0]*plain.size[1]*pixNum)
	if mse == 0:
		return mse, 100
	psnr = 10 * math.log10((255*255) / mse)
	return mse, psnr


