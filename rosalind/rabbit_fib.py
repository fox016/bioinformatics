#!/usr/bin/python

def rabbits(n, k):
	count = (0, 1)
	for year in xrange(n-1):
		count = (count[0]+count[1], count[0]*k)
	return count[0] + count[1]

"""
def rabbits(n, k):
	if n <= 2:
		return 1
	return rabbits(n-1, k) + k * rabbits(n-2, k)
"""

print rabbits(5, 3)
