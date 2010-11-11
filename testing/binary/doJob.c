#include <stdio.h>
#include <stdlib.h>

int main(){
	FILE *file;
	int i, c;

	char string[100];

	for(i = 0; (c = getc(stdin)) != EOF && i < 99; string[i++] = c)
		;
	string[i] = '\0';

	//

	for(i = 0; i < 1000; i++){
		fprintf(stdout, "%s", string);
	}
}
