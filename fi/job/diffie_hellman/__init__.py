import commands
import os
import math

import fi

DESCRIPTION = "A brute force attack against a Diffie-Hellman-Merkle Key Exchange system with a 128 bit key"

P = 23
G = 5

execute = commands.getoutput

def diffie_hellman(binary_path):
    output = execute("gcc -o %s %s.c" % (
        binary_path,
        binary_path
        )
    )
    
    # Compiler errors?
    if output.strip():
        print output
        exit(1)
        
    output = execute("%s %d %d %d %d" % (
        binary_path,
        P, G,
        6, #Ax
        15 #Bx
    ))
    
    return output.split()

def input(max, binary_path):
    Ay, By, S = diffie_hellman(binary_path)
    
    for partition in fi.partition(range(P), max):
        yield partition[0], partition[-1], int(Ay), int(By), int(S)        
    
    execute("rm %s" % binary_path)