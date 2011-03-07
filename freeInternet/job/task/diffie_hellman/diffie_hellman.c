#include <stdio.h>
#include <string.h>

#define number long

number modular_multiply(number base, number power, number modulus){
    number mask, multiplier, product;
    
    product = 1;
    multiplier = base;
        
    // For each bit in power
    for(mask = 1; mask < power; mask = mask << 1){
        // Bit set in power?
        if(!!(power & mask)){
            product = (product * multiplier) % modulus;
        }
        
        // Update base^mask
        multiplier = (multiplier * multiplier) % modulus;
    }
    
    return product;
}

void diffie_hellman(char *argv[]){
    number p, g, Ax, Bx, Ay, By, S;

    p = atoi(argv[1]);
    g = atoi(argv[2]);
    Ax = atoi(argv[3]);
    Bx = atoi(argv[4]);

    Ay = modular_multiply(g, Ax, p);
    printf("%ld ", Ay);

    By = modular_multiply(g, Bx, p);
    printf("%ld ", By);
    
    S = modular_multiply(Ay, Bx, p);
    printf("%ld\n", S);
}

void usage(){
    printf("Usage: diffie_hellman prime primitive_root private_1 private_2\n");
}

int main(int argc, char *argv[]){
    /*
        scanf for {p, g, private_key1, private_key2}
        
        printf {p, g, public_key1, S}
    
    */
    // Regular use
    if(argc == 5){
        diffie_hellman(argv);
    
    } else {
        usage();
    }
    
    return 0;
}

