#!/bin/bash -e
#SBATCH --account=t3
#SBATCH --partition=standard
#SBATCH --cpus-per-task=4
#SBATCH --mem=4000
#SBATCH --time=8:00:00
#SBATCH --nodes=1

echo "------------------------------------------------------------"
echo "[`date`] Job started"
echo "------------------------------------------------------------"
DATE_START=`date +%s`

echo HOSTNAME: ${HOSTNAME}
echo HOME: ${HOME}
echo USER: ${USER}
echo X509_USER_PROXY: ${X509_USER_PROXY}
echo CMD-LINE ARGS: $@

if [[ "$4" != "test" ]]; then
  SLURM_ARRAY_TASK_ID=$4
else
  SLURM_ARRAY_TASK_ID=1
fi

if [ -z ${SLURM_ARRAY_TASK_ID} ]; then
  printf "%s\n" "Environment variable \"SLURM_ARRAY_TASK_ID\" is not defined. Job will be stopped." 1>&2
  exit 1
fi

# define SLURM_JOB_NAME and SLURM_ARRAY_JOB_ID, if they are not defined already (e.g. if script is executed locally)
[ ! -z ${SLURM_JOB_NAME} ] || SLURM_JOB_NAME=$1
[ ! -z ${SLURM_ARRAY_JOB_ID} ] || SLURM_ARRAY_JOB_ID=local$(date +%y%m%d%H%M%S)

#SLURM_JOB_NAME=$1
echo SLURM_JOB_NAME: ${SLURM_JOB_NAME}
echo SLURM_JOB_ID: ${SLURM_JOB_ID}
echo SLURM_ARRAY_JOB_ID: ${SLURM_ARRAY_JOB_ID}
echo SLURM_ARRAY_TASK_ID: ${SLURM_ARRAY_TASK_ID}

USERDIR=$6
if [[ ${USERDIR} == /pnfs/* ]]; then
    (
      (! command -v scram &> /dev/null) || eval `scram unsetenv -sh`
      gfal-mkdir -p root://t3dcachedb.psi.ch:1094/$USERDIR
      gfal-mkdir -p root://t3dcachedb.psi.ch:1094/$USERDIR/logs
      sleep 5
    )
#mkdir -p $USERDIR
fi
echo OUTPUT_DIR: $USERDIR

# local /scratch dir to be used by the job
TMPDIR=/scratch/${USER}/slurm/${SLURM_JOB_NAME}_${SLURM_JOB_ID}_${SLURM_ARRAY_TASK_ID}
echo TMPDIR: ${TMPDIR}
mkdir -p ${TMPDIR}
NUM_LUMIBLOCK=${SLURM_ARRAY_TASK_ID}
cd ${TMPDIR}

source /cvmfs/cms.cern.ch/cmsset_default.sh

echo
echo "--------------------------------------------------------------------------------"
echo "--------------------------------------------------------------------------------"
echo "                          Creating JOB ["$4"]"
echo

export SCRAM_ARCH=slc7_amd64_gcc700
cd ${TMPDIR}

scramv1 project CMSSW $2
cd $2/src
eval `scram runtime -sh`
git clone https://github.com/TizianoBevilacqua/SiPixelTools-PhaseIPixelNtuplizer.git SiPixelTools/PhaseIPixelNtuplizer
cd SiPixelTools/PhaseIPixelNtuplizer

# output file
output="Ntuple_"$4".root"

echo
echo "--------------------------------------------------------------------------------"
echo "                                JOB ["$4"] ready"
echo "                                    Compiling..."
echo

sed -i "s;CMSSW_VERSION 113;CMSSW_VERSION 106;" plugins/PhaseIPixelNtuplizer.h
sed -i "s;CMSSW_VERSION 113;CMSSW_VERSION 106;" interface/PixelHitAssociator.h
scram b -j 4

echo
echo "--------------------------------------------------------------------------------"
echo "                                 Compiling ready"
echo "                               Starting JOB ["$4"]"
echo

if [[ $#argv > 7 ]]; then
    echo $#
    echo "cmsRun test/run_MyTest_PhaseIPixelNtuplizer_Data_2018_106X_cfg.py globalTag=$3 dataTier=ALCARECO inputFileName=$5 outputFileName=$output maxEvents=$7\n"
    cmsRun test/run_MyTest_PhaseIPixelNtuplizer_Data_2018_106X_cfg.py dataTier=ALCARECO  globalTag=$3 outputFileName=$output inputFileName=$5 maxEvents=$7
else
    echo "cmsRun test/run_MyTest_PhaseIPixelNtuplizer_Data_2018_106X_cfg.py globalTag=$3 dataTier=ALCARECO inputFileName=$5 outputFileName=$output maxEvents=-1\n"
    cmsRun test/run_MyTest_PhaseIPixelNtuplizer_Data_2018_106X_cfg.py dataTier=ALCARECO  globalTag=$3 outputFileName=$output inputFileName=$5 maxEvents=-1
fi


echo
echo "--------------------------------------------------------------------------------"
echo "                               JOB ["$4"] Finished"
echo "                              Writing output to EOS?..."
echo

# Copy to Eos
if [[ ${USERDIR} == /pnfs/* ]]; then
    xrdcp -f -N $output root://t3dcachedb.psi.ch:1094//$USERDIR/$output
    xrdcp -f -N /work/${USER}/test/.slurm/${SLURM_JOB_NAME}_${SLURM_JOB_ID}_${4}.out root://t3dcachedb.psi.ch:1094//$USERDIR/logs/${SLURM_JOB_NAME}_${SLURM_JOB_ID}_${4}.out
    xrdcp -f -N /work/${USER}/test/.slurm/${SLURM_JOB_NAME}_${SLURM_JOB_ID}_${4}.err root://t3dcachedb.psi.ch:1094//$USERDIR/logs/${SLURM_JOB_NAME}_${SLURM_JOB_ID}_${4}.err
else
    cp $output $USERDIR/$output
    cp  /work/${USER}/test/.slurm/${SLURM_JOB_NAME}_${SLURM_JOB_ID}_${4}.out $USERDIR/logs/${SLURM_JOB_ID}_${SLURM_JOB_ID}_${4}.out
    cp  /work/${USER}/test/.slurm/${SLURM_JOB_NAME}_${SLURM_JOB_ID}_${4}.err $USERDIR/logs/${SLURM_JOB_ID}_${SLURM_JOB_ID}_${4}.err
fi

echo
echo "Output: "
ls -l $USERDIR/$output

cd ../../../..
rm -rf $2

echo
echo "--------------------------------------------------------------------------------"
echo "                                 JOB ["$4"] DONE"
echo "--------------------------------------------------------------------------------"
echo "--------------------------------------------------------------------------------"
