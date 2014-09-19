import sys

values = [57, 71, 87, 97, 99, 101, 103, 113, 114, 115, 128, 129, 131, 137, 147, 156, 163, 186]

"""
def count_peptides_new(mass):
	table = [{"count": 1, "pairs": [], "index": 0}]
	for i in xrange(mass):
		table.append({"count": 0, "pairs": [], "index": i+1})
	for value in values:
		for i in xrange(value, mass+1):
			if table[i-value]['count'] != 0:
				table[i]['count'] += table[i-value]['count']
				table[i]['pairs'].append((i-value,value))
	combos = build_combos(table, mass)
	return sum(map(count_all_unique_orderings, combos))

combo_map = {0: [[]]}
for value in values:
	combo_map[value] = [[value]]

def build_combos(table, index):

	if index in combo_map:
		return combo_map[index]

	pairs = table[index]['pairs']
	combos = []
	for i in xrange(len(pairs)):
		left = build_combos(table, pairs[i][0])
		right = build_combos(table, pairs[i][1])
		for left_list in left:
			for right_list in right:
				combos.append(left_list + right_list)
	
	combo_map[index] = combos
	return combos
"""

def count_peptides(mass):
	table = [{"count": 1, "combos": [[]]}]
	for i in xrange(mass):
		table.append({"count": 0, "combos": []})
	for value in values:
		for i in xrange(value, mass+1):
			if table[i-value]['count'] != 0:
				table[i]['count'] += table[i-value]['count']
				for combo in table[i-value]['combos']:
					table[i]['combos'].append(combo + [value]) # This is the problem! Copying lists is expensive
	return sum(map(count_all_unique_orderings, table[mass]['combos']))

def count_all_unique_orderings(nums):
	freq_counts = get_freq_counts(nums)
	total = len(nums)
	solution = 1
	for freq in freq_counts:
		solution *= count_n_choose_k(total, freq)
		total -= freq
	return solution

def get_freq_counts(nums):
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
	if (k > N) or (N < 0) or (k < 0):
		return 0
	val = 1
	for j in xrange(min(k, N-k)):
		val = (val*(N-j))//(j+1)
	return val

mass = 1359
print count_peptides(mass)
