import sys

alpha = "ATCG"

def find_approx_frequent_words(genome, k, d):

	"""
	Runtime => O(4^k * k * |genome|)
	@param genome => nucleotide sequence to search through
	@param k => length of substring to search for
	@param d => max number of mismatches allowed
	@return => most frequent substrings of length k found in genome with at most d mismatches
	"""

        kmer_freq_map = {} # map kmer => frequency
	all_kmers = get_combinations(alpha, k)
	print "Got combinations"
	best_solution = {"frequency": 0, "values": []}
	for current_index in xrange(len(genome) - k + 1):
		sequence = genome[current_index:current_index+k]
		print sequence, genome
		for kmer in all_kmers:
			if has_d_mismatches(sequence, kmer, d):
				if kmer in kmer_freq_map:
					kmer_freq_map[kmer] += 1
				else:
					kmer_freq_map[kmer] = 1
				if kmer_freq_map[kmer] == best_solution['frequency']:
					best_solution['values'].append(kmer)
				elif kmer_freq_map[kmer] > best_solution['frequency']:
					best_solution = {"frequency": kmer_freq_map[kmer], "values": [kmer]}
	return best_solution

def get_combinations(alphabet, length):
	pools = [alphabet] * length
	result = [""]
	for pool in pools:
		result = [x+y for x in result for y in pool]
	return result

def has_d_mismatches(s1, s2, d):
	count = 0
	for index in xrange(len(s1)):
		if s1[index] != s2[index]:
			count+=1
			if count > d:
				return False
	return True

filename = sys.argv[1]
input = [line.split() for line in open(filename, "r")]
genome = input[0][0]
k, d = map(int, input[1])
print ' '.join(find_approx_frequent_words(genome, k, d)['values'])
