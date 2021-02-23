import os

# a=[1,3,4,5]
# print (sum(x for x in a))
# print (" "*(1-2),"@"*3)
# print ("@"*2)
n=30
for x in range(n):
    if (n-x-1):
        print(" "*(n-x-2),"#"*(x+1))
    else:
        print("#"*(x+1))