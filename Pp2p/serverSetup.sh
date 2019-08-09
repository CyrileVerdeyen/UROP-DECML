#!/bin/bash

HOSTS=("vmClient0" "vmClient1" "vmClient2" "vmClient3" "vmClient4" "vmClient5" "vmClient6" "vmClient7" "vmClient8" "vmClient9" "vmClient10" "vmClient11" "vmClient12" "vmClient13" "vmClient14" "vmClient15" "vmClient16" "vmClient17" "vmClient18" "vmClient19" "vmCO" "vmQ")

SCRIPT=("git clone -b serverImplementation --single-branch https://github.com/CyrileVerdeyen/UROPFNS.git;
    cd UROPFNS/Pp2p;
    sudo ./setup.sh")

SCRIPTP=("cd UROPFNS/Pp2p;
    git pull")

SCRIPTR=("cd UROPFNS/Pp2p/tests;
    rm saved_model0.pkl")

SCRIPTM=("cd UROPFNS/Pp2p;
    wget -O Tdata.tar.gz 'http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz';
    tar -C ./tests -xvzf Tdata.tar.gz;
    wget -O Ldata.tar.gz 'http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz';
    tar -C ./tests -xvzf Ldata.tar.gz;
    wget -O Tedata.tar.gz 'http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz';
    tar -C ./tests -xvzf Tedata.tar.gz;
    wget -O Ledata.tar.gz 'http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz';
    tar -C ./tests -xvzf Ledata.tar.gz")

SCRIPTD=("cd UROPFNS/Pp2p/tests;
    git clean -f")

PULLFLAG=$1

if [[ ${PULLFLAG} == *"setup" ]];
then
    for i in ${!HOSTS[*]} ; do
        konsole --noclose -e ssh -t ${HOSTS[i]} "${SCRIPT}" & sleep 6s
    done
fi

if [[ ${PULLFLAG} == *"pull" ]];
then
    for i in ${!HOSTS[*]} ; do
        konsole --noclose -e ssh -t ${HOSTS[i]} "${SCRIPTP}" & sleep 1s
    done
fi

if [[ ${PULLFLAG} == *"remove" ]];
then
    for i in ${!HOSTS[*]} ; do
        konsole --noclose -e ssh -t ${HOSTS[i]} "${SCRIPTR}" & sleep 1s
    done
fi

if [[ ${PULLFLAG} == *"delete" ]];
then
    for i in ${!HOSTS[*]} ; do
        konsole --noclose -e ssh -t ${HOSTS[i]} "${SCRIPTD}" & sleep 1s
    done
fi