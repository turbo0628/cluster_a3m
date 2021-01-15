#!/bin/bash

basedir=`dirname $0`
origin_a3m=$1
outroot=$2
tmproot=$3

python=python3
mmseqs="$basedir/mmseqs/bin/mmseqs"

if [ -z "$tmproot" ]; then
    tmproot="/dev/shm/a3m_cluster_trim_tmp"
fi

if [ ! -d $tmproot ]; then
    mkdir -p $tmproot
fi
if [ ! -d $outroot ]; then
    mkdir -p $outroot
fi

# I simply don't check, but it has to end with a3m.
target=`basename -- $origin_a3m`
target=${target%.a3m}

echo "TARGET $target"

tmpdir=`mktemp -d ${tmproot}/cluster_trim_XXXXXX`

# dealignment
$python $basedir/dealign.py $1 $tmpdir/${target}.fasta

# cluster
$mmseqs easy-cluster $tmpdir/${target}.fasta $tmpdir/${target} $tmpdir/mmseq
tsv_path=$tmpdir/${target}_cluster.tsv
if [ ! -s "$tsv_path" ]; then
    echo "TSV file $tsv_path not found"
    exit -1
fi
# tsv path
$python $basedir/trim_by_cluster.py $origin_a3m $tsv_path $outroot/$target

rm -rf $tmpdir
