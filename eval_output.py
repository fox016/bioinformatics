import sys

filename = sys.argv[1]
contigs = [line[:-1] for line in open(filename, "r")]
lengths = map(len, contigs)
print "Avg", sum(lengths) / float(len(contigs))
print "Max", max(lengths)
print "Count", len(contigs)
