'''
Pattern to make hollow hour-glass.
2 methods:
    1. Using 1 for loop
    2. Using 2 for loops
'''



def loop_1():                         #  Using 1 loop 

    print("Using one single for loop.")
    n=int(input("Enter the base number: "))
    print(" *"*n)
    rows=(n-1)*2                      #  number of rows excluding the header and footer
    for i in range(1,(n-1)*2):        
        if i==(n-2):
            print(" "*(n-2),"* *")
        elif i==(n-1):
            print(" "*(n-1),"*")
        elif 1<=i<(n-1):
            print(" "*i,"*"," "*((rows-(i-1)*2)-5),"*")
        elif i==(n):
            print(" "*(n-2),"* *")
        else:
            print(" "*(rows-i),"*"," "*(((i-n)-1)*2 +1),"*")
    print(" *"*n)

def loop_2():            #  using 2 loops
    print(f'\n Using two for loops.')
    n=int(input("Enter the base number: "))
    print(" *"*n)
    for i in range(n-2,1,-1):
        k=2*(i-2)+1
        print(" "*(n-i-1),"*"," "*k,"*")
    print(" "*(n-2),"* *")
    print(" "*(n-1),"*")
    print(" "*(n-2),"* *")
    s=(n-1)*2-(1+n)
    for i in range(s,0,-1):
        print(" "*(i),"*"," "*(abs(i-s)*2+1),"*")
    print(" *"*n)

def main():
    print('''
          Options:
          1. Using one single for loop.
          2. Using two for loops.''')
    choice=int(input("Enter choice: "))
    if choice==1:
        loop_1()
    elif choice==2:
        loop_2()
    else:
        print("Try again.")
        main()
if __name__=="__main__":
    main()