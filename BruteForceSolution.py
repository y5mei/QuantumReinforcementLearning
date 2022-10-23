import math
import itertools
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict


class BruteForceSolution:
    def __init__(self,taskList,robotList):
        self.taskList = taskList
        self.robotList = robotList
        self.m = len(taskList) # num of tasks
        self.k = len(robotList) # num of robots
        self.distanceMap = self.DistMapRobottoTarget()
        self.sorted_arrangement_dist_list = self.AllPossibleList()
        self.uniqueCombination = 0
        self.eliminateItems = dict()
        self.minDistance = self.sorted_arrangement_dist_list[1][0]


    def distanceBetweenTwoPoints(self,x,y,m,n):
        return math.sqrt((x-m)*(x-m)+(y-n)*(y-n))

    def AllPossibleList(self):
        '''
        :return: return a sorted list [arrangement, distance]
        '''
        items = []
        for i in range(self.k):
            taskIndex = [_ for _ in range(self.m)]
            items.append(taskIndex)

        # allItems are all the M^K possible arrangements
        allItems = list(itertools.product(*items))
        # eliminate the arrangements that there is a target does not have any robot
        eliminateItems = dict()
        s =""
        for item in allItems:
            # if there is any task has no robot, we ignore this arrangement
            if len(set(item)) < self.m:
                continue
            myValue = 0
            myKey = s.join(list(map(str, item)))
            for nRbot, nTask in enumerate(item):
                distKey = str(nRbot)+str(nTask)
                myValue += self.distanceMap[distKey]
            eliminateItems[myKey]=round(myValue,2)
        # update the number of the unique arrangement that all target get at least one robot
        self.uniqueCombination = len(eliminateItems.keys())
        self.eliminateItems = eliminateItems
        # sort from small to big
        sort_orders = sorted(self.eliminateItems.items(), key=lambda x: x[1], reverse=False)
        return list(zip(*sort_orders))
        # print(self.uniqueCombination)

        # sort_orders = sorted(eliminateItems.items(), key=lambda x: x[1], reverse=False)
        # sort_distance = sorted(eliminateItems.values(),reverse=False)
        # print(sort_distance)
        # for key, value in sort_orders:
        #     print (key,"distance is ", value)

    def DistMapRobottoTarget(self):
        '''
        :return: a map that key is the [Robot-->Target] arrangement, and value is Distance
        '''
        d = dict()
        robotNumLilst = [_ for _ in range(self.k)]
        taskNumList = [_ for _  in range(self.m)]
        allCombination = list(itertools.product(robotNumLilst,taskNumList))

        for rNum, tNum in allCombination:
            x,y = self.robotList[rNum]
            i,j = self.taskList[tNum]
            # Calculate the distance between the robot (x,y) and the target (i,j)
            distance = math.sqrt((x-i)*(x-i)+(y-j)*(y-j))
            distance = round(distance, 2)
            mykey = str(rNum)+str(tNum)
            d[mykey] = distance
        #
        # for arrangement, dist in d.items():
        #     print ("Robot -> Target [",arrangement,"] distance is "+ str(dist))
        return d

    def getDistanceHistogram(self,f, row, col, position):
        axes = f.add_subplot(row, col, position)
        seperated_list = self.sorted_arrangement_dist_list
        # the histogram of the data
        n, bins, patches = plt.hist(seperated_list[1],bins=50)
        plt.xlabel('Travel Distance')
        plt.ylabel('Occurrence')
        titleStr = "M = "+ str(self.m)+"   K="+str(self.k)+", The shortest Distance is "+str(seperated_list[1][0])+"\n Total # of available arrangement is "\
                   +str(len(seperated_list[0]))+\
                   "\n The Min path will assign the robots to tasks:"+ seperated_list[0][0] +" respectively"
        plt.title(titleStr)
        plt.grid(True)
        return f

    def getSubPlotTest(self,f, row, col, position):
        '''
        This is a test funciton, do not use
        :param f:
        :param row:
        :param col:
        :param position:
        :return:
        '''
        axarr = f.add_subplot(row,col,position)
        axarr.plot([5,5])
        # print(type(f))
        return f
    def getSubPlotReal(self,f, row, col, position):
        '''
        This is a test funciton, do not use
        :param f:
        :param row:
        :param col:
        :param position:
        :return:
        '''
        axes = f.add_subplot(row, col, position)
        seperated_list = self.sorted_arrangement_dist_list
        n, bins, patches = plt.hist(seperated_list[1])
        plt.xlabel('Travel Distance')
        plt.ylabel('Occurrence')
        titleStr = "M = " + str(self.m) + "   T=" + str(self.k) + "\n Total # of available arrangement is " \
                   + str(len(seperated_list[0])) + "\n The shortest Distance is " + str(seperated_list[1][0]) + \
                   "\n with the Robot -> Task arrangement as " + seperated_list[0][0]
        plt.title(titleStr)
        plt.grid(True)
        return f
    def GenerateRobotPath(self):
        bestArrangement = self.sorted_arrangement_dist_list[0][0]
        nextMovement = []
        for i in bestArrangement:
            index = int(i)
            taskCoordinate = self.taskList[index]
            nextMovement.append(taskCoordinate)

        RobotTrace = [self.robotList,nextMovement]
        RobotTrace = [list(a) for a in zip(self.robotList, nextMovement)]
        # print("this is the robot trace:")
        # print(RobotTrace)
        # RobotTrace = list(zip(*RobotTrace))
        return RobotTrace







#############################################################
### unit test
#############################################################
# target = [[2, 0], [0, 2],[3,3]]
# robot1 = [[1, 2], [0.5, 2], [0.25, 2], [0.125, 2], [0.0625, 2]]
#
#
# b = BruteForceSolution(target,robot1)
# l = b.AllPossibleList()
# b.getDistanceHistogram()
#
# trace = b.GenerateRobotPath()
#
# for i in trace:
#     print(i)