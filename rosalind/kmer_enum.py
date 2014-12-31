#!/usr/bin/python

def get_combinations(alpha, length):
	pools = [alpha] * length
	result = [""]
	for pool in pools:
		result = [x+y for x in result for y in pool]
	return result

read = [line.split() for line in open("input.txt", "r")]
alpha = "".join(read[0])
length = int(read[1][0])
for c in get_combinations(alpha, length):
	print c
