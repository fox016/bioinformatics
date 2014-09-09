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

ecoli = ''.join([line for line in open("e_coli.txt", "r")]).replace("\n", "")
print ' '.join(map(str, find_minimum_skew(ecoli)['index']))
