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

read = [line[0:-1] for line in open("input.txt", "r")]
text = read[0]
k = int(read[1])
profile = map(lambda x: map(float, x.split()), read[2:])
print profile_most_probable_kmer(text, k, profile)
