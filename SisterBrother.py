# coding: utf-8
import random as rnd
import matplotlib.pyplot as plt

def make_family(size, p):
	#stupid!!!
	#girls = rnd.randint(0,size)
	#boys = size - girls
	girls = 0
	boys = 0
	for i in range(size):
		# toss a coin for boiy or girl
		if rnd.random() < p:
			girls += 1
		else:
			boys += 1
			
	return girls, boys
	
def get_family_stats(girls, boys):
	n_girl_broth = int(boys)
	if girls == 0:
		n_girl_broth = 0
	n_boy_broth = int(boys-1)
	if boys == 0: 
		n_boy_broth = 0
	return n_girl_broth, n_boy_broth
	
def get_family_stats_2(girls, boys):
	p_boy_broth = 0
	p_girl_broth = 0
	if boys > 1:
		p_boy_broth = 1
	if girls > 0 and boys > 0:
		p_girl_broth = 1
	
	return p_girl_broth, p_boy_broth
	

mean_size = range(1,20)
mean_n_g = []
mean_n_b = []

for s in mean_size:
	size_tot = 0
	girls_tot = 0
	boys_tot = 0
	n_g_tot = 0
	n_b_tot = 0
	for i in range(10000):
		size = int(round(rnd.expovariate(1.0/s)))
		size_tot += size
		if size > 0:
			g, b = make_family(size, 0.8)
			girls_tot += g
			boys_tot += b
			n_g, n_b = get_family_stats(g, b)
			n_g_tot += g*n_g
			n_b_tot += b*n_b
				
	if girls_tot > 0:
		res_g = float(n_g_tot)/girls_tot
	else:
		res_g = 0.0
		
	if boys_tot > 0:
		res_b = float(n_b_tot)/boys_tot
	else:
		res_b = 0.0

	mean_n_g.append(res_g)
	mean_n_b.append(res_b)
		
	print("res g and b:", res_g, res_b)

# do the plotting	
plt.plot(mean_size,mean_n_b,'b', label="boys")
plt.plot(mean_size,mean_n_g,'r', label="girls")
plt.xlim(1,20)
plt.xlabel('mean family size')
plt.ylabel('average nnumber of brothers')
plt.legend(loc='upper left')
plt.show()