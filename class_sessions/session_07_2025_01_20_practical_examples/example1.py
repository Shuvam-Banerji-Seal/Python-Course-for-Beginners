# def sort_by_vowel_count(sentence):

#     # Define vowels as a list
#     vowels = ['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U']
    
#     # Function to count vowels in a word
#     def count_vowels(word):
#         return sum(1 for char in word if char in vowels)
    
#     # Split sentence into words
#     words = sentence.split()
    
#     # Sort words based on vowel count
#     sorted_words = sorted(words, key=count_vowels)
    
#     # Join words back into sentence
#     return ' '.join(sorted_words)

# # Example usage
# if __name__ == "__main__":
#     test_sentence = "Rajiv has cracked a dictionary"
#     result = sort_by_vowel_count(test_sentence)
#     print(f"Original: {test_sentence}")
#     print(f"Sorted: {result}")




s="Rajib has cracked a dictionary"
s1=s.split()
d={}
print(s1)
for i in s1:
    print(i)
    c=0
    for j in i:
        #print(j)
        if j in "AEIOUaeiou":
            c+=1
            print("the vowels",j)
            print ("The no of vowels:",c)
            d[i]=c
print(d)
d1=d.values()
print(d1)
d2=sorted(d1)
print(d2)


final_sentence = []
for count in d2:    #for each count in the sorted counts
    for word, word_count in d.items(): #find words with this count
        print(f"word: {word}, word_count: {word_count}")
        if word_count == count and word not in final_sentence:
            final_sentence.append(word)
print(final_sentence)

print(" ".join(final_sentence))