alpha = "ACTG"

def motif_enumeration(dna_list, k, d):
	solution = set()
	for kmer in get_kmers(dna_list, k):
		for pattern in get_diffs(kmer, d):
			if in_all_dna(dna_list, get_diffs(pattern, d)):
				solution.add(pattern)
	return solution

def get_kmers(dna_list, k):
	kmers = set()
	for dna in dna_list:
		for index in xrange(len(dna)-k+1):
			kmers.add(dna[index:index+k])
	return kmers

def get_diffs(kmer, d):
	diffs = set([kmer])
	index_combos = get_combinations(range(len(kmer)), d)
	for combo in index_combos:
		current_combos = set([kmer])
		for index in combo:
			for t in set(current_combos):
				for nuc in alpha:
					current_combos.add(t[0:index] + nuc + t[index+1:])
		diffs = diffs.union(current_combos)
	return diffs

def get_combinations(nums, length):
	pools = [nums] * length
	result = [[]]
	for pool in pools:
		result = [x+[y] for x in result for y in pool]
	return result

def in_all_dna(dna_list, diffs):
	for dna in dna_list:
		has = False
		for diff in diffs:
			if diff in dna:
				has = True
		if not has:
			return False
	return True

input = [line.split() for line in open("input.txt", "r")]
k, d = map(int, input[0])
dna_list = map(lambda a: a[0], input[1:])
print ' '.join(motif_enumeration(dna_list, k, d))
