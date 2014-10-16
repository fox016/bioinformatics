#!/usr/bin/python

from math import log

text = "yabbadabbado"
alpha = "$abdoy"
alpha_index_map = {
	"$": 0, 
	"a": 1,
	"b": 2,
	"d": 3,
	"o": 4,
	"y": 5
}
radix = 10

def radix_sort(list_of_nums):
	solution = list(list_of_nums)
	placement = 1
	while True:
		buckets = [list() for _ in xrange(radix)]
		for num in solution:
			index = num / placement
			buckets[index % radix].append(num)
		print buckets
		if index <= 0:
			break
		solution = reduce(lambda x,y: x+y, buckets, [])
		placement*=radix
	return solution
 
def suffix_array(T):
	n = len(T)
	B = [range(start, n+1, 3) for start in xrange(3)]
	C = B[1] + B[2]
	T+="$$"
	T_int = ''.join(map(lambda char: str(alpha_index_map[char]), T))
	R = map(int, [T_int[k+start:k+start+3] for k in [1,2] for start in xrange(0, n, 3)])
	R_sorted = radix_sort(R)
	print R
	print R_sorted

suffix_array(text)
