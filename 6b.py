#!/usr/bin/python

def count_breakpoints(P):
	count = 0 if P[0] == 1 else 1
	for index in xrange(len(P)-1):
		if P[index+1] != P[index] + 1:
			count+=1
	return count

data = [line[:-1] for line in open("input.txt", "r")][0]
print count_breakpoints(map(int, data[1:-1].split()))
