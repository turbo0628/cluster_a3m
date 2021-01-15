#!/bin/bash

a3m_inroot=/opt/ml/share/magichuang/CAMEO_MultA3Ms
a3m_outroot=/opt/ml/share/magichuang/CAMEO_TrimA3Ms/a3m
npz_outroot=/opt/ml/share/magichuang/CAMEO_TrimA3Ms/npz
multdir=$1
basedir=`dirname $0`

mkdir -p /opt/ml/env/tfold-ms/
tmproot=/opt/ml/env/tfold-ms

# Traverse all files under multdir
for a3m_file in $a3m_inroot/$multdir/*.a3m; do
	echo "Processing $a3m_file"
	bash $basedir/gen_trim_signle_cluster.sh $a3m_file $a3m_outroot/$multdir $tmproot &
done
wait

# Invoke pred npz

export RXTHREAD_HOME="/opt/Tencent_Threading"
export TFOLDMS_ENABLE="True"
export PYENV_PATH="$RXTHREAD_HOME/Miniconda_Pkgs/miniconda2/envs/trrosetta"
export TGT_PKG_PATH="$RXTHREAD_HOME/TGT_Package"
export PROP_PKG_PATH="$RXTHREAD_HOME/Predict_Property"


local_outdir=`mktemp -d /opt/ml/env/tfold-ms/pred_npz_XXXXXXX`

pushd $local_outdir

relnam=${multdir%_MultA3Ms}

echo "[`date`] - PredNPZ starts."

$RXTHREAD_HOME/trRosetta_Package/pred_orientation/PredNPZ.sh -i $relnam -r $a3m_outroot/$multdir -S 8 -o ${local_outdir}/${relnam}_NPZ -O ${local_outdir}/${relnam}.npz -E $PYENV_PATH -T $TGT_PKG_PATH -P $PROP_PKG_PATH

echo "[`date`] - PredNPZ Finished. Return code $?."

tar cf ${relnam}.tar *
cp -rv ${relnam}.tar ${npz_outroot}

popd

rm -rf ${local_outdir}
