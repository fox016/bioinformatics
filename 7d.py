#!/usr/bin/python

class Tree:

	def __init__(self, text):
		self.node_edge_map = {1: []}
		self.node_index = 1
		self.node_leaf_map = {}
		self.leaf_count = 0
		self.text = text
		for index in xrange(len(text)):
			self._add_string(text[index:], index)
		self._compress_paths(1, None)
	
	def _compress_paths(self, node, prev_edge):
		edges = self.node_edge_map[node]
		if len(edges) == 0:
			return
		if len(edges) == 1 and prev_edge:
			new_edge = self._combine_edges(prev_edge, edges[0])
			self._compress_paths(new_edge['child'], new_edge)
			return
		for edge in edges:
			self._compress_paths(edge['child'], edge)
	
	def _combine_edges(self, prev_edge, edge):
		new_edge = {"parent": prev_edge['parent'], "child": edge['child'], "index": prev_edge['index'], "length": prev_edge['length'] + edge['length']}
		self.node_edge_map.pop(edge['parent'])
		edge_list = self.node_edge_map[prev_edge['parent']]
		for index in xrange(len(edge_list)):
			if edge_list[index]['child'] == edge['parent']:
				edge_list[index] = new_edge
				break
		return new_edge

	def _add_string(self, string, offset=0):
		node = 1
		for index in xrange(len(string)):
			edge = self._get_edge(node, index+offset)
			if not edge:
				edge = self._add_edge(node, index+offset)
			node = edge["child"]
	
	def _get_edge(self, start_node, index):
		for edge in self.node_edge_map[start_node]:
			if self.text[edge["index"]] == self.text[index]:
				return edge
		return None

	def _add_edge(self, parent_node, index):
		self.node_index+=1
		edge = {"parent": parent_node, "child": self.node_index, "index": index, "length": 1}
		self.node_edge_map[parent_node].append(edge)
		self.node_edge_map[self.node_index] = []
		if self.text[index] == "$":
			self.node_leaf_map[self.node_index] = self.leaf_count
			self.leaf_count+=1
		return edge

	def __str__(self):
		rows = []
		for node in xrange(1, self.node_index+1):
			if node in self.node_edge_map:
				for edge in self.node_edge_map[node]:
					rows.append(self.text[edge['index']:edge['index']+edge['length']])
		return '\n'.join(rows)

text = [line[:-1] for line in open("input.txt", "r")][0]
tree = Tree(text)
print tree
