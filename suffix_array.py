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
text = "AACGATAGCGGTAGA"
alpha = "$ACGT"
alpha_index_map = {
	"$": 0, 
	"A": 1,
	"C": 2,
	"G": 3,
	"T": 4
}

def radix_sort(list_of_nums):
	solution = list(list_of_nums)
	digit_place = 1
	done = False
	while not done:
		done = True
		buckets = [list() for _ in xrange(10)]
		for num in solution:
			index = (num / digit_place)
			buckets[index % 10].append(num)
			if index > 0:
				done = False
		solution = reduce(lambda x,y: x+y, buckets, [])
		digit_place*=10
	return solution

def get_prime(list_of_nums, sorted_list):
	list_map = {}
	duplicates = False
	for index in xrange(len(sorted_list)):
		element = sorted_list[index]
		if element in list_map:
			duplicates = True
		list_map[element] = index
	ranks = []
	for element in list_of_nums:
		ranks.append(list_map[element]+1)
	return ranks, duplicates

def compare_tuple(t1, t2):
	for index in xrange(len(t1)):
		if t1[index] < t2[index]:
			return -1
		if t1[index] > t2[index]:
			return 1
	return 0
 
def suffix_array(T):

	print "T", T

	n = len(T)
	B = [range(start, n+1, 3) for start in xrange(3)]
	C = B[1] + B[2]
	print "B", B
	print "C", C

	T += "00"
	R = []
	for k in [1,2]:
		offset = 0
		while k+offset <= B[k][-1]:
			R.append(int(T[k+offset:k+offset+3]))
			offset += 3
	R_sorted = radix_sort(R)
	R_prime, is_dup = get_prime(R, R_sorted)
	print "R", R
	print "R_sorted", R_sorted
	print "R_prime", R_prime

	while is_dup:
		SA_R = suffix_array(''.join(map(str, R_prime))) # TODO This only works if all elements of R_prime < 10
		print "SA_R", SA_R
		SA_R_sorted = radix_sort(SA_R)
		print "SA_R_sorted", SA_R_sorted
		R_prime, is_dup = get_prime(SA_R_sorted, SA_R)
		print "R_prime", R_prime
		R_prime = map(lambda x: x-1, R_prime[0:-1]) # This should always cut off the trailing 0
		print "R_prime", R_prime

	rank = [None for _ in xrange(len(T)+1)]
	SC = [0] * len(C)
	for index in xrange(len(C)):
		i = C[index]
		value = R_prime[index]
		rank[i] = value
		SC[value-1] = i
	rank[n+1] = 0
	rank[n+2] = 0
	print "rank", rank
	print "SC", SC

	pairs = [int(T[i] + str(rank[i+1])) for i in B[0]]
	pairs_sorted = radix_sort(pairs)
	print "pairs", pairs
	print "pairs_sorted", pairs_sorted

	SB = map(lambda i: B[0][i-1], get_prime(pairs_sorted, pairs)[0]) # Not sure get_prime will return what I need here, may have to call recursively
	print "SB", SB

	solution = [0] * (n+1)
	SC_index = 0
	SB_index = 0
	for solution_index in xrange(len(solution)):
		i = SC[SC_index]
		j = SB[SB_index]
		if (i-1) % 3 == 0:
			Si = (T[i], rank[i+1])
			Sj = (T[j], rank[j+1])
		else:
			Si = (T[i], T[i+1], rank[i+2])
			Sj = (T[j], T[j+1], rank[j+2])
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
	return solution

print ', '.join(map(str, suffix_array(''.join(map(lambda a: str(alpha_index_map[a]), text)))))
