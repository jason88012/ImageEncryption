from permutation import permutation
from diffusion import diffusion
from chaos import chaosSystem3d

from PIL import Image

import sys
import timeit as t

key = [0.1, 0.2, 0.3]
def image_encrypt(src_img, key):
	chen_system = chaosSystem3d(key)
	per_img = permutation(src_img, chen_system)
	cipher = diffusion(per_img, chen_system)
	return cipher

def main():
	PATH = sys.argv[1]
	src_img = Image.open(PATH)

	t_start = t.default_timer()
	cipher = image_encrypt(src_img, key)
	t_end = t.default_timer()
	print("Finished!")
	print("Total eclipse time: %4fsec" % (t_end - t_start))

	name = input("Please input cipher file name: ")
	cipher.save(name+".bmp")

if __name__ == '__main__':
	main()