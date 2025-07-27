

#Write a python code to print the pascals triangle by taking input from an user that will be the row number



def factorial(n):
    fac =1
    for i in range(1,n+1):
        fac=fac*i
    return fac

def Cnk(n,k):
    return int(factorial(n)/(factorial(k)*factorial(n-k)))

def pascal_triangle(n):
    for i in range(n):
        for j in range(n-i+1):
            print(end=" ")
        for j in range(i+1):
            print(Cnk(i,j),end=" ")
        print()

def main():
    n = int(input("Enter the number of rows: "))
    pascal_triangle(n)

if __name__ == "__main__":
    main()
  
