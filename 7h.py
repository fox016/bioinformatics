#!/usr/bin/python

class Tree:

	def __init__(self, text, SA, LCP):
		self.current_node = 0
		self.node_count = 1
		self.edge_map = {} # tuple (parent, child) => tuple (index, length)
		self.node_parent_map = [None] # node => parent
		self.text = text
		self._build(text, SA, LCP + [LCP[-1]])
	
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

read = [line[:-1] for line in open("input.txt", "r")]
print Tree(read[0], map(int, read[1].split(", ")), map(int, read[2].split(", ")))
