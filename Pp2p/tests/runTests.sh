#!/bin/bash

HOSTS=("vmClient0" "vmClient1" "vmClient2" "vmClient3" "vmClient4" "vmClient5" "vmClient6" "vmClient7" "vmClient8" "vmClient9" "vmClient10" "vmClient11" "vmClient12" "vmClient13" "vmClient14" "vmClient15" "vmClient16" "vmClient17" "vmClient18" "vmClient19")

CO=("vmCO")
Q=("vmQ")

SCRIPTN=("cd UROPFNS/Pp2p/tests;
    python3 runTestNode.py")

SCRIPTCO=("cd UROPFNS/Pp2p/tests;
    python3 runTestCO.py")

SCRIPTCOD=("cd UROPFNS/Pp2p/tests;
    python3 runTestCOd.py")

SCRIPTQ=("cd UROPFNS/Pp2p/tests;
    python3 runTestQ.py")

SCRIPTA=("cd UROPFNS/Pp2p/tests;
    python3 runTestAccuracy.py")

CONSOLE=$1
if [ $CONSOLE == "d" ];
then
    konsole --noclose -e ssh -t ${CO} "${SCRIPTCOD}" & sleep 20s
fi

if [ $CONSOLE == "nd" ];
then
    konsole --noclose -e ssh -t ${CO} "${SCRIPTCO}" & sleep 20s
fi

for i in ${!HOSTS[*]} ; do
    konsole --noclose -e ssh -t ${HOSTS[i]} "${SCRIPTN}" & sleep 1s
done

PULLFLAG=$2

if [ ${PULLFLAG} == "q" ];
then
    sleep 20s & konsole --noclose -e ssh -t ${Q} "${SCRIPTQ}" &
fi

if [ ${PULLFLAG} == "a" ];
then
    sleep 20s & konsole --noclose -e ssh -t ${Q} "${SCRIPTA}" &
fi