#!/usr/bin/python

def greedy_sorting(P):
	for k in xrange(len(P)):
		if P[k] != k+1:
			index = find_index(P, k+1)
			P = P[0:k] + map(lambda x: x * -1, P[k:index+1][::-1]) + P[index+1:]
			display(P)
			if P[k] < 0:
				P = P[0:k] + map(lambda x: x * -1, P[k:k+1]) + P[k+1:]
				display(P)

def find_index(array, element):
	element = abs(element)
	for index in xrange(len(array)):
		if abs(array[index]) == element:
			return index
	raise ValueError("Value not found")

def display(array):
	print "(" + ' '.join(map(lambda n: "+"+str(n) if n > 0 else str(n), array)) + ")"

data = [line[:-1] for line in open("input.txt", "r")][0]
greedy_sorting(map(int, data[1:-1].split()))
