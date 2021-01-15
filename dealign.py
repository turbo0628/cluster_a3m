import os,sys

#from tqdm import tqdm

def dealign(filename, no_query_flag=False):
    seqs = []
    with open(filename, "r+") as f:
       lines = f.readlines()
       seq = ""
       title = ""
       for line in lines:
           line=line.strip()
           if line.startswith(">"):
               if title != "" and seq != "":
                   seqs.append((title, seq))
               title = line
               seq = ""
           else:
               seq += line
       # last line
       seqs.append((title, seq))

    print("read seqs num: ", len(seqs))
    (query_title, query_seq) = seqs[0]
    ins_positions = []
    a2m_query_seq=""
    for i, sym in enumerate(query_seq):
        if sym == "-":
            ins_positions.append(i)
        else:
            a2m_query_seq+=sym
    if len(seqs) > 1:
        print("a2m query seq: ", a2m_query_seq)
        seqs[0] = (query_title, a2m_query_seq)

        #for seqid, (title, seq) in tqdm( enumerate(seqs[1:]), "Processing..."):
        for seqid, (title, seq) in enumerate(seqs[1:]):
            fasta_seq=""
            for i, sym in enumerate(seq):
                if sym != "-":
                    fasta_seq += sym.upper()
            seqs[seqid + 1] = (title, fasta_seq)
    if no_query_flag == True:
        return seqs[1:]
    else:
        return seqs

if __name__ == "__main__":
    aln = sys.argv[1]
    outname = sys.argv[2]
    no_query_flag = False
    if len(sys.argv) == 4:
        if sys.argv[3] == "1":
            no_query_flag = True
    seqs = dealign(aln, no_query_flag)
    with open(outname, "w+") as wf:
        for seq in seqs:
            wf.write("{}\n".format(seq[0]))
            wf.write("{}\n".format(seq[1]))
