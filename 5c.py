DEL = 1
IN = 2
MATCH = 3

def lcs(v, w):
	s = []
	ops = []
	for i in xrange(len(v)+1):
		s.append([0] * (len(w)+1))
		ops.append([0] * (len(w)+1))
	for i in xrange(1, len(v)+1):
		for j in xrange(1, len(w)+1):
			if v[i] == w[j]:
				s[i][j] = max(s[i-1][j], s[i][j-1], s[i-1][j-1]+1)
			else:
				s[i][j] = max(s[i-1][j], s[i][j-1])

read = [line[:-1] for line in open("input.txt", "r")]
longest_subsequence(read[0], read[1])
