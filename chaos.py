from scipy.integrate import odeint
import numpy as np
import math

'''
This file implement two kinds of chaos system
First one is "3d-chen system".
The second is "Logistic map".
'''
		
class chaosSystem3d(object):
	def __init__(self, init):
		self.a = 0.12521231547896
		self.b = 0.58749654123587
		self.c = 0.98564123475621
		self.init = init

	def chen(self, init, t):
		x, y, z = init

		xd = self.a*(y - x)
		yd = (self.c - self.a)*x - x*z + self.c*y
		zd = x*y - self.b*z
		return [xd, yd, zd]

	def generate_seq3d(self, t):
		state = odeint(self.chen, self.init, t)
		return state

	def generate_seq1d(self, t):
		# random seqence 1-d which is PRNS
		state = odeint(self.chen, self.init, t)
		PRNS = []
		for s in state:
			for i in range(3):
				frac = abs(math.modf(s[i])[0])
				x = int(math.floor((frac * 10**8)) % 256)
				PRNS.append(x)
		return PRNS

# This function generate keys in eXOR operation
def runLogisticMap(init, u=3.999999, step=2):
	chaos_signal = [init]
	for n in range(1, step+1):
		r = u * chaos_signal[n-1] * (1-chaos_signal[n-1])
		chaos_signal.append(r)
	return chaos_signal[1:]

# This function convert desire time step to require data stucture
def step(t):
	step = 0.0001
	start = 0.0
	end = t * step
	return np.arange(start, end, step)


# ===============================================================
def test():
	key = [0.22521231547896, 0.58749654123587, 0.98564123475621]
	chenSys = chaosSystem3d(key)
	s = chenSys.generate_seq3d(t=step(3))
	print(s)


if __name__ == '__main__':
	test()





