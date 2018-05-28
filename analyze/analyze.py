from functions import *
from PIL import Image
import matplotlib.image as mpimg
import os
import argparse

def histogram_analyze(plain, cipher):
	draw_histogram(plain, "Plain")
	draw_histogram(cipher, "Cipher")
	print("\nSave histogram file to %s" % os.getcwd())

def differential_analyze(cipher, diff_cipher):
	print("\nCalculating NPCR and UACI...")
	npcr, uaci = calc_diff(cipher, diff_cipher)
	print("NPCR = %s" % (npcr))
	print("UACI = %s" % (uaci))
	print("")

def correlation_analyze(plain, cipher):
	_policy = ["horizontal", "vertical", "diagonal"]
	for p in _policy:
		print("Calculating %s correlation..." % (p))
		plain_corr = calc_correlation(plain, 'plain', p)
		cipher_corr = calc_correlation(cipher, 'cipher', p)
		print("Plain image %s correlation is: %f" % (p, plain_corr))
		print("Cipher image %s correlation is: %f" % (p, cipher_corr))

def entropy_analyze(plain, cipher):
	print("\nCalculating image's entropy")
	plain_e = calc_entropy(plain, 'p')
	cipher_e = calc_entropy(cipher, 'c')
	print("Plain image's entropy is: %f" % plain_e)
	print("Cipher image's entropy is: %f" % cipher_e)

def psnr_analyze(plain, r_plain):
	print("Calculating image's MSE and PSNR ...")
	mse, psnr = calc_psnr(plain, r_plain)
	print("MSE: %s PSNR: %sdB" % (str(mse)[:-10], str(psnr)[:-10]))

def main(args):
	if args.all:
		# Open all require file
		PLAIN_PATH = input("Please specify plain image: ")
		plain = Image.open(PLAIN_PATH)
		arr_p = mpimg.imread(PLAIN_PATH)
		CIPHER_PATH = input("Please specify cipher image: ")
		cipher = Image.open(CIPHER_PATH)
		arr_c = mpimg.imread(CIPHER_PATH)
		DIFF_CIPHER = input("Please specify cipher image relative to one pixel changed plain image: ")
		diff_cipher = Image.open(DIFF_CIPHER)
		# Do all analysis
		histogram_analyze(arr_p, arr_c)
		differential_analyze(cipher, diff_cipher)
		correlation_analyze(plain, cipher)
		entropy_analyze(plain, cipher)

	else:
		if args.plot:
			PATH = input("Please specify image path: ")
			img = mpimg.imread(PATH)
			file_name = PATH.split('/')[-1]
			name = file_name.split('.')[-2]
			draw_histogram(img, name)
		elif args.correlation:
			PLAIN_PATH = input("Please specify plain image: ")
			plain = Image.open(PLAIN_PATH)
			CIPHER_PATH = input("Please specify cipher image: ")
			cipher = Image.open(CIPHER_PATH)			
			correlation_analyze(plain, cipher)
		elif args.entropy:
			PATH = input("Please specify image path: ")
			img = Image.open(PATH)			
			e = calc_entropy(img, 'c')
			print("image's entropy is: ", e)
		elif args.differential:
			CIPHER_PATH = input("Please specify cipher image: ")
			cipher = Image.open(CIPHER_PATH)			
			DIFF_CIPHER = input("Please specify cipher image relative to one pixel changed plain image: ")
			diff_cipher = Image.open(DIFF_CIPHER)
			differential_analyze(cipher, diff_cipher)
		elif args.noise:
			PLAIN_PATH = input("Please specify plain image: ")
			plain = Image.open(PLAIN_PATH)
			REC_IMG = input("Please specify recover plain image: ")
			r_plain = Image.open(REC_IMG)
			psnr_analyze(plain, r_plain)


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="cipher image KPI analysis tool")
	parser.add_argument("-p", "--plot", help="draw image's histogram", action="store_true")
	parser.add_argument("-d", "--differential", help="differential analysis", action="store_true")
	parser.add_argument("-c", "--correlation", help="image's correlation", action="store_true")
	parser.add_argument("-e", "--entropy", help="image's entropy", action="store_true")
	parser.add_argument("-n", "--noise", help="image's PSNR", action="store_true")
	parser.add_argument("-a", "--all", help="Do all analysis", action="store_true")
	args = parser.parse_args()
	main(args)