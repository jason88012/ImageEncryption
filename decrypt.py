from permutation import inv_permutation
from diffusion import inv_diffusion
from chaos import chaosSystem3d

from PIL import Image

import sys
import timeit as t

key = [0.1, 0.2, 0.3]
 
def image_decrypt(cipher, key):
	chen_system = chaosSystem3d(key)
	per_img = inv_diffusion(cipher, chen_system)
	plain = inv_permutation(per_img, chen_system)
	return plain

def main():
	PATH = sys.argv[1]
	cipher = Image.open(PATH)

	plain = image_decrypt(cipher, key)

	name = input("Please input plain image name: ")
	plain.save(name+".bmp")

if __name__ == '__main__':
	main()