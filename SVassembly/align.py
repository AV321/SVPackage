#"/mnt/ix2/Sandbox/avitko/170621_SV_phasing/A032_contig_eval/assemblyFinal2.fasta.gz"
#'alignment_test.txt'

def mappyAlign(infile, outfile):
    import mappy as mp
    
    a = mp.Aligner("/mnt/ix1/Resources/10X_resources/refdata-b37-2.1.0/fasta/genome.fa")

    if not a: raise Exception("ERROR: failed to load/build index")

    outfile = open(outfile, 'w')

    outfile.write("read\tchr\tpos\tr_st\tr_en\tq_st\tq_en\tcigstr\tcigtup\n")

    for name, seq, qual in mp.fastx_read(infile): # read a fasta/q sequence

        for hit in a.map(seq): # traverse alignments ##CORE DUMPED### on aji, but fine on tamago
            if ((hit.ctg).isdigit()):
                outfile.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(name, hit.ctg, hit.r_st, hit.r_st, hit.r_en, hit.q_st, hit.q_en, hit.cigar_str, hit.cigar))

    outfile.close()
