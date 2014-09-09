import sys

values = [57, 71, 87, 97, 99, 101, 103, 113, 114, 115, 128, 129, 131, 137, 147, 156, 163, 186]

def count_peptides(mass):

	"""
	Runtime ?
	@param mass - target peptide mass
	@return count of all linear peptides of mass "mass"
	"""

	table = [{"count": 1, "combos": [[]]}]
	for i in xrange(mass):
		table.append({"count": 0, "combos": []})
	for value in values:
		for i in xrange(value, mass+1):
			if table[i-value]['count'] != 0:
				table[i]['count'] += table[i-value]['count']
				for combo in table[i-value]['combos']:
					table[i]['combos'].append(list(combo) + [value]) # This is the problem! Copying lists is expensive
	return reduce(lambda x,y: x+y, map(count_all_unique_orderings, table[mass]['combos']), 0)

def count_all_unique_orderings(nums):

	"""
	Runtime O(|nums|^2)
	@param nums - list of sorted numbers
	@return count of unique permutations of nums
	"""

	freq_counts = get_freq_counts(nums)
	total = len(nums)
	solution = 1
	for freq in freq_counts:
		solution *= count_n_choose_k(total, freq)
		total -= freq
	return solution

def get_freq_counts(nums):

	"""
	Runtime O(|nums|)
	@param nums - list of sorted numbers
	@return list of how frequently each unique number appears
	"""

	ptr = 0
	freq_counts = []
	count = 1
	for index in xrange(1, len(nums)):
		if nums[ptr] == nums[index]:
			count+=1
		else:
			freq_counts.append(count)
			count = 1
			ptr = index
	freq_counts.append(count)

	return freq_counts

def count_n_choose_k(N, k):

	"""
	Runtime O(N)
	@param N - integer, length of a set
	@param k - integer <= N
	@return length of n_choose_k
	"""

	if (k > N) or (N < 0) or (k < 0):
		return 0
	val = 1
	for j in xrange(min(k, N-k)):
		val = (val*(N-j))//(j+1)
	return val

mass = 1024
print count_peptides(mass)
