val_index_map = {"A": 0, "C": 1, "G": 2, "T": 3}

def profile_most_probable_kmer(text, k, profile):
	best = {"kmer": "", "prob": 0}
	for index in xrange(len(text) - k + 1):
		kmer = text[index:index+k]
		prob = get_probability(kmer, profile)
		if prob > best['prob']:
			best['kmer'] = kmer
			best['prob'] = prob
	return best['kmer']

def get_probability(kmer, profile):
	return reduce(lambda x, y: x * y, map(lambda index: profile[val_index_map[kmer[index]]][index], xrange(len(kmer))), 1)

text = "ACGGGGATTACCTCGGGGATTTCC"
k = 12
profile = [[0.2, 0.2, 0.0, 0.0, 0.0, 0.0, 0.9, 0.1, 0.1, 0.1, 0.3, 0.0],
		[0.1, 0.6, 0.0, 0.0, 0.0, 0.0, 0.0, 0.4, 0.1, 0.2, 0.4, 0.6],
		[0.0, 0.0, 1.0, 1.0, 0.9, 0.9, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0],
		[0.7, 0.2, 0.0, 0.0, 0.1, 0.1, 0.0, 0.5, 0.8, 0.7, 0.3, 0.4]]
print profile_most_probable_kmer(text, k, profile)
