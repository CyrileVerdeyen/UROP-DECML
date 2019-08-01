#!/bin/bash

HOSTS=("vmClient0" "vmClient1" "vmClient2" "vmClient3" "vmClient4" "vmClient5" "vmClient6" "vmClient7" "vmClient8" "vmClient9" "vmClient10" "vmClient11" "vmClient12" "vmClient13" "vmClient14" "vmClient15" "vmClient16" "vmClient17" "vmClient18" "vmClient19" "vmCO" "vmQ")

SCRIPT=("git clone -b serverImplementation --single-branch https://github.com/CyrileVerdeyen/UROPFNS.git;
    cd UROPFNS/Pp2p;
    sudo ./setup.sh")

SCRIPTP=("cd UROPFNS/Pp2p;
    git pull")

PULLFLAG=$1

if [ ${PULLFLAG} -eq 0 ];
then
    for i in ${!HOSTS[*]} ; do
        konsole --noclose -e ssh -t ${HOSTS[i]} "${SCRIPT}" & sleep 6s
    done
fi

if [ ${PULLFLAG} -eq 1 ];
then
    for i in ${!HOSTS[*]} ; do
        konsole --noclose -e ssh -t ${HOSTS[i]} "${SCRIPTP}" & sleep 6s
    done
fi