#!/usr/bin/python

class Tree:

	def __init__(self, text, SA, LCP):
		self.current_node = 0
		self.node_count = 1
		self.edge_map = {} # tuple (parent, child) => tuple (index, length)
		self.node_parent_map = [None] # node => parent
		self.text = text
		self._build(text, SA, LCP + [LCP[-1]])

	def get_longest_repeat(self):
		best = (float("-inf"), float("-inf"))
		for key in self.edge_map.keys():
			str_data = self.edge_map[key]
			if str_data[0] + str_data[1] < len(self.text):
				if str_data[1] > best[1]:
					best = (key, str_data[1])
		current_node = best[0][1]
		repeat = ""
		while current_node:
			parent = self.node_parent_map[current_node]
			current_edge = (parent, current_node)
			current_data = self.edge_map[current_edge]
			repeat = self.text[current_data[0]:current_data[0]+current_data[1]] + repeat
			current_node = parent
		return repeat
	
	def _build(self, text, SA, LCP):
		for index in xrange(len(SA)):
			if LCP[index+1] - LCP[index] <= 0:
				prev_length = self._get_string_length(self.current_node)
				self._add_edge(self.current_node, SA[index]+prev_length, len(text)-SA[index]-prev_length)
				self._reverse_current(LCP[index]-LCP[index+1])
			else:
				self.current_node = self._add_edge(self.current_node, SA[index]+LCP[index], LCP[index+1] - LCP[index])
				self._add_edge(self.current_node, SA[index]+LCP[index+1], len(text)-SA[index]-LCP[index+1])
	
	def _add_edge(self, parent, index, length):
		child = self.node_count
		self.node_count+=1
		self.edge_map[(parent, child)] = (index, length)
		self.node_parent_map.append(parent)
		return child

	def _split_edge(self, edge, start_length):
		str_data = self.edge_map[edge]
		parent = edge[0]
		child = edge[1]
		index = str_data[0]
		length = str_data[1]
		new_node = self.node_count
		self.node_count+=1
		self.edge_map[(parent, new_node)] = (index, start_length)
		self.edge_map[(new_node, child)] = (index + start_length, length - start_length)
		self.node_parent_map.append(parent)
		self.node_parent_map[child] = new_node
		self.edge_map.pop(edge)
		return new_node
	
	def _get_string_length(self, node):
		length = 0
		while self.node_parent_map[node] != None:
			parent = self.node_parent_map[node]
			edge = self.edge_map[(parent, node)]
			length += edge[1]
			node = parent
		return length

	def _reverse_current(self, reverse_length):
		length = 0
		while reverse_length > length:
			parent = self.node_parent_map[self.current_node]
			edge = (parent, self.current_node)
			str_data = self.edge_map[edge]
			length += str_data[1]
			if length > reverse_length:
				self.current_node = self._split_edge(edge, length - reverse_length)
			else:
				self.current_node = parent

	def __str__(self):
		return '\n'.join(self.text[value[0]:value[0]+value[1]] for value in self.edge_map.values())


text = "ATATCGTTTTATCGTT"
alpha = "$ACGT"
alpha_index_map = {
	"$": 0, 
	"A": 1,
	"C": 2,
	"G": 3,
	"T": 4
}

def get_prime(list_of_tuples, sorted_list):
	list_map = {}
	duplicates = False
	for index in xrange(len(sorted_list)):
		element = sorted_list[index]
		if element in list_map:
			duplicates = True
		list_map[element] = index
	ranks = []
	for element in list_of_tuples:
		ranks.append(list_map[element]+1)
	return ranks, duplicates

def compare_tuple(t1, t2):
	for index in xrange(len(t1)):
		if t1[index] < t2[index]:
			return -1
		if t1[index] > t2[index]:
			return 1
	return 0
 
def suffix_array(T):
	n = len(T)
	B = [range(start, n+1, 3) for start in xrange(3)]
	C = B[1] + B[2]
	T += [0,0]
	R = []
	for k in [1,2]:
		offset = 0
		while k+offset <= B[k][-1]:
			R.append(tuple(T[k+offset:k+offset+3]))
			offset += 3
	R_sorted = sorted(R)
	R_prime, is_dup = get_prime(R, R_sorted)
	while is_dup:
		SA_R = suffix_array(R_prime)
		SA_R_sorted = sorted(SA_R)
		R_prime, is_dup = get_prime(SA_R_sorted, SA_R)
		R_prime = map(lambda x: x-1, R_prime[0:-1])
	rank = [None for _ in xrange(len(T)+1)]
	SC = [0] * len(C)
	for index in xrange(len(C)):
		i = C[index]
		value = R_prime[index]
		rank[i] = value
		SC[value-1] = i
	rank[n+1] = 0
	rank[n+2] = 0
	pairs = [(T[i], rank[i+1]) for i in B[0]]
	pairs_sorted = sorted(pairs)
	SB = map(lambda i: B[0][i-1], get_prime(pairs_sorted, pairs)[0])
	solution = [0] * (n+1)
	SC_index = 0
	SB_index = 0
	for solution_index in xrange(len(solution)):
		i = SC[SC_index]
		j = SB[SB_index]
		if (i-1) % 3 == 0:
			Si = (T[i], rank[i+1])
			Sj = (T[j], rank[j+1])
		else:
			Si = (T[i], T[i+1], rank[i+2])
			Sj = (T[j], T[j+1], rank[j+2])
		if compare_tuple(Si, Sj) < 0:
			solution[solution_index] = i
			SC_index+=1
			if SC_index >= len(SC):
				return solution[0:solution_index+1] + SB[SB_index:]
		else:
			solution[solution_index] = j
			SB_index+=1
			if SB_index >= len(SB):
				return solution[0:solution_index+1] + SC[SC_index:]
	return solution

def count_same(s1, s2):
	count = 0
	for index in xrange(min(len(s1),len(s2))):
		if s1[index] == s2[index]:
			count+=1
		else:
			return count
	return count

def lcp_array(SA, text):
	lcp = [0] * len(SA)
	lcp[0] = 0
	for index in xrange(1, len(SA)):
		lcp[index] = count_same(text[SA[index-1]:], text[SA[index]:])
	return lcp

SA = suffix_array(map(lambda a: alpha_index_map[a], text))
LCP = lcp_array(SA, text+"$")
print Tree(text+"$", SA, LCP).get_longest_repeat()
