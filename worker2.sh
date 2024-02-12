#!/bin/sh

executable=$1
filelist=$2
isdata=$3

currDir=$(pwd)

export Home=.

source /cvmfs/cms.cern.ch/cmsset_default.sh

scram project CMSSW_12_1_0
cd CMSSW_12_1_0/src/
eval `scramv1 runtime -sh`
cd -
echo " "
echo "Extracting venv.tar"
tar xf venv.tar
#xrdcp $2 .

ls -lrt

#export PATH=$USER_PATH:$PATH
export PATH=$PATH:$PWD/venv/bin
echo "  PATH"
$PATH

echo "Activating environment"
source venv/bin/activate

#/eos/uscms/store/user/cbell/Events/run_02/unweighted_events.lhe.gz
#xrdcp /eos/uscms/store/user/cbell/Events/run_01/unweighted_events.lhe.gz
:
#xrdcp $2 .


echo "hostname"
hostname

#python3 $1 unweighted_events.lhe.gz
python3 $1 $2
#python3 histogram.py ../Events/run_01/unweighted_events.lhe.gz
ls -lrt
