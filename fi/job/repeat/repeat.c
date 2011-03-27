#include <stdio.h>

int main(int argc, char *argv[]){
    int i, j;
    
    sleep(5);

    for(i = 0; i < 1000; i++){
        for(j = 1; j < argc; j++){
            printf("%s ", argv[j]);
        }
        printf("\n");
    }
}