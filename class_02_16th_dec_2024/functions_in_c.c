#include<stdio.h>


int func(int n)

{
    return n*n;
}


void main()
{
    int a = func(5);
    printf("%d\n",a);
}