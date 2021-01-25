# perfect square
print(" ")
print("This program finds all perfect squares within a specified range (from 1 to any number).")
print(" ")
b=int(input("Please type the higher limit of the range: "))
newlist=[]
for i in range(1,b):
    for j in range(1,b):
        y=i/j
        z=y/j
        if z==1:
            newlist.append(i)
print("=======================================================================================")
print("Here is the list of perfect squares within the range ( 1 -", b,"):")
print(newlist)
print(" ")