# n - number of times sequence should appear
# l - expected length of string
# d - max errors in match

import sys

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

# Build DP table to match substr to kmer
# Get the cost of mapping one dna sequence to another
# Return both the cost (int) and path (string)
#	 M, X, I, D => match, mismatch, insert, delete
#  e.g., 3, "1M1I2M1D1M1X1M"
def build_cost_table(kmer, substr):
	width = len(substr) + 1
	height = len(kmer) + 1
	table = [[(0, 'N') for x in range(width)] for y in range(height)]
	for x in range(width):
		table[0][x] = (x, 'D')
	for y in range(height):
		table[y][0] = (y, 'I')
	for x in range(1, width):
		for y in range(1, height):
			left = (table[y][x-1][0]+1, 'D')
			down = (table[y-1][x][0]+1, 'I')
			if substr[x-1] == kmer[y-1]:
				diag = (table[y-1][x-1][0], 'M')
			else:
				diag = (table[y-1][x-1][0]+1, 'X')
			if diag[0] <= down[0] and diag[0] <= left[0]:
				table[y][x] = diag
			elif left[0] <= down[0] and left[0] <= diag[0]:
				table[y][x] = left
			else:
				table[y][x] = down
	return table

# Get path from DP table
def get_path(table, width, height):
	y = height-1
	x = width-1
	path = ""
	while y != 0 or x != 0:
		pos = table[y][x]
		path += pos[1]
		if pos[1] == "M" or pos[1] == "X":
			y-=1
			x-=1
		elif pos[1] == "I":
			y-=1
		elif pos[1] == "D":
			x-=1
	path = path[::-1]
	return path

# Compress a path string
#  e.g. "MMXMDDMMM" => "2M1X1M2D3M"
def compress_path(path):
	new_path = ""
	prev_char = path[0]
	count = 1
	for pos in xrange(1, len(path)):
		char = path[pos]
		if char == prev_char:
			count+=1
		else:
			new_path += str(count) + prev_char
			count = 1
		prev_char = char
	new_path += str(count) + prev_char
	return new_path

# Find a kmer of length l that has n matches with up to d errors in genome
def find_matches(n, l, d, genome):
	print "getting combos..."
	all_kmers = get_combinations("ACGT", l)
	print "getting substrings..."
	all_substrs = get_substrs(genome, l-d, l+d)
	print "getting costs and paths..."
	for kmer in all_kmers:
		match_count = 0
		matches = list()
		for substr in all_substrs:
			table = build_cost_table(kmer, substr)
			cost = table[len(kmer)][len(substr)][0]
			if cost >=0 and cost <= d:
				match = {}
				match['pos'] = all_substrs[substr]
				match['kmer'] = kmer
				match['path'] = compress_path(get_path(table, len(substr)+1, len(kmer)+1))
				matches.append(match)
				match_count+=len(match['pos'])
			if match_count == n:
				print kmer
				for match in matches:
					for pos in match['pos']:
						print pos, match['path']
				# return matches
	return list()

# Main
if __name__ == "__main__":
	infile = open("trans_in4.txt", "r")
	inputs = map(int, infile.readline().rstrip().split(" "))
	genome = infile.readline().rstrip()
	matches = find_matches(inputs[0], inputs[1], inputs[2], genome)
	"""
	if len(matches) == 0:
		print "No matches found"
	else:
		print matches[0]['kmer']
		for match in matches:
			for pos in match['pos']:
				print pos, match['path']
	"""
