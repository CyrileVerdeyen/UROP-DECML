#!/bin/bash

HOSTS=("vmClient0" "vmClient1" "vmClient2" "vmClient3" "vmClient4" "vmClient5" "vmClient6" "vmClient7" "vmClient8" "vmClient9" "vmClient10" "vmClient11" "vmClient12" "vmClient13" "vmClient14" "vmClient15" "vmClient16" "vmClient17" "vmClient18" "vmClient19" "vmCO" "vmQ")

SCRIPT=("git clone -b serverImplementation --single-branch https://github.com/CyrileVerdeyen/UROPFNS.git;
    cd UROPFNS/Pp2p;
    sudo ./setup.sh")

SCRIPTP=("cd UROPFNS/Pp2p;
    git pull")

SCRIPTB=("sudo rm -r UROPFNS;
    git clone -b serverImplementationMnist --single-branch https://github.com/CyrileVerdeyen/UROPFNS.git")

SCRIPTR=("cd UROPFNS/Pp2p/tests;
    rm saved_model0.pkl")

SCRIPTN=("cd UROPFNS/Pp2p/tests;
    mv saved_model0.pkl saved_model_MnistSVM.pkl")

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

if [[ ${PULLFLAG} == *"rename" ]];
then
    for i in ${!HOSTS[*]} ; do
        konsole --noclose -e ssh -t ${HOSTS[i]} "${SCRIPTN}" & sleep 1s
    done
fi

if [[ ${PULLFLAG} == *"branch" ]];
then
    for i in ${!HOSTS[*]} ; do
        konsole --noclose -e ssh -t ${HOSTS[i]} "${SCRIPTB}" & sleep 1s
    done
fi