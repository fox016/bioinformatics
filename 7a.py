
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
	
	def _get_edge(self, start_node, value):
		if start_node not in self.node_edge_map:
			return None
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
for pattern in [line[:-1] for line in open("input.txt", "r")]:
	tree.add_string(pattern)
print tree
