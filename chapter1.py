import random

"""
-------------------- Global Variables
"""

alpha = "ATCG"
nucleotide_pair_map = {"A":"T", "T":"A", "C":"G", "G":"C"}
nucleotide_value_map = {"A":1, "T":2, "C":3, "G":4}

"""
-------------------- Primary Functions
"""

def find_frequent_words(genome, k):

	"""
	Runtime => O(|genome|)
	@param genome => nucleotide sequence to search through
	@param k => length of substring to search for
	@return => most frequent substrings of length k found in genome
	"""

        sequence_freq_map = {} # map sequence => frequency
	best_solutions = {"frequency":0, "value":[]} # value is array of starting indices
        for current_index in xrange(len(genome) - k + 1):
		sequence = genome[current_index:current_index+k]
		if sequence in sequence_freq_map:
			sequence_freq_map[sequence] += 1
		else:
			sequence_freq_map[sequence] = 1
		if sequence_freq_map[sequence] > best_solutions['frequency']:
			best_solutions = {"frequency": sequence_freq_map[sequence], "value": [current_index]}
		elif sequence_freq_map[sequence] == best_solutions['frequency']:
			best_solutions['value'].append(current_index)
	best_solutions["value"] = map(lambda i: genome[i:i+k], best_solutions["value"]) # value is transformed to array of k-mers
	return best_solutions

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
	best_solution = {"frequency": 0, "values": []}
	for current_index in xrange(len(genome) - k + 1):
		sequence = genome[current_index:current_index+k]
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

def find_approx_complement_frequent_words(genome, k, d):

	"""
	Runtime => O(4^k * k * |genome|)
	@param genome => nucleotide sequence to search through
	@param k => length of substring to search for
	@param d => max number of mismatches allowed
	@return => kmers that maximize count_d(genome + kmer) + count_d(genome + get_complement(kmer))
	"""

        kmer_freq_map = {} # map kmer => frequency
	all_kmers = get_combinations(alpha, k)
	best_solution = {"frequency": 0, "values": []}
	for current_index in xrange(len(genome) - k + 1):
		sequence = genome[current_index:current_index+k]
		for kmer in all_kmers:
			complement = get_complement(kmer)
			if has_d_mismatches(sequence, kmer, d) or has_d_mismatches(sequence, complement, d):
				if kmer in kmer_freq_map:
					kmer_freq_map[kmer] += 1
				else:
					kmer_freq_map[kmer] = 1
				if kmer_freq_map[kmer] == best_solution['frequency']:
					best_solution['values'].append(kmer)
				elif kmer_freq_map[kmer] > best_solution['frequency']:
					best_solution = {"frequency": kmer_freq_map[kmer], "values": [kmer]}
	return best_solution


def get_complement(sequence):

	"""
	Runtime => O(|sequence|)
	@param sequence => nucleotide sequence
	@return => reverse complement
	"""

	return ''.join(map(lambda x: nucleotide_pair_map[x], sequence)[::-1])

def find_pattern(pattern, genome):

	"""
	Runtime => O(|genome|)
	@param pattern => nucleotide pattern to search for
	@param genome => nucleotide sequence to search through
	@return => indexes where pattern is found in genome
	"""

        tens_table = [pow(10, m) for m in xrange(len(pattern))]
        hash_pattern = get_hash(pattern, tens_table)
        index = []
        for current_index in xrange(len(genome) - len(pattern) + 1):
		if current_index == 0:
			current_hash = get_hash(genome[0:len(pattern)], tens_table)
		else:
			current_hash = ((current_hash - (nucleotide_value_map[genome[current_index-1]] * tens_table[len(pattern)-1])) * 10 + nucleotide_value_map[genome[current_index-1+len(pattern)]])
                if current_hash == hash_pattern:
                        index.append(current_index)
        return index

def find_approx_pattern(pattern, genome, d):

	"""
	Runtime => O(|genome| * |pattern|)
	@param pattern => nucleotide pattern to search for
	@param genome => nucleotide sequence to search through
	@param d => max number of mismatches allowed
	@return => indexes where pattern is found in genome with at most d mismatches
	"""

        index = []
        for current_index in xrange(len(genome) - len(pattern) + 1):
		sequence = genome[current_index:current_index+len(pattern)]
		if has_d_mismatches(sequence, pattern, d):
                        index.append(current_index)
        return index

def find_clumps(genome, k, l, t):

	"""
	Runtime => O(|genome| * l)
	@param genome => nucleotide sequence to search through
	@param k => length of substring to search for
	@param l => length of window to search through
	@param t => number of times k-mer should be found in window of length l
	@return => k-mers found t times in any window of length l
	"""

	kmers = set()
	for index in xrange(len(genome) - l + 1):
		window = genome[index:index+l]
		words = find_frequent_words(window, k)
		if words["frequency"] == t:
			kmers.update(words["value"])
	return kmers

def find_clumps_4k(genome, k, l, t):

	"""
	Runtime => O(4^k + k * |genome|) because the book asks for a solution like this
	@param genome => nucleotide sequence to search through
	@param k => length of substring to search for
	@param l => length of window to search through
	@param t => number of times k-mer should be found in window of length l
	@return => k-mers found t times in any window of length l
	"""

	kmer_index_map = {} # map k-mer => indexes found in genome
	kmers = get_combinations(alpha, k)
	for kmer in kmers:
		kmer_index_map[kmer] = []
	for index in xrange(len(genome) - k + 1):
		current = genome[index:index+k]
		kmer_index_map[current].append(index)

	result_set = set()
	for kmer in kmers:
		if kmer in result_set:
			continue
		indexes = kmer_index_map[kmer]
		if len(indexes) < t:
			continue
		else:
			for i in xrange(len(indexes) - t + 1):
				if(indexes[i+t-1] - indexes[i]) <= l:
					result_set.add(kmer)
					break
	return result_set

def find_minimum_skew(genome):

	"""
	Runtime => O(|genome|)
	@param genome => nucleotide sequence to search through
	@return => value and index(es) of minimum skew
	"""

	skew = 0
	index = 0
	minimum = {"value": 0, "index": [0]}
	for index in xrange(1, len(genome)):
		if genome[index] == "C":	
			skew -= 1
		elif genome[index] == "G":
			skew += 1
		if skew < minimum['value']:
			minimum['value'] = skew
			minimum['index'] = [index+1]
		elif skew == minimum['value']:
			minimum['index'].append(index+1)
	return minimum

"""
-------------------- Helper Functions
"""

def get_hash(segment, tens_table):
        hash = 0
        for i in xrange(1, len(segment)+1):
                hash += (nucleotide_value_map[segment[i-1]] * tens_table[len(segment)-i])
        return hash

def has_d_mismatches(s1, s2, d):
	count = 0
	for index in xrange(len(s1)):
		if s1[index] != s2[index]:
			count+=1
			if count > d:
				return False
	return True

def generate_genome(length):
	genome = ""
	for i in xrange(length):
		genome += random.choice(alpha)
	return genome

def get_combinations(alphabet, length):
	pools = [alphabet] * length
	result = [""]
	for pool in pools:
		result = [x+y for x in result for y in pool]
	return result

"""
-------------------- Script
"""

cholera = "ATCAATGATCAACGTAAGCTTCTAAGCATGATCAAGGTGCTCACACAGTTTATCCACAACCTGAGTGGATGACATCAAGATAGGTCGTTGTATCTCCTTCCTCTCGTACTCTCATGACCACGGAAAGATGATCAAGAGAGGATGATTTCTTGGCCATATCGCAATGAATACTTGTGACTTGTGCTTCCAATTGACATCTTCAGCGCCATATTGCGCTGGCCAAGGTGACGGAGCGGGATTACGAAAGCATGATCATGGCTGTTGTTCTGTTTATCTTGTTTTGACTGAGACTTGTTAGGATAGACGGTTTTTCATCACTGACTAGCCAAAGCCTTACTCTGCCTGACATGCACCGTAAATTGATAATGAATTTACATGCTTCCGCGACGATTTACCTCTTGATCATCGATCCGATTGAAGATCTTCAATTGTTAATTCTCTTGCCTCGACTCATAGCCATGATGAGCTCTTGATCATGTTTCCTTAACCCTCTATTTTTTACGGAAGAATGATCAAGCTGCTGCTCTTGATCATCGTTTC"
clump_genome = "GATCAGCATAAGGGTCCCTGCAATGCATGACAAGCCTGCAGTTGTTTTACATCGATCGATCGATCG"
approx_genome = "AACAAGCATAAACATTAAAGAG"
random = generate_genome(100000)

print "\nfind_frequent_words"
print find_frequent_words(cholera, 9)
print find_frequent_words(random, 9)

print "\nfind_pattern"
print find_pattern("ATGATCAAG", cholera)
print find_pattern("ATGATCAAG", random)

print "\nfind_clumps"
print find_clumps(clump_genome, 4, 25, 3)
print find_clumps_4k(clump_genome, 4, 25, 3)

print "\nfind_minimum_skew"
print find_minimum_skew(cholera)
print find_minimum_skew(random)

print "\nfind_approx_pattern"
print find_approx_pattern("AAAAA", approx_genome, 1)
print find_approx_pattern("ATGATCAAG", cholera, 1)
print find_approx_pattern("ATGATCAAG", random, 1)

print "\nfind_approx_frequent_words"
print find_approx_frequent_words(approx_genome, 5, 1)

print "\nfind_approx_complement_frequent_words"
print find_approx_complement_frequent_words(approx_genome, 5, 1)
