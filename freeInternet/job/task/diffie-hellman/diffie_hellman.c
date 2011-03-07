#include <stdio.h>

#define number long int

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

int main(){
    
}