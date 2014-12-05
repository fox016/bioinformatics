import sys

nucleotide_value_map = {"A":1, "T":2, "C":3, "G":4, "N": 5}

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

def get_hash(segment, tens_table):
        hash_num = 0
        for i in xrange(1, len(segment)+1):
                hash_num += (nucleotide_value_map[segment[i-1]] * tens_table[len(segment)-i])
        return hash_num

def hash_genome(genome, k, tens_table):
	kmer_index_map = {}
	for i in xrange(len(genome) - k + 1):
		if i == 0:
			hash_pattern = get_hash(genome[0:k], tens_table)
		else:
			hash_pattern = ((hash_pattern - (nucleotide_value_map[genome[i-1]] * tens_table[k-1])) * 10 + nucleotide_value_map[genome[i-1+k]])
		if hash_pattern in kmer_index_map:
			kmer_index_map[hash_pattern].append(i+1)
		else:
			kmer_index_map[hash_pattern] = [i+1]
	return kmer_index_map

def map_reads(genome, genome_name, reads, k, tens_table):
	kmer_index_map = hash_genome(genome, k, tens_table)
	for read_input in reads:
		read_name, read = read_input
		pos_freq_map = {}
		for i in xrange(len(read) - k + 1):
			if i == 0:
				kmer_hash = get_hash(read[0:k], tens_table)
			else:
				kmer_hash = ((kmer_hash - (nucleotide_value_map[read[i-1]] * tens_table[k-1])) * 10 + nucleotide_value_map[read[i-1+k]])
			if kmer_hash in kmer_index_map:
				for position in kmer_index_map[kmer_hash]:
					if position-i in pos_freq_map:
						pos_freq_map[position-i]+=1
					else:
						pos_freq_map[position-i]=1
		best_pos = (-1, -1)
		for pos in pos_freq_map:
			if pos_freq_map[pos] > best_pos[1]:
				best_pos = (pos, pos_freq_map[pos])
		if best_pos[0] >= 0:
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
tens_table = map(lambda x: pow(10, x), range(k))
map_reads(genome[0][1], genome[0][0], reads, k, tens_table)
