#!usr/bin/python

import sys
import pysam

samfile = pysam.Samfile(sys.argv[1])
for pile_column in samfile.pileup():
	print ("%s,%s" % (pile_column.pos, pile_column.n))
