import random, time

outList = ['','','','','']

while True:
    for i in range(0,5):
        if i == 0:
            upper = 90
            lower = 0
        elif i == 1:
            upper = 60
            lower = 0
        elif i == 2:
            upper = 20
            lower = -80
        elif i == 3:
            upper = 15
            lower = -90
        else:
            upper = 1
            lower = 0
        outList[i] = str(random.randint(lower,upper))+ '\n'
    print(outList)
    outText = open('positions.txt','w')
    outText.writelines(outList)
    outText.close()
    time.sleep(10)

    
