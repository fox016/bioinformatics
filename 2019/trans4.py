import sys
import itertools

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

# Get all kmers of given length
def get_combinations(alphabet, length):
	pools = [alphabet] * length
	result = [""]
	for pool in pools:
		result = [x+y for x in result for y in pool]
	return result

# n - number of occurrences
# l - length of kmer to return
# d - max number of mismatches
def find_kmer(n, l, d, genome):
	kmer_count_map = {}
	substrs = get_substrs(genome, l, l) # substrings of length l in genome
	replace_values = get_combinations("ACGT", d) # mismatch combination values
	replace_indexes = itertools.permutations("".join(map(lambda x: hex(x)[2:].upper(), range(l))), d) # mismatch combination indexes
	for indexes in replace_indexes:
		for values in replace_values:
			for substr in substrs:
				kmer = substr
				for i in range(d):
					value = values[i]
					index = int(indexes[i], 16)
					kmer = kmer[:index] + value + kmer[index+1:]
				if kmer in kmer_count_map:
					for pos in substrs[substr]:
						kmer_count_map[kmer].add(pos)
				else:
					kmer_count_map[kmer] = set(substrs[substr])
				if len(kmer_count_map[kmer]) >= n:
					print kmer, kmer_count_map[kmer]
					print ""

# Main
if __name__ == "__main__":
	infile = open("in.txt", "r")
	inputs = map(int, infile.readline().rstrip().split(" "))
	genome = infile.readline().rstrip()
	find_kmer(inputs[0], inputs[1], inputs[2], genome)
