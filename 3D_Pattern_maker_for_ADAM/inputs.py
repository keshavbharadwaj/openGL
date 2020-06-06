def ini():
    k=input("Which boxes do you want\n0 for box2\n1 for box3\n2 for box4 \n3 for box5 \n4 for box6\n5 for box7\n").split(',')
    l=[0,0,0,0,0,0]
    for i in k:
        if int(i)>6 and int(i)<0:
            print("Out of range of boxes")
            exit()
        l[int(i)]=int(input("how many of box"+str(int(i)+2)+" do you want"))
    print(l)
    return l
