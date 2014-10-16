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

def get_prime(list_of_nums, sorted_list):
	list_map = {}
	for index in xrange(len(sorted_list)):
		element = sorted_list[index]
		if element in list_map:
			list_map[element]['indexes'].append(index)
			list_map[element]['count']+=1
		else:
			list_map[element] = {"count": 0, "indexes": [index]}
	ranks = []
	for element in list_of_nums:
		ranks.append(list_map[element]['indexes'][list_map[element]['count']]+1)
		list_map[element]['count']-=1
	return ranks

def radix_sort(list_of_nums):
	solution = list(list_of_nums)
	placement = 1
	while True:
		buckets = [list() for _ in xrange(radix)]
		for num in solution:
			index = num / placement
			buckets[index % radix].append(num)
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
	R_prime = get_prime(R, R_sorted)

	rank = [None for _ in xrange(len(T)+1)]
	for index in xrange(len(C)):
		i = C[index]
		rank[i] = R_prime[index]
	rank[n+1] = 0
	rank[n+2] = 0

suffix_array(text)
