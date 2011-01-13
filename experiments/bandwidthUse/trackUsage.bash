#!/bin/bash

while /bin/true; do sleep $2; clear; tc -s qdisc ls dev $1 | grep bytes; done 
