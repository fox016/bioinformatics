#!/usr/bin/python

def change_problem(amount, values):
	table = [float("inf")] * (amount + 1)
	for value in values:
		for index in xrange(value, len(table)):
			if index % value == 0:
				table[index] = index / value
			else:
				table[index] = min(table[index], table[index-value]+1)
	print table
	return table[amount]

read = [line[:-1] for line in open("input.txt", "r")]
amount = int(read[0])
values = map(int, read[1].split(','))
print change_problem(amount, values)
