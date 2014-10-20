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
			print "\nINDEX", index
			print "SA", SA[index], self.text[SA[index]:]
			print "LCP", LCP[index], LCP[index+1]
			print "CURRENT_NODE", self.current_node
			if LCP[index+1] - LCP[index] <= 0:
				prev_length = self._get_string_length(self.current_node)
				print "PREV_LENGTH", prev_length
				print "MAKE_EDGE", self.current_node, self.node_count, SA[index]+prev_length, len(text)-SA[index]-prev_length
				self._add_edge(self.current_node, SA[index]+prev_length, len(text)-SA[index]-prev_length)
				print "REVERSE_CURRENT_NODE", LCP[index]-LCP[index+1]
				self._reverse_current(LCP[index]-LCP[index+1])
			else:
				print "MAKE_EDGE", self.current_node, self.node_count, SA[index]+LCP[index], LCP[index+1] - LCP[index]
				self.current_node = self._add_edge(self.current_node, SA[index]+LCP[index], LCP[index+1] - LCP[index])
				print "MAKE_EDGE", self.current_node, self.node_count, SA[index]+LCP[index+1], len(text)-SA[index]-LCP[index+1]
				self._add_edge(self.current_node, SA[index]+LCP[index+1], len(text)-SA[index]-LCP[index+1])
	
	def _add_edge(self, parent, index, length):
		child = self.node_count
		self.node_count+=1
		self.edge_map[(parent, child)] = (index, length)
		self.node_parent_map.append(parent)
		return child

	def _split_edge(self, edge, end_length):
		str_data = self.edge_map[edge]
		parent = edge[0]
		child = edge[1]
		index = str_data[0]
		length = str_data[1]
		new_node = self.node_count
		self.node_count+=1
		print "MAKE_EDGE_SPLIT", parent, new_node, index, length-end_length
		self.edge_map[(parent, new_node)] = (index, length - end_length)
		print "MAKE_EDGE_SPLIT", new_node, child, index+length-end_length, end_length
		self.edge_map[(new_node, child)] = (index + length - end_length, end_length)
		self.node_parent_map.append(parent)
		self.node_parent_map[child] = new_node
		print "NODE_PARENT_MAP", self.node_parent_map
		print "REMOVE EDGE", edge, str_data
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
		edges = []
		for edge in self.edge_map.keys():
			value = self.edge_map[edge]
			print edge, value
			edges.append(self.text[value[0]:value[0]+value[1]])
		return '\n'.join(edges)

def build_tree(text, SA, LCP):
	tree = Tree(text, SA, LCP)
	return tree

read = [line[:-1] for line in open("input.txt", "r")]
print build_tree(read[0], map(int, read[1].split(", ")), map(int, read[2].split(", ")))
