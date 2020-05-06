import random

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
    print(random.randint(lower,upper))
        
