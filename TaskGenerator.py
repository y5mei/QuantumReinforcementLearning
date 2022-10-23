from random import random


# GenerateTast Function will take two variables
# 1) maxValue -> the max value of (x,y) coordinate
# 2) numofTask -> how many task in total
# and return a list of coordinate[x,y] for each task in the system
def GenerateTask(maxValue: int, numofTask: int):
    result = []
    for i in range(numofTask):
        x = round(random() * maxValue, 2)
        y = round(random() * maxValue, 2)
        result.append([x, y])
    return result


# GenerateRobot Function will take two variables
# 1) maxValue -> the max value of (x,y) coordinate
# 2) numofRobot -> how many robots in total
# and return a list of coordinate[x,y] for each robots in the system
def GenerateRobot(maxValue: int, numofRobot: int):
    return GenerateTask(maxValue, numofRobot)

def GenerateRobotTrace(maxValue:int, numofRobot:int):
    mylist = GenerateTask(maxValue, numofRobot)
    result = []
    for i in mylist:
        result.append([i])
    return result



#############################################################
### unit test
#############################################################
# taskList = GenerateTask(5, 10)
# robotsList = GenerateTask(5, 15)
# print(taskList)
# print(robotsList)
