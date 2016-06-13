# coding: utf-8
import math
def checkFermat(a,b,c,n):
	if  pow(c,n) == pow(a,n) + pow(b,n):
		return True
	else:
		return False	
		