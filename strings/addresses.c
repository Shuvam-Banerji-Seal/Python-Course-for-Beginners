#include<stdio.h>
#include<stdlib.h>
#include<string.h>



// int main() {
//     // Declare a string with a size of 100 characters
//     char str[100];
    
//     printf("Enter a string: ");
//     // Read a string from the user
//     fgets(str, sizeof(str), stdin);

//     printf("You entered: %s", str);
//     printf("The address of the string is: %p\n", (void*)str);
//     printf("The address of the first character is: %p\n", (void*)&str[0]);
//     printf("The address of the second character is: %p\n", (void*)&str[1]);
//     printf("The address of the third character is: %p\n", (void*)&str[2]);
//     printf("The address of the fourth character is: %p\n", (void*)&str[3]);
//     printf("The address of the fifth character is: %p\n", (void*)&str[4]);

//     printf("The address of the sixth character is: %p\n The sixth character is %c", (void*)&str[5], str[5]);
//     printf("\nThe address of the seventh character is: %p\n The seventh character is %c", (void*)&str[6], str[6]);
//     printf("The address of the last character is: %p\n", (void*)&str[strlen(str) - 1]);
    
//     // Return success
//     return 0;
// }


int main(){
    int array[5] = {1, 2, 3, 4, 5};
    printf("The address of the array is: %p\n", (void*)array);
    printf("The address of the first element is: %p\n", (void*)&array[0]);
    printf("The address of the second element is: %p\n", (void*)&array[1]); 
    printf("The address of the third element is: %p\n", (void*)&array[2]);
    printf("The address of the fourth element is: %p\n", (void*)&array[3]);
    printf("The address of the fifth element is: %p\n", (void*)&array[4]);
    printf("The address of the last element is: %p\n", (void*)&array[4]);
    printf("The address of the sixth element is: %p\n", (void*)&array[5]);
}