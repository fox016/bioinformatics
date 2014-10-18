#!/usr/bin/python

class Tree:

	def __init__(self, text, SA, LCP):
		self.current_node = 0
		self.node_count = 1
		self.edge_map = {} # tuple (parent, child) => tuple (index, length)
		self.node_parent_map = [None] # node => parent
		self._build(text, SA, LCP + [0])
	
	def _build(self, text, SA, LCP):
		for index in xrange(len(SA)):
			if LCP[index+1] - LCP[index] <= 0:
				prev_length = self._get_string_length(self.current_node)
				self._add_edge(self.current_node, SA[index]+prev_length, len(text)-SA[index]-prev_length)
			else:
				pass # TODO
	
	def _add_edge(self, parent, index, length):
		child = self.node_count
		self.node_count+=1
		self.edge_map[(parent, child)] = (index, length)
		self.node_parent_map.append(parent)
	
	def _get_string_length(self, node):
		length = 0
		while self.node_parent_map[node] != None:
			parent = self.node_parent_map[node]
			edge = self.edge_map[(parent, node)]
			length += edge[1]
		return length

	def __str__(self):
		return '\n'.join(map(str, self.edge_map.values()))

def build_tree(text, SA, LCP):
	tree = Tree(text, SA, LCP)
	return tree

read = [line[:-1] for line in open("input.txt", "r")]
print build_tree(read[0], map(int, read[1].split(", ")), map(int, read[2].split(", ")))
