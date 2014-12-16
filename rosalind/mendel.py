#!/usr/bin/python

def get_probabilities(k, m, n):
	total = float(k + m + n)
	return [(k/total) * ((k-1)/(total-1)), \
		(k/total) * (m/(total-1)) + (m/total) * (k/(total-1)), \
		(k/total) * (n/(total-1)) + (n/total) * (k/(total-1)), \
		(m/total) * ((m-1)/(total-1)), \
		(m/total) * (n/(total-1)) + (n/total) * (m/(total-1)), \
		(n/total) * ((n-1)/(total-1))]

k, m, n = 17, 21, 25
print sum(map(lambda x,y: x*y, get_probabilities(k, m, n), [1.0, 1.0, 1.0, 0.75, 0.50, 0.0]))
