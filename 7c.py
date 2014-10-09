#!/usr/bin/python

class Tree:

	def __init__(self, text):
		self.node_child_map = {1: []}
		self.node_parent_map = {1: None}
		self.node_level_map = {1: 0}
		self.node_index = 1
		self.node_leaf_map = {}
		self.leaf_count = 0
		text = text + "$"
		for index in xrange(len(text)):
			self._add_string(text[index:])
	
	def longest_repeat(self):
		node = self._find_lowest_branching_node()
		pattern = []
		while True:
			edge = self.node_parent_map[node]
			if not edge:
				break
			pattern.append(edge['value'])
			node = edge['parent']
		return ''.join(pattern[::-1])
	
	def _find_lowest_branching_node(self):
		best = (1, 0)
		for node in self.node_level_map:
			if len(self.node_child_map[node]) > 1:
				level = self.node_level_map[node]
				if level > best[1]:
					best = (node, level)
		return best[0]

	def _add_string(self, string):
		node = 1
		for index in xrange(len(string)):
			edge = self._get_edge(node, string[index])
			if not edge:
				edge = self._add_edge(node, string[index])
			node = edge["child"]
	
	def _get_edge(self, start_node, value):
		for edge in self.node_child_map[start_node]:
			if edge['value'] == value:
				return edge
		return None

	def _add_edge(self, parent_node, value):
		self.node_index+=1
		edge = {"parent": parent_node, "child": self.node_index, "value": value}
		self.node_child_map[parent_node].append(edge)
		self.node_child_map[self.node_index] = []
		self.node_parent_map[self.node_index] = edge
		self.node_level_map[self.node_index] = self.node_level_map[parent_node] + 1
		if value == "$":
			self.node_leaf_map[self.node_index] = self.leaf_count
			self.leaf_count+=1
		return edge

	def __str__(self):
		rows = []
		for node in self.node_child_map.keys():
			for edge in self.node_child_map[node]:
				rows.append(' '.join(map(str, [edge['parent'], edge['child'], edge['value']])))
		return '\n'.join(rows)

text = [line[:-1] for line in open("input.txt", "r")][0]
tree = Tree(text)
print tree.longest_repeat()
