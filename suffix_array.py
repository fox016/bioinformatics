#!/usr/bin/python

# http://www.cs.helsinki.fi/u/tpkarkka/publications/jacm05-revised.pdf
# http://en.wikipedia.org/wiki/Radix_sort#Example_in_Python

"""
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
"""

text = [line[:-2] for line in open("input.txt", "r")][0]
alpha = "$ACGT"
alpha_index_map = {
	"$": 0, 
	"A": 1,
	"C": 2,
	"G": 3,
	"T": 4
}

radix = 10

def radix_sort(list_of_nums):
	solution = list(list_of_nums)
	digit_place = 1
	done = False
	while True:
		done = True
		buckets = [list() for _ in xrange(radix)]
		for num in solution:
			index = (num / digit_place)
			buckets[index % 10].append(num)
			if index > 0:
				done = False
		if done:
			break
		solution = reduce(lambda x,y: x+y, buckets, [])
		digit_place*=10
	return solution

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

def compare_tuple(t1, t2):
	for index in xrange(len(t1)):
		if t1[index] < t2[index]:
			return -1
		if t1[index] > t2[index]:
			return 1
	return 0
 
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

	pairs = [int(T_int[i] + str(rank[i+1])) for i in B[0]]
	pairs_sorted = radix_sort(pairs)

	SC = map(lambda i: C[i-1], get_prime(R_sorted, R)) # TODO
	SB = map(lambda i: B[0][i-1], get_prime(pairs_sorted, pairs))

	solution = [0] * (n+1)
	SC_index = 0
	SB_index = 0
	for solution_index in xrange(len(solution)):
		i = SC[SC_index]
		j = SB[SB_index]
		if (i-1) % 3 == 0:
			Si = (T_int[i], rank[i+1])
			Sj = (T_int[j], rank[j+1])
		else:
			Si = (T_int[i], T_int[i+1], rank[i+2])
			Sj = (T_int[j], T_int[j+1], rank[j+2])
		if compare_tuple(Si, Sj) < 0:
			solution[solution_index] = i
			SC_index+=1
			if SC_index >= len(SC):
				return solution[0:solution_index+1] + SB[SB_index:]
		else:
			solution[solution_index] = j
			SB_index+=1
			if SB_index >= len(SB):
				return solution[0:solution_index+1] + SC[SC_index:]

print ', '.join(map(str, suffix_array(text)))
