import commands
import os
import math

import freeInternet.common as common

_DESCRIPTION = "A brute force attack against a Diffie-Hellman-Merkle Key Exchange system with a 128 bit key"

P = 23
G = 5

def execute(command):
    return commands.getoutput(command)

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

def input(directory, max):
    binary_path = os.path.join(directory, "diffie_hellman")
    
    Ay, By, S = diffie_hellman(binary_path)
    
    for partition in common.partition(range(P), max):
        yield partition[0], partition[-1], int(Ay), int(By), int(S)        
    
    execute("rm %s" % binary_path)