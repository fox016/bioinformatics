#!/usr/bin/python

class Tree:

	def __init__(self):
		self.node_edge_map = {1: []}
		self.node_count = 1

	def add_string(self, string, node=1):
		if len(string) == 0:
			return
		edge = self._get_edge(node, string[0])
		if not edge:
			edge = self._add_edge(node, string[0])
		self.add_string(string[1:], edge[1])
	
	def trie_matching(self, text):
		return filter(lambda index: self._prefix_matching(text[index:]), xrange(len(text)))

	def _prefix_matching(self, text):
		symbol_index = 0
		node = 1
		while True:
			edge = None if symbol_index >= len(text) else self._get_edge(node, text[symbol_index])
			if edge:
				symbol_index+=1
				node = edge[1]
			elif len(self.node_edge_map[node]) == 0:
				return True
			else:
				return False
	
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

tree = Tree()
read = [line[:-1] for line in open("input.txt", "r")]
map(lambda pattern: tree.add_string(pattern), read[1:])
print ' '.join(map(str, tree.trie_matching(read[0])))
