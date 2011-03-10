#include <stdio.h>
#include <stdlib.h>

int main(){
    FILE *file;
    int i, c;

    char string[100];

    file = fopen("client_files/jobInput", "r");

    for(i = 0; (c = getc(file)) != EOF && i < 99; string[i++] = c)
        ;
    fclose(file);
    
    string[i] = '\0';

    sleep(5);

    file = fopen("client_files/jobOutput", "w");
    for(i = 0; i < 1000; i++){
        fprintf(file, "%s", string);
    }
    fclose(file);
}