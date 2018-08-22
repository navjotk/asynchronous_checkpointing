#!/bin/bash

#TIME="/usr/bin/time -l"
TIME=""
SIZE=160000
NUM_STEPS=100000
INTERVAL=10
ORDER=16
INCREMENT=10
MAX=640
#WRITE_FILES=""
WRITE_FILES="--no-write-files"

while [  $INTERVAL -lt $MAX ]; do
      $TIME python async_experiment.py $SIZE $INTERVAL $NUM_STEPS $ORDER $WRITE_FILES
      let INTERVAL=$INTERVAL+$INCREMENT
done
