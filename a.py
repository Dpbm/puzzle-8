import numpy as np

# for i in range(9):
#     for j in range(9):
#         print(f"{i//3}",end=" ")
#     print()
# print("-"*10)
# for i in range(9):
#     for j in range(9):
#         print(f"{(j+3)//3}",end=" ")
#     print()

a = np.array([
    [0,0,0,1,1,1,2,2,2],
    [0,0,0,1,1,1,2,2,2],
    [0,0,0,1,1,1,2,2,2],
    [3,3,3,4,4,4,5,5,5],
    [3,3,3,4,4,4,5,5,5],
    [3,3,3,4,4,4,5,5,5],
    [6,6,6,7,7,7,8,8,8],
    [6,6,6,7,7,7,8,8,8],
    [6,6,6,7,7,7,8,8,8],
])

for block in range(9):
    print("Block ",block)
    print(a[(block//3)*3:((block//3)*3)+3, (block%3)*3:((block%3)*3)+3])
