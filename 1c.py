import sys

nucleotide_value_map = {"A":1, "T":2, "C":3, "G":4}

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

def get_hash(segment, tens_table):
        hash = 0
        for i in xrange(1, len(segment)+1):
                hash += (nucleotide_value_map[segment[i-1]] * tens_table[len(segment)-i])
        return hash

filename = sys.argv[1]
input = [line.split() for line in open(filename, "r")]
pattern = input[0][0]
genome = input[1][0]
print ' '.join(map(str, find_pattern(pattern, genome)))
