#!/usr/bin/python
counts = map(int, [line.split() for line in open("input.txt", "r")][0])
print sum(map(lambda x,y: x*y, map(lambda c: c*2, counts), [1.0, 1.0, 1.0, 0.75, 0.50, 0.0]))
