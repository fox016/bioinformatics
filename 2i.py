
def turnpike(delta_a):

	length = delta_a.count(0)
	a = [-1] * length
	a[0] = 0
	a[-1] = delta_a[-1]

	index_possible_value_map = {}
	for index in xrange(1, length-1):
		index_possible_value_map[index] = range(index, a[-1]-(length-index-1)+1)
	print index_possible_value_map

	"""
	value_lists = []
	for index in xrange(1, length-1):
		value_lists.append(index_possible_value_map[index])
	combos = get_combinations(value_lists) # O(1350^140) => NOT GOOD

	for combo in combos:
		current = [a[0]] + combo + [a[-1]]
		if get_delta(current) == delta_a:
			return current
	"""

	return a

def get_delta(a):
	a_inv = map(lambda x: x * -1, a)
	return sorted([a1 + a2 for a1 in a for a2 in a_inv])

"""
def get_combinations(list_of_lists):
	pools = list_of_lists
	result = [[]]
	for pool in pools:
		result = [x+[y] for x in result for y in pool]
	return result
"""

delta_a = [map(int, line.split()) for line in open("input.txt", "r")][0]
print ' '.join(map(str, turnpike(delta_a)))
