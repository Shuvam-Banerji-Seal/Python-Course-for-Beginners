# n=13 # test value
# d={}
# for i in range(1,n+1):
#     a=i//10
#     b=i%10
#     c=a+b
#     d[i]=c
# print(d)
# m=[]
# l=[]
# for j in d:
#     # print(j)
#     m.append(j)
# for k in range(0,len(m)):
#     g=m[k]
#     if d[g]==d[j]:
#         l.append(d[j])
# print(f'm: {m}')
# print(f'l; {l}')

class solution:
    
    def __init__(self, n):
        self.n = n

    def count(self):
        count = 0
        for i in range(0, self.n + 1):
            count += 1
        return count
    
    def sum_of_digits(self):
        sum = 0
        while self.n > 0:
            digit = self.n % 10
            sum += digit
            self.n //= 10
        return sum


    def coubt_largest(self):
        count = 0
        for i in range(0, self.n + 1):
            if i == self.sum_of_digits():
                count += 1
        return count


    def main():
        n = int(input("Enter a number: "))
        array = [i for i in range(0, n+1)]
        final_array = []
        print(f"Array: {array}")
        for i in array:
            for j in array:
                if (i != j and i == sum_of_digits(j)):
                    final_array.append((i, j))
                # if (i != sum_of_digits(j)):
                #     final_array.append((i))
                    
        print(f"Final Array: {len(final_array)}")
    
if __name__ == "__main__":
    main()