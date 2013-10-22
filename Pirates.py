# Some comment
w=0
while w!=1:
    print ("Ready?");x=input()
    if x.lower() in ("yea", "yep", "yesh", "yar", "yup"):
        for x in range(1,201):
            print(x)
        w=1
        print ('Wooooooooooooooooooooot! You did it!')
    else:
        print ('Nope...')
