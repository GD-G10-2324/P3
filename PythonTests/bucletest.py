import time
COMM_LIMIT = 5000
FAULT_DELTA = 14
SECONDSHOUR = 3600
totalcommits = 33733
interval = round(SECONDSHOUR/(COMM_LIMIT-FAULT_DELTA),3)
print('INTERVALO USADO: ',interval)
while totalcommits >= 0:
    print(totalcommits, end=', ')
    totalcommits-=1
    time.sleep(interval)