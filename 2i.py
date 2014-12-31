#!/usr/bin/python

def turnpike(delta_a):

	length = delta_a.count(0)
	a = [-1] * length
	a[0] = 0

	delta_a = filter(lambda x: x > 0, delta_a)

	a[-1] = delta_a[-1]
	delta_a = delta_a[:-1]

	a[-2] = delta_a[-1]
	delta_a = delta_a[:-1]
	delta_a.remove(a[-1] - a[-2])

	return turnpike_helper(delta_a, a)

def turnpike_helper(d, x):

	if len(d) == 0:
		return x

	high_num = d[-1]
	for index in xrange(len(x)):
		if x[index] == -1:
			low_index = index
			break
	for index in reversed(xrange(len(x))):
		if x[index] == -1:
			high_index = index
			break
	
	d1 = list(d)
	x1 = list(x)
	x1[high_index] = high_num
	s1 = None
	if(is_valid(x1, d1, high_index)):
		s1 = turnpike_helper(d1, x1)
	
	d2 = list(d)
	x2 = list(x)
	x2[low_index] = x2[-1] - high_num
	s2 = None
	if(is_valid(x2, d2, low_index)):
		s2 = turnpike_helper(d2, x2)

	if s1 != None:
		return s1
	return s2

def is_valid(new_x, new_d, new_index):
	for index in xrange(len(new_x)):
		if index == new_index or new_x[index] == -1:
			continue
		try:
			new_d.remove(abs(new_x[index]-new_x[new_index]))
		except ValueError:
			return False
	return True

def get_delta(a):
	a_inv = map(lambda x: x * -1, a)
	return sorted([a1 + a2 for a1 in a for a2 in a_inv])

d = [map(int, line.split()) for line in open("input1.txt", "r")][0]
a = turnpike(d)
print ' '.join(map(str, a))
