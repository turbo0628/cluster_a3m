import sys


def load_tsv(tsv_path):
    seqid_dict = {}
    with open(tsv_path, "r+") as f:
        lines = f.readlines()
    for line in lines:
        cluster, seqid = line.strip().split()
        print("cluster {}, seqid {}".format(cluster, seqid))
        if cluster in seqid_dict.keys():
            seqid_dict[cluster].append(seqid)
        else:
            seqid_dict[cluster] = [seqid]
    return seqid_dict


def trim_seqs_in_cluster(seqs, cluster_seqids):
    trim_seqs = [seqs[0]]
    for (title, seq) in seqs[1:]:
        if title[1:] in cluster_seqids:
            continue
        trim_seqs.append((title, seq))
    return trim_seqs


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

def trim_single_cluster(seqs, cluster_list, seqid_dict, out_prefix, topN=5):
    cnt = 0
    for length, cluster in cluster_list:
        if cnt >= topN:
            break
        print(length, " ", cluster)
        trim_seqs = trim_seqs_in_cluster(seqs, seqid_dict[cluster])
        print("trim length ", len(trim_seqs))
        out_path = out_prefix + "_c{}.a3m".format(cnt)
        cnt = cnt + 1
        write_seqs(trim_seqs, out_path)


def trim_dual_cluster(seqs, cluster_list, seqid_dict, out_prefix):
    cnt = 0
    for i in range(len(cluster_list)):
        _, cluster_a = cluster_list[i]
        for j in range(i + 1, len(cluster_list)):
            print("cluster i {} j {}".format(i, j))
            _, cluster_b = cluster_list[j]
            trim_seqs = trim_seqs_in_cluster(seqs, seqid_dict[cluster_a]) 
            trim_seqs = trim_seqs_in_cluster(trim_seqs, seqid_dict[cluster_b]) 
            print("trim length ", len(trim_seqs))
            cnt = cnt + 1
            out_path = out_prefix + "_c{}_c{}.a3m".format(i, j)
            write_seqs(trim_seqs, out_path)


def trim_triple_cluster(seqs, cluster_list, seqid_dict, out_prefix):
    cnt = 0
    for i in range(len(cluster_list)):
        _, cluster_a = cluster_list[i]
        for j in range(i + 1, len(cluster_list)):
            _, cluster_b = cluster_list[j]
            for k in range(j + 1, len(cluster_list)):
                _, cluster_c = cluster_list[k]
                print("cluster i {} j {} k {}".format(i, j, k))
                trim_seqs = trim_seqs_in_cluster(seqs, seqid_dict[cluster_a]) 
                trim_seqs = trim_seqs_in_cluster(trim_seqs, seqid_dict[cluster_b]) 
                trim_seqs = trim_seqs_in_cluster(trim_seqs, seqid_dict[cluster_c]) 
                print("trim length ", len(trim_seqs))
                cnt = cnt + 1
                out_path = out_prefix + "_c{}_c{}_c{}.a3m".format(i, j, k)
                write_seqs(trim_seqs, out_path)
            
    #for length, cluster in cluster_list:
    #    print(length, " ", cluster)
    #    trim_seqs = trim_seqs_in_cluster(seqs, seqid_dict[cluster])
    #    print("trim length ", len(trim_seqs))
    #    cnt = cnt + 1
    #    out_path = out_prefix + "_c{}.a3m".format(cnt)
    #    write_seqs(trim_seqs, out_path)

if __name__ == "__main__":
    a3m_path = sys.argv[1]
    tsv_path = sys.argv[2]
    seqid_dict = load_tsv(tsv_path)
    cluster_list = []
    for cluster in seqid_dict:
        print(cluster, " ", len(seqid_dict[cluster]))
        cluster_list.append((len(seqid_dict[cluster]), cluster))
    cluster_list.sort()
    cluster_list.reverse()
    seqs = read_seqs(a3m_path)
    print("#seqs ", len(seqs))
    out_prefix = sys.argv[3]
    trim_single_cluster(seqs, cluster_list, seqid_dict, out_prefix)
    #trim_dual_cluster(seqs, cluster_list, seqid_dict, out_prefix)
    #trim_triple_cluster(seqs, cluster_list, seqid_dict, out_prefix)
