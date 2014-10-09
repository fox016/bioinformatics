#!/usr/bin/python

class Tree:

	def __init__(self, text):
		self.node_edge_map = {1: []}
		self.node_count = 1
		self.text = text
		for index in xrange(len(text)):
			self._add_string(text[index:])
	
	def trie_matching(self, text):
		best = ""
		for index in xrange(len(text)):
			match = self._prefix_matching(text[index:])
			if len(match) > len(best):
				best = match
		return best

	def _add_string(self, string):
		node = 1
		for index in xrange(len(string)):
			edge = self._get_edge(node, string[index])
			if not edge:
				edge = self._add_edge(node, string[index])
			node = edge[1]

	def _prefix_matching(self, text):
		symbol_index = 0
		match = ""
		node = 1
		while True:
			edge = None if symbol_index >= len(text) else self._get_edge(node, text[symbol_index])
			if edge:
				match += text[symbol_index]
				symbol_index+=1
				node = edge[1]
			else:
				return match
	
	def _get_edge(self, start_node, value):
		for edge in self.node_edge_map[start_node]:
			if edge[2] == value:
				return edge
		return None

	def _add_edge(self, parent_node, value):
		self.node_count+=1
		edge = (parent_node, self.node_count, value)
		self.node_edge_map[parent_node].append(edge)
		self.node_edge_map[self.node_count] = []
		return edge

	def __str__(self):
		rows = []
		for node in xrange(1, self.node_count+1):
			for edge in self.node_edge_map[node]:
				rows.append(' '.join(map(str, edge)))
		return '\n'.join(rows)

text1, text2 = [line[:-1] for line in open("input.txt", "r")]
tree = Tree(text1)
print tree.trie_matching(text2)
