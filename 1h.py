import sys

alpha = "ATCG"
nucleotide_pair_map = {"A":"T", "T":"A", "C":"G", "G":"C"}

def find_approx_complement_frequent_words(genome, k, d):

	"""
	Runtime => O(|genome| * k^d * d^2))
	@param genome => nucleotide sequence to search through
	@param k => length of substring to search for
	@param d => max number of mismatches allowed
	@return => kmers that maximize count_d(genome + kmer) + count_d(genome + get_complement(kmer))
	"""

        kmer_freq_map = {} # map kmer => frequency
	best_solution = {"frequency": 0, "values": set()}
	for index in xrange(len(genome) - k + 1):
		sequence = genome[index:index+k]
		all_kmers = get_all_diffs(sequence, d)
		for kmer in all_kmers:
			if kmer in kmer_freq_map:
				kmer_freq_map[kmer] += 1
			else:
				kmer_freq_map[kmer] = 1
			comp = get_complement(kmer)
			if comp in kmer_freq_map:
				kmer_freq_map[comp] += 1
			else:
				kmer_freq_map[comp] = 1
			if kmer_freq_map[kmer] == best_solution['frequency']:
				best_solution['values'].add(kmer)
			elif kmer_freq_map[kmer] > best_solution['frequency']:
				best_solution = {"frequency": kmer_freq_map[kmer], "values": set([kmer])}
	return best_solution['values'].union(map(get_complement, best_solution['values']))

def get_all_diffs(sequence, d):

	"""
	Runtime => O(d^2 * |sequence|^d)
	"""

	diffs = set([sequence])
	index_combos = get_combinations(range(len(sequence)), d)
	for combo in index_combos:
		current_combos = set([sequence])
		for index in combo:
			for t in set(current_combos):
				for nuc in alpha:
					current_combos.add(t[0:index] + nuc + t[index+1:])
		diffs = diffs.union(current_combos)
	return diffs

def get_combinations(nums, length):

	"""
	Runtime => O((|nums|-1)^length)
	"""

	pools = [nums] * length
	result = [[]]
	for pool in pools:
		result = [x+[y] for x in result for y in pool]
	return result

def get_complement(pattern):

	"""
	Runtime => O(|pattern|)
	@param pattern => nucleotide sequence
	@return => reverse complement
	"""

	return ''.join(map(lambda x: nucleotide_pair_map[x], pattern)[::-1])

filename = sys.argv[1]
input = [line.split() for line in open(filename, "r")]
genome = input[0][0]
k, d = map(int, input[1])
print ' '.join(find_approx_complement_frequent_words(genome, k, d))


