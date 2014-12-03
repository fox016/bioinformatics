import sys

def read_fasta_file(filename):
	fasta_input = [line[:-1] for line in open(filename, 'r')]
	reads = [] 
	for i in xrange(1, len(fasta_input), 2):
		reads.append((fasta_input[i-1][1:], fasta_input[i]))
	return reads

def hash_genome(genome, k):
	kmer_index_map = {}
	for i in xrange(len(genome) - k + 1):
		kmer = genome[i:i+k]
		if kmer in kmer_index_map:
			kmer_index_map[kmer].append(i+1)
		else:
			kmer_index_map[kmer] = [i+1]
	return kmer_index_map

def map_reads(genome, genome_name, reads, k, d):
	kmer_index_map = hash_genome(genome, k)
	for read_input in reads:
		read_name, read = read_input
		if read in kmer_index_map:
			index_list = kmer_index_map[read]
			write_sam_line(read_name, genome_name, index_list[0], len(read), read)

def write_sam_line(read_name, genome_name, genome_position, matches, read):
	line = [read_name, "0", genome_name, str(genome_position), "255", str(matches)+"M", "*", "0", "0", read, "*"]
	print '\t'.join(line)

if len(sys.argv) != 5:
	print "Usage: python mapping.py <genome_fasta_file> <reads_fasta_file> <kmer_size> <errors_tolerated>"
	sys.exit(0)
genome = read_fasta_file(sys.argv[1])
reads = read_fasta_file(sys.argv[2])
k = int(sys.argv[3])
d = int(sys.argv[4])
map_reads(genome[0][1], genome[0][0], reads, k, d)
