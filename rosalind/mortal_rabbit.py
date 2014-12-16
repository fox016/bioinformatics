#!/usr/bin/python

dur, m = 86, 20
memo = {1: (1,0,0), 2: (0,1,0)}

def count_rabbits(n):
	global m
	if n in memo:
		return memo[n]
	if n < 1:
		memo[n] = (0,0,0)
		return (0,0,0)
	last_count = count_rabbits(n-1)
	result = (last_count[1]-last_count[2], last_count[0]+last_count[1], last_count[2] + count_rabbits(n-m)[0])
	memo[n] = result
	return result

baby, adult, dead = count_rabbits(dur)
print baby + adult - dead
