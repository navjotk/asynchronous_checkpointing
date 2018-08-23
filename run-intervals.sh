#!/bin/bash

#TIME="/usr/bin/time -l"
TIME=""
ORDER=$1
SIZE=$2
WRITE_FILES=$3
export DEVITO_OPENMP=1
#Usage: run-intervals.sh <ORDER> <CP_SIZE> <WRITE_FILES>


NUM_STEPS=100000

INTERVAL=10
INCREMENT=10
MAX=640
#WRITE_FILES=""
#WRITE_FILES="--no-write-files"

while [  $INTERVAL -lt $MAX ]; do
    $TIME python async_experiment.py $SIZE $INTERVAL $NUM_STEPS $ORDER $WRITE_FILES
    rm -rf tmp
    mkdir tmp
    let INTERVAL=$INTERVAL+$INCREMENT
done
