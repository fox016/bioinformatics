#!/usr/bin/python

DELETE = 0
INSERT = 1
MATCH = 2

INDEL_COST = -5

PROTEIN_INDEX_MAP = {'A': 0, 'C': 1, 'E': 3, 'D': 2, 'G': 5, 'F': 4, 'I': 7, 'H': 6, 'K': 8, 'M': 10, 'L': 9, 'N': 11, 'Q': 13, 'P': 12, 'S': 15, 'R': 14, 'T': 16, 'W': 18, 'V': 17, 'Y': 19}

edge_map = {}

def linear_space_alignment(v, w, matrix, top, bottom, left, right):
        global edge_map
        if left == right:
		while top < bottom:
			first_node = (top, left)
			second_node = (top+1, left)
			edge_map[first_node] = second_node
			top+=1
                return
        if top == bottom:
		while left < right:
			first_node = (top, left)
			second_node = (top, left+1)
			edge_map[first_node] = second_node
			left+=1
                return
        mid_edge = linear_middle_edge(v[top:bottom], w[left:right], matrix)
        first_node = (top+mid_edge[0][0], left+mid_edge[0][1])
        second_node = (top+mid_edge[1][0], left+mid_edge[1][1])
        edge_map[first_node] = second_node
        linear_space_alignment(v, w, matrix, top, first_node[0], left, first_node[1])
        linear_space_alignment(v, w, matrix, second_node[0], bottom, second_node[1], right)

def unwind(v, w, matrix):
        global edge_map
        print max_alignment(v, w, matrix)[0][-1]
        new_v = []
        new_w = []
        node = (0,0)
        while node in edge_map:
                next_node = edge_map[node]
                if next_node[0] == node[0]:
                        new_v.append("-")
                        new_w.append(w[node[1]])
                elif next_node[1] == node[1]:
                        new_v.append(v[node[0]])
                        new_w.append("-")
                else:
                        new_v.append(v[node[0]])
                        new_w.append(w[node[1]])
                node = next_node
        print ''.join(new_v)
        print ''.join(new_w)

def max_alignment(v, w, matrix):
        row = [INDEL_COST * i for i in xrange(len(v)+1)]
        ops = [INSERT for i in xrange(len(v)+1)]
        for j in xrange(1, len(w)+1):
                new_row = [(INDEL_COST * j)] + ([0] * len(v))
                for i in xrange(1, len(row)):
                        new_row[i], ops[i] = max_index([new_row[i-1] + INDEL_COST, row[i] + INDEL_COST, row[i-1] + match_cost(v[i-1], w[j-1], matrix)])
                row = new_row
        return row, ops

def match_cost(p1, p2, matrix):
        return matrix[PROTEIN_INDEX_MAP[p1]][PROTEIN_INDEX_MAP[p2]]

def max_index(nums):
        best = (nums[0], 0)
        for index in xrange(1, len(nums)):
                if nums[index] > best[0]:
                        best = (nums[index], index)
        return best

def linear_middle_edge(v, w, matrix):
        middle = (len(w) / 2) + 1
        source_distances, source_ops = max_alignment(v, w[0:middle], matrix)
        sink_distances, sink_ops = max_alignment(v[::-1], w[middle-1:][::-1], matrix)
        best = (0, source_distances[0] + sink_distances[len(v)], source_ops[0])
        for i in xrange(1, len(v)+1):
                length = source_distances[i] + sink_distances[len(v)+1-i]
                if length > best[1]:
                        best = (i, length, source_ops[i])
        op = best[2]
        if op == DELETE:
                return (best[0]-1, middle), (best[0], middle)
        elif op == INSERT:
                return (best[0], middle-1), (best[0], middle)
        return (best[0]-1, middle-1), (best[0], middle)

matrix = [map(int, line.split()) for line in open("blosum62.txt", "r")]
v, w = [line[:-1] for line in open("input.txt", "r")]
linear_space_alignment(v, w, matrix, 0, len(v), 0, len(w))
unwind(v, w, matrix)
