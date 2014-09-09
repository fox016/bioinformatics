import sys

alpha = "ATCG"

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

def get_combinations(alphabet, length):
	pools = [alphabet] * length
	result = [""]
	for pool in pools:
		result = [x+y for x in result for y in pool]
	return result

"""
filename = sys.argv[1]
input = [line.split() for line in open(filename, "r")]
genome = input[0][0]
k, l, t = map(int, input[1])
print ' '.join(map(str, find_clumps_4k(genome, k, l, t)))
"""

ecoli = ''.join([line for line in open("e_coli.txt", "r")]).replace("\n", "")
ecoli = ecoli[3800000:4100000]
k = 9
l = 1000
t = 5
print ' '.join(map(str, find_clumps_4k(ecoli, k, l, t)))
