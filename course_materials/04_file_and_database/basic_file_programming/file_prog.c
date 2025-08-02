#include<stdio.h>
#include<stdlib.h>
int main()
{
    FILE *fp;
    fp = fopen("test.I_live_in_a_dream", "w");
    if(fp == NULL)
    {
        printf("Error in creating file");
        exit(1);
    }
    fprintf(fp, "Hello World\n");
    fprintf(fp, "This is a test file\n");
    fprintf(fp, "This file is created using C programming\n");
    fprintf(fp, "This is the end of the file\n");
    fclose(fp);
    return 0;
}