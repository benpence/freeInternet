#include <stdio.h>
#include <string.h>

#define number long

number square_and_multiply(number base, number power, number modulus){
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

void brute_force(char *argv[]){
    number p, g, public_key_1, public_key_2, start, stop;
    number private_key;
    
    p = atoi(argv[1]);
    g = atoi(argv[2]);
    public_key_1 = atoi(argv[3]);
    public_key_2 = atoi(argv[4]);
    start = atoi(argv[5]);
    stop = atoi(argv[6]);
    
    // Try all stop->stop private keys
    private_key = start;
    while(square_and_multiply(g, private_key, p) != public_key_1  &&  private_key <= stop + 1){
        private_key++;
    }
    
    if(private_key == stop + 1){
        printf("Private key not in range");
    } else {
        printf("Shared key %ld", square_and_multiply(public_key_2, private_key, p));
    }
}

void diffie_hellman(char *argv[]){
    number p, g, Ax, Bx;
    number Ay, By;

    p =  atoi(argv[1]);
    g =  atoi(argv[2]);
    Ax = atoi(argv[3]);
    Bx = atoi(argv[4]);

    Ay = square_and_multiply(g, Ax, p);
    printf("%ld ", Ay);

    By = square_and_multiply(g, Bx, p);
    printf("%ld", By);
}

void usage(){
    printf("Usage: diffie_hellman prime primitive_root private_key_1 private_key_2\n");
    printf("Usage: diffie_hellman prime primitive_root public_key_1 public_key_2 range_start range_end\n");
}

int main(int argc, char *argv[]){
    /*
        scanf for {p, g, private_key1, private_key2}
        
        printf {p, g, public_key1, S}
    
    */
    
    // Job
    if(argc == 7){
        brute_force(argv);
        
    // Create public key
    } else if(argc == 5){
        diffie_hellman(argv);
        
    } else {
        usage();
    }
    
    return 0;
}