#!/usr/bin/python

import subprocess

log = ""

process = subprocess.Popen(	'tar xvf job.tar.gz',
							shell=True,
							stdout=subprocess.PIPE)
log = process.stdout.readlines()

process = subprocess.Popen(	'./doJob < jobInput',
							shell=True,
							stdin=open('jobInput', 'r'),
							stdout=subprocess.PIPE)
log = process.stdout.read()
print log

subprocess.Popen('rm jobInput doJob', shell=True)
