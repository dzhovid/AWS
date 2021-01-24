from random import randint
secret_num = randint(1,10)
#guess = 0
i=0
while i < 6:
    if i==5:
        print("You lost your 5 chances. Start over.")
        break
    i+=1
    guess = int(input('Guess the secret number which is in range (1 - 10): '))
    if guess > secret_num:
        print("HINT: Go lower.")
    if guess < secret_num:
        print("HINT: Go higher.")
    if guess == secret_num:
        print("That's correct. You got it!")
        break

print("Hello from Git session in Vs Code.")