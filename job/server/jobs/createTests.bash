#!/bin/bash
rm -rf 0*

gcc -o job job.c > /dev/null
for i in {001..010}; do
    mkdir $i
    cp ./job $i/
    echo "$i" > $i/jobInput

    tar czvf $i.tar.gz $i > /dev/null
    rm -rf $i
done
