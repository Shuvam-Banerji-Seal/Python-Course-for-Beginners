#include <stdio.h>
int main()
{
    int a = 5;
    char name[8] = "Duytika";
    char c;
    printf(" the value of the interger is %d", a);
    printf("\n The amount of storage used by the integer is %d \n", sizeof(a));
    printf(" the value of the string is %s", name);
    printf("\n The amount of storage used by the string is %d \n", sizeof(name));
    printf(" the value of the character is %c", c); 
    printf("\n The amount of storage used by the character is %d \n", sizeof(c));
    return 0;
}