mat = [[]]
r = int(input("Enter the row of matrix:"))
c = int(input("Enter the column of matrix:"))


v=1
# for i in range(r):
#     for j in range(c):
#        mat[i][j].append(i+j)

for i in range(r):
    if i == 0 and len(mat[0])==0:
        for j in range(c):
            mat[0].append(v)
            v = v+1
    else:
        row = []
        for j in range(c):
            row.append(v)
            v = v+1
        mat.append(row)
        
print(mat)
for rowing in mat:
    print  (rowing)
# v=1
# mat = []
# r = int(input("Enter the row of matrix:"))
# c = int(input("Enter the column of matrix:"))
# for i in range(r):
#     row = []
#     for j in range(c):
#         row.append(v)
#         v = v+1
#     mat.append(row)
    
# print(mat)