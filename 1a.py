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

genome = "TAAACCCTTTATCATTTATCATGGATACTGGATACTTTATCATGGATACTGGATACTAGTTCTCTTTATCATGATCATGTTAGTTCTCTGGATACTGGATACTGGATACTTTATCATGGATACTTTATCATGATCATGTTAAACCCTGATCATGTTAGTTCTCTAGTTCTCTGATCATGTTTTATCATGGATACTAAACCCTAGTTCTCTTTATCATTTATCATAGTTCTCTAGTTCTCTGATCATGTTTTATCATGATCATGTTGGATACTAGTTCTCTAAACCCTAGTTCTCTGATCATGTTGATCATGTTGGATACTGGATACTGGATACTAAACCCTGGATACTGATCATGTTTTATCATGATCATGTTGGATACTGGATACTGATCATGTTTTATCATAGTTCTCTAGTTCTCTGGATACTAGTTCTCTAAACCCTAAACCCTAAACCCTTTATCATGGATACTGATCATGTTAAACCCTGATCATGTTGGATACTTTATCATTTATCATGATCATGTTAGTTCTCTGGATACTTTATCATGATCATGTTTTATCATTTATCATTTATCATAAACCCTGGATACTAAACCCTAAACCCTGATCATGTTAAACCCTGATCATGTTTTATCATAGTTCTCTTTATCATAAACCCTTTATCATGGATACTGATCATGTTAAACCCTGGATACTGGATACTGGATACTGATCATGTTGGATACTTTATCATAAACCCTTTATCATAGTTCTCTTTATCATAGTTCTCTAAACCCTAGTTCTCTGGATACTGGATACTGGATACTGATCATGTTAGTTCTCTGGATACTAGTTCTCTAGTTCTCTTTATCATTTATCATTTATCATGGATACTGATCATGT"
k = 13
print ' '.join(find_frequent_words(genome, k)['value'])
