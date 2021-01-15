import sys


def load_tsv(tsv_path):
    seqid_dict = {}
    with open(tsv_path, "r+") as f:
        lines = f.readlines()
    for line in lines:
        cluster, seqid = line.strip().split()
        if cluster in seqid_dict.keys():
            seqid_dict[cluster].append(seqid)
        else:
            seqid_dict[cluster] = [seqid]
    return seqid_dict


def extract_seqs_in_cluster(seqs, cluster_seqids, reserve_query=True):
    if reserve_query:
        extract_seqs = [seqs[0]]
    else:
        extract_seqs = []
    for (title, seq) in seqs[1:]:
        #print(title)
        #title=title.strip()
        if title[1:] in cluster_seqids:
            extract_seqs.append((title, seq))
    return extract_seqs


def read_seqs(seq_file):
    seqs = []
    with open(seq_file, "r+") as f:
        lines = f.readlines()
        seq = ""
        title = ""
        for line in lines:
            line = line.strip()
            if line.startswith(">"):
                if title != "" and seq != "":
                    seqs.append((title, seq))
                title = line
                seq = ""
            else:
                seq += line
        # last line
        seqs.append((title, seq))
    return seqs


def write_seqs(seqs, out_path):
    with open(out_path, "w+") as wf:
        for seq in seqs:
            wf.write("{}\n".format(seq[0]))
            wf.write("{}\n".format(seq[1]))

def assemble_single_cluster(seqs, cluster_list, seqid_dict, out_prefix):
    cnt = 0
    for length, cluster in cluster_list:
        print(length, " ", cluster)
        extract_seqs = extract_seqs_in_cluster(seqs, seqid_dict[cluster])
        print("trim length ", len(extract_seqs))
        cnt = cnt + 1
        out_path = out_prefix + "_c{}.a3m".format(cnt)
        write_seqs(extract_seqs, out_path)


def assemble_dual_cluster(seqs, cluster_list, seqid_dict, out_prefix):
    cnt = 0
    for i in range(len(cluster_list)):
        _, cluster_a = cluster_list[i]
        for j in range(i + 1, len(cluster_list)):
            print("cluster i {} j {}".format(i, j))
            _, cluster_b = cluster_list[j]
            extract_seqs = extract_seqs_in_cluster(seqs, seqid_dict[cluster_a]) 
            extract_seqs += extract_seqs_in_cluster(seqs, seqid_dict[cluster_b], False) 
            print("trim length ", len(extract_seqs))
            cnt = cnt + 1
            out_path = out_prefix + "_c{}_c{}.a3m".format(i, j)
            write_seqs(extract_seqs, out_path)


def assemble_triple_cluster(seqs, cluster_list, seqid_dict, out_prefix):
    cnt = 0
    for i in range(len(cluster_list)):
        _, cluster_a = cluster_list[i]
        for j in range(i + 1, len(cluster_list)):
            _, cluster_b = cluster_list[j]
            for k in range(j + 1, len(cluster_list)):
                _, cluster_c = cluster_list[k]
                print("cluster i {} j {} k {}".format(i, j, k))
                extract_seqs = extract_seqs_in_cluster(seqs, seqid_dict[cluster_a]) 
                extract_seqs += extract_seqs_in_cluster(seqs, seqid_dict[cluster_b], False) 
                extract_seqs += extract_seqs_in_cluster(seqs, seqid_dict[cluster_c], False) 
                print("trim length ", len(extract_seqs))
                cnt = cnt + 1
                out_path = out_prefix + "_c{}_c{}_c{}.a3m".format(i, j, k)
                write_seqs(extract_seqs, out_path)
            
    #for length, cluster in cluster_list:
    #    print(length, " ", cluster)
    #    extract_seqs = extract_seqs_in_cluster(seqs, seqid_dict[cluster])
    #    print("trim length ", len(extract_seqs))
    #    cnt = cnt + 1
    #    out_path = out_prefix + "_c{}.a3m".format(cnt)
    #    write_seqs(extract_seqs, out_path)

if __name__ == "__main__":
    a3m_path = sys.argv[1]
    tsv_path = sys.argv[2]
    seqid_dict = load_tsv(tsv_path)
    cluster_list = []
    for cluster in seqid_dict:
        print(cluster, " ", len(seqid_dict[cluster]))
        cluster_list.append((len(seqid_dict[cluster]), cluster))
    cluster_list.sort()
    # cluster_list = cluster_list.sort()
    # print(cluster_list.sort())
    seqs = read_seqs(a3m_path)
    print("#seqs ", len(seqs))
    out_prefix = sys.argv[3]
    #assemble_single_cluster(seqs, cluster_list, seqid_dict, out_prefix)
    #assemble_dual_cluster(seqs, cluster_list, seqid_dict, out_prefix)
    assemble_triple_cluster(seqs, cluster_list, seqid_dict, out_prefix)
