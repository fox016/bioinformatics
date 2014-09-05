import sys

values = [57, 71, 87, 97, 99, 101, 103, 113, 114, 115, 128, 129, 131, 137, 147, 156, 163, 186]

def count_peptides(mass):
	table = [1] + [0] * mass
	for value in values:
		for i in xrange(value, mass+1):
			table[i] += table[i - value]
	return table

mass = 1024
print count_peptides(mass)
