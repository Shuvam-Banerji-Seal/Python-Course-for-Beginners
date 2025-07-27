
def number_of_special_characters(string):
    count = 0
    # for char in string:
    #     if not (ord(char) >= 65 and ord(char) <= 90) and not (ord(char) >= 97 and ord(char) <= 122) and not (ord(char) >= 48 and ord(char) <= 57):
    #         count += 1
    
    for char in string:
        if not (char.isalnum() or char.isspace()):
            count += 1
    return count

def number_of_vowels(string):
    count = 0
    vowels = "aeiouAEIOU"
    for char in string:
        if char in vowels:
            count += 1
    return count

def number_of_spaces(string):
    count = 0
    for char in string:
        if ord(char) == 32:
            count += 1
    return count

def number_of_lowercase(string):
    count = 0
    for char in string:
        if char.islower():
            count += 1
    return count


def number_of_uppercase(string):
    count = 0
    for char in string:
        if char.isupper():
            count += 1
    return count

def number_of_digits(string):
    count = 0
    for char in string:
        if char.isdigit():
            count += 1
    return count

def number_of_alphabets(string):
    count = 0
    for char in string:
        if char.isalpha():
            count += 1
    return count

def main():
    no_of_alphabets=0
    no_of_digits=0
    no_of_uppercase=0
    no_of_lowercase=0
    no_of_spaces=0
    no_of_vowels=0
    no_of_special_characters=0
    
    with open("test.txt", "r") as file:
        text = file.read()
        print(f"Content of the file: {text}")
        no_of_alphabets = number_of_alphabets(text)
        no_of_digits = number_of_digits(text)
        no_of_uppercase = number_of_uppercase(text)
        no_of_lowercase = number_of_lowercase(text)  
        no_of_spaces = number_of_spaces(text)
        no_of_vowels = number_of_vowels(text)
        no_of_special_characters = number_of_special_characters(text)
        
    print("Number of alphabets: ", no_of_alphabets)
    print("Number of digits: ", no_of_digits)
    print("Number of uppercase: ", no_of_uppercase)
    print("Number of lowercase: ", no_of_lowercase)
    print("Number of spaces: ", no_of_spaces)
    print("Number of vowels: ", no_of_vowels)
    print("Number of special characters: ", no_of_special_characters)



if __name__ == "__main__":
    main()

# main() # try not to use it