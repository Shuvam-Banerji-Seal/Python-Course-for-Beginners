

# Write a python code to take the email address from the user and then use string slicing to extract the user name and domain name and print them.
# Example:
# Input:
# Enter your email address: 2r9bI@example.com
# Output:
# User name: 2r9bI
# Domain name: example.com

def main():
    email = input("Enter your email address: ")
    user_name = email[:email.index("@")]
    domain_name = email[email.index("@")+1:]
    print(f"User name: {user_name}")
    print(f"Domain name: {domain_name}")    

def trial():
    p=str(input("Enter email address:"))
    s=list(p)
    m=len(s)
    print(s)
    for i in s :
        if i=="@":
            n=s.index(i)
    print("The user name:",str(s[0:n]))
    print("The doamin:",s[n+1:m])
    
    
trial()