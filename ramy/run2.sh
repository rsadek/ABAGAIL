#!/bin/bash
# edit the classpath to to the location of your ABAGAIL jar file
#
export CLASSPATH=./lib/ABAGAIL.jar:../../output/production/ABAGAIL/:../../../Common/JMatIO/lib/jmatio.jar:$CLASSPATH

RUN=3;
SAMPLES=20;
ITERS=100000;
numProcs=8;

numProcs=8;
for i in 1 2 3 4 5
do
  echo "$i $numProcs yo yo"
done
# NN
#echo "NN 10 runs 10 samples 10 iters"
# { time java VoteTest 3 20 100000 Vote_3a_20_100000.mat ;}  > NN_Vote3runsa_20samples_10000iters.log 2>&1 &

# echo "NN 100 runs 10 samples 10 iters"
# { time java VoteTest 3 20 100000 Vote_3b_20_100000.mat ;} > NN_Vote3runsb_20samples_10000iters.log 2>&1 &

#echo "NN 100 runs 10 samples 100 iters"
# { time java VoteTest 3 20 100000 Vote_3c_20_100000.mat ;} > NN_Vote3runsc_20samples_100000iters.log 2>&1 &
# echo "NN 100 runs 10 samples 1000 iters"
# { time java VoteTest 3 20 100000 Vote_3d_20_100000.mat ;}  > NN_Vote3runsd_20samples_100000iters.log 2>&1



echo "done"
