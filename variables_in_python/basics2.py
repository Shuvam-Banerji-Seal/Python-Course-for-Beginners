def main():
    name = input("\n Enter your name: ")
    print(f"Your name is {name}, and your initial is {get_initials(name)}")
    get_initials(name)


def get_initials_dd():
    pass

### HOMEWORK: the user will input the name in inconsistent cases and your will print the name in the proper eg Firs_name Last_name ie first character of the parts of the name will be in upper case.
def get_initials(name_local):
    # print(name_local.strip()) 
    # print(name_local.strip().split())
    
    parts =(name_local.strip().split())
    initials = []   #This is an empty list 
    for chunk in parts:
        # print(f"The chunk is : {chunk}")
        initials.append(chunk[0].upper())
        # print(f"The current initials are {initials}")

    ini = "".join(initials)
    # print(f"The initials in string are {ini}")
    return ini

if __name__ == '__main__':
    main()
