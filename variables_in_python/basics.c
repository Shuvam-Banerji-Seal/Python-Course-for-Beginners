#include <stdio.h>
#define main duytika
int foo()
{
  printf("\n This is the foo function");
  return 0;
}

int duytika()
{
  printf("\n This is the main function");
  foo();
  return 0;
}
