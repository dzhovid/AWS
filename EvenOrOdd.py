# a program which checks if the given number is odd or even
print(" ")
x=int(input("Please enter a number to check if it is even or odd: "))
print("==========================================================")
y = x % 2
if y == 0:
    print("                      The number you have entered is EVEN.")
else:
    print("                      The number you have entered is ODD.")
print(" ")