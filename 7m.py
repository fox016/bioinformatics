#!/usr/bin/python

def get_prime(list_of_tuples, sorted_list):
	list_map = {}
	duplicates = False
	for index in xrange(len(sorted_list)):
		element = sorted_list[index]
		if element in list_map:
			duplicates = True
		list_map[element] = index
	ranks = []
	for element in list_of_tuples:
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
	n = len(T)
	B = [range(start, n+1, 3) for start in xrange(3)]
	C = B[1] + B[2]
	T += [0,0]
	R = []
	for k in [1,2]:
		offset = 0
		while k+offset <= B[k][-1]:
			R.append(tuple(T[k+offset:k+offset+3]))
			offset += 3
	R_sorted = sorted(R)
	R_prime, is_dup = get_prime(R, R_sorted)
	while is_dup:
		SA_R = suffix_array(R_prime)
		SA_R_sorted = sorted(SA_R)
		R_prime, is_dup = get_prime(SA_R_sorted, SA_R)
		R_prime = map(lambda x: x-1, R_prime[0:-1])
	rank = [None for _ in xrange(len(T)+1)]
	SC = [0] * len(C)
	for index in xrange(len(C)):
		i = C[index]
		value = R_prime[index]
		rank[i] = value
		SC[value-1] = i
	rank[n+1] = 0
	rank[n+2] = 0
	pairs = [(T[i], rank[i+1]) for i in B[0]]
	pairs_sorted = sorted(pairs)
	SB = map(lambda i: B[0][i-1], get_prime(pairs_sorted, pairs)[0])
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

text, k = [line[:-1] for line in open("/Users/Admin/Downloads/rosalind_7m.txt", "r")]
k = int(k)
SA = suffix_array(map(ord, text[:-1]))
for index in xrange(len(SA)):
	if SA[index] % k == 0:
		print str(index) + "," + str(SA[index])
