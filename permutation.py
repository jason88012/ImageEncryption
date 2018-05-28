from PIL import Image
from projection import projection, inv_projection
from chaos import *

import sys
import numpy as np
import timeit as t

'''
This file implement the chaos based 3d bitmap permutation
'''
mode_to_bpp = {'1':1, 'L':8, 'P':8, 'RGB':24, 'RGBA':32, 'CMYK':32, 'YCbCr':24, 'I':32, 'F':32}

def findMinFac(n):
	f = 2
	while f < n:
		if n % f == 0:
			break
		else:
			f += 1
	return f

def calc_dim(img):
	w = img.size[0]
	h = img.size[1]
	d = mode_to_bpp[img.mode]

	dim = sorted([w, h, d], reverse=True)  
	while (1):
		hist_max = dim[0]
		f = findMinFac(dim[0])
		if (dim[2]*f < hist_max):
			dim[0] = dim[0] / f
			dim[2] = dim[2] * f
			dim.sort(reverse=True) 
		else:
			break
	return [int(i) for i in dim]

def mappingRule(chaos_system, size):
	state = chaos_system.generate_seq3d(step(max(size))).T

	#randState = state[0:128]
	rs = [state[0][:size[0]], state[1][:size[1]], state[2][:size[2]]]
	q = []
	sq = []
	for s in rs:
		q.append((s * (10**9)) % 65536)
		sq.append((s * (10**9)) % 65536)

	for s in sq:
		s.sort()

	rule = [[], [], []]
	for dim in range(len(q)):
		for i in range(len(q[dim])):
			idx = np.where(q[dim] == sq[dim][i])
			rule[dim].append(idx[0][0])
	#rule = np.array(rule)
	return rule

def mapping(srcBitArr, rule):
	assert len(srcBitArr.shape) == 3, "wrong bit array dimension"
	new = -1*(np.ones((len(rule[0]), len(rule[1]), len(rule[2])), dtype=np.bool))
	for w in range(srcBitArr.shape[0]):
		for h in range(srcBitArr.shape[1]):
			for d in range(srcBitArr.shape[2]):
				new[rule[0][w]][rule[1][h]][rule[2][d]] = srcBitArr[w][h][d]
	return new

def inv_mapping(perBitArr, rule):
	assert len(perBitArr.shape) == 3, "wrong bit array dimension"
	new = -1*(np.ones((len(rule[0]), len(rule[1]), len(rule[2])), dtype=np.bool))

	for w in range(perBitArr.shape[0]):
		for h in range(perBitArr.shape[1]):
			for d in range(perBitArr.shape[2]):
				new[w][h][d] = perBitArr[rule[0][w]][rule[1][h]][rule[2][d]]
	return new

def permutation(srcImg, chaos_system):
	# Use chen system generate mapping rule
	print("generating mapping rule...")

	t_start = t.default_timer()

	''' Change HERE to modify use new dimension alg whether or not'''
	#dim3d = calc_dim(srcImg)
	dim3d = [srcImg.size[0], srcImg.size[1], mode_to_bpp[srcImg.mode]]

	rule = mappingRule(chaos_system, dim3d)
	# Project pixel image to bit array
	srcBitArray = projection(srcImg, dim3d)
	# mapping according to mapping rule
	print("image permuting...")
	perBitArray = mapping(srcBitArray, rule)
	# project bit array to pixel image 
	perImg = inv_projection(perBitArray, srcImg.mode)

	t_end = t.default_timer()
	print("Eclipse time = %f" % (t_end - t_start))

	return perImg

def inv_permutation(perImg, chaos_system):
	# Use chen system generate mapping rule
	print("generating mapping rule...")
	dim3d = calc_dim(perImg)
	rule = mappingRule(chaos_system, dim3d)
	# Project pixel image to bit array
	perBitArray = projection(perImg, dim3d)
	# mapping according to mapping rule
	print("image permuting...")
	srcBitArray = inv_mapping(perBitArray, rule)
	# project bit array to pixel image 
	plainImg = inv_projection(srcBitArray, perImg.mode)
	return plainImg

### Test code
def buildNewImage(size):
	new = Image.new('L', size)
	newPix = new.load()

	for h in range(size[1]):
		for w in range(size[0]):
			newPix[w, h] = w
	return new


def test_permutation():
	srcImg = Image.open(sys.argv[1])
	key = [0.1, 0.2, 0.3]
	chen_system = chaosSystem3d(key)
	dim3d = calc_dim(srcImg)
	rule = mappingRule(chen_system, dim3d)
	perImg = permutation(srcImg, chen_system)

	#perImg.show()

	name = input("Please input saving name: ")
	name += ".bmp"
	perImg.save(name)

def test_invper():
	cipher = Image.open(sys.argv[1])
	key = [0.1, 0.2, 0.3]
	chen_system = chaosSystem3d(key)
	dim3d = calc_dim(cipher)
	rule = mappingRule(chen_system, dim3d)
	plain = inv_permutation(cipher, chen_system)
	name = input("Please input saving name: ")
	name += ".bmp"
	plain.save(name)

if __name__ == '__main__':
	if len(sys.argv) == 2:
		test_permutation()
	else:
		test_invper()