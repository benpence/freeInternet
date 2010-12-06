#!/bin/bash

rm -rf jobs
mkdir jobs
gcc -o job job.c > /dev/null

for i in {00000..00002}; do
    for j in {1..3}; do
        dir=jobs/$i$j
        mkdir $dir
        cp ./job $dir
        echo "$i" > $dir/jobInput
        tar czvf $dir.send.tgz $dir > /dev/null
        rm -rf $dir
    done
done

rm job
