#!/usr/bin/python

def chores(l):
    print l[0]
    yield True

    print l[1]
    yield True

    print l[2]
    yield True

    yield False

test = chores(['hey', 'ho', 'hiya'])
while test.next():
    pass
