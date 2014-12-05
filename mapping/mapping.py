import sys

def read_fasta_file(filename):
	fasta_input = [line[:-1] for line in open(filename, 'r')]
	ext = filename[filename.rfind('.'):]
	if ext == ".fasta":
		reads = []
		for i in xrange(1, len(fasta_input), 2):
			reads.append((fasta_input[i-1][1:], fasta_input[i]))
		return reads
	elif ext == ".fa":
		read_name = fasta_input[0][1:]
		read = ""
		for i in xrange(1, len(fasta_input)):
			read += fasta_input[i].upper()
		return [(read_name, read)]
	else:
		print "File type " + ext + " not supported"
		sys.exit(0)

def hash_genome(genome, k):
	kmer_index_map = {}
	for i in xrange(len(genome) - k + 1):
		kmer = genome[i:i+k]
		if kmer in kmer_index_map:
			kmer_index_map[kmer].append(i+1)
		else:
			kmer_index_map[kmer] = [i+1]
	return kmer_index_map

def map_reads(genome, genome_name, reads, k):
	kmer_index_map = hash_genome(genome, k)
	for read_input in reads:
		read_name, read = read_input
		pos_freq_map = {}
		for i in xrange(len(read) - k + 1):
			read_kmer = read[i:i+k]
			if read_kmer in kmer_index_map:
				for position in kmer_index_map[read_kmer]:
					if position-i in pos_freq_map:
						pos_freq_map[position-i]+=1
					else:
						pos_freq_map[position-i]=1
		best_pos = (-1, -1)
		for pos in pos_freq_map:
			if pos_freq_map[pos] > best_pos[1]:
				best_pos = (pos, pos_freq_map[pos])
		write_sam_line(read_name, genome_name, best_pos[0], len(read), read)

def write_sam_line(read_name, genome_name, genome_position, matches, read):
	line = [read_name, "0", genome_name, str(genome_position), "255", str(matches)+"M", "*", "0", "0", read, "*"]
	print '\t'.join(line)

if len(sys.argv) != 4:
	print "Usage: python mapping.py <genome_fasta_file> <reads_fasta_file> <kmer_size>"
	sys.exit(0)
genome = read_fasta_file(sys.argv[1])
reads = read_fasta_file(sys.argv[2])
k = int(sys.argv[3])
map_reads(genome[0][1], genome[0][0], reads, k)
