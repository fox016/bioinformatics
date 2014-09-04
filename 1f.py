import sys

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
pattern = input[0][0]
genome = input[1][0]
d = int(input[2][0])
print ' '.join(map(str, find_approx_pattern(pattern, genome, d)))
