# n - number of times sequence should appear
# l - expected length of string
# d - max errors in match

# Get all kmers of given length
def get_combinations(alphabet, length):
	pools = [alphabet] * length
	result = [""]
	for pool in pools:
		result = [x+y for x in result for y in pool]
	return result

# Get all substrings of genome, length from min_len to max_len
# Map substring value to string index (1-based index)
def get_substrs(genome, min_len, max_len):
	substrs = {}
	for length in range(min_len, max_len+1):
		for start_pos in range(len(genome)-length+1):
			substr = genome[start_pos:start_pos+length]
			if substr in substrs:
				substrs[substr].append(start_pos+1)
			else:
				substrs[substr] = [start_pos+1]
	return substrs

# Get the cost of mapping one dna sequence to another
# Return both the cost (int) and path (string)
#	 M, X, I, D => match, mismatch, insert, delete
#  e.g., 3, "1M1I2M1D1M1X1M"
def get_cost(kmer, substr):
	# TODO this is all just for testing now
	if kmer == "ACGTAGC":
		if substr == "AGTCATC":
			return 3, "1M1I2M1D1M1X1M"
		elif substr == "ACGATC":
			return 2, "3M1I1M1X1M"
	return 100, "1M"

# Find a kmer of length l that has n matches with up to d errors in genome
def find_matches(n, l, d, genome):
	all_kmers = get_combinations("ACGT", l)
	all_substrs = get_substrs(genome, l-d, l+d)
	for kmer in all_kmers:
		match_count = 0
		matches = list()
		for substr in all_substrs:
			cost, path = get_cost(kmer, substr)
			if cost >=0 and cost <= d:
				match = {}
				match['pos'] = all_substrs[substr]
				match['kmer'] = kmer
				match['path'] = path
				matches.append(match)
				match_count+=len(match['pos'])
			if match_count == n:
				return matches
	return list()

# Main
if __name__ == "__main__":
	infile = open("trans_in1.txt", "r")
	inputs = map(int, infile.readline().rstrip().split(" "))
	genome = infile.readline().rstrip()
	matches = find_matches(inputs[0], inputs[1], inputs[2], genome)
	if len(matches) == 0:
		print "No matches found"
	else:
		print matches[0]['kmer']
		for match in matches:
			for pos in match['pos']:
				print pos, match['path']
