import TracePlot as TP
import TaskGenerator
import matplotlib.pyplot as plt
import numpy as np
import BruteForceSolution as BFS
import time
import AminKNeuronMethod as ak

valrange = 8

############################## This is the Brute Froce Method ############################
tasklist = TaskGenerator.GenerateTask(valrange,7)
# tasklist = [[6.72, 7.39], [0.82, 0.91], [2.56, 6.7]]
print("The task list is:")
print(tasklist)
robotList = TaskGenerator.GenerateRobot(valrange,7)
# robotList = [[1.61, 7.41], [7.48, 2.89], [1.84, 0.41]]
print("The robot position list is:")
print(robotList)
# Count the Running time of BruteForce Method
start_time = time.time()
Solution = BFS.BruteForceSolution(tasklist,robotList)
print("--- brute force method time: %10f seconds ---" % (time.time() - start_time))

# Make the plots
RobotTrace = Solution.GenerateRobotPath()
TracePlot = TP.TracePlot(tasklist, RobotTrace,valrange)
# Create a Figure Object, and assign this object to each of the method that can create a subplot
# This is the only way how we can merge subplots into one Figure
# Each of the methods need to return the Figure object!!!
f = plt.figure(num=1, figsize=(15,10))
TracePlot.getRobotTracyPlot(f,1,3,1, "Brute force min Travel Dist is "+str(Solution.minDistance))
test = Solution.getDistanceHistogram(f,1,3,3)

# plt.savefig('220.png')
# plt.show()

############################## Amin's easier method with K output ############################
# Amin's easier method
# newtasklist = TaskGenerator.GenerateTask(valrange,5)
# newrobotlist = TaskGenerator.GenerateRobot(valrange,8)
# print(newrobotlist)
newSolution = ak.AminKNeuronMethod(tasklist,robotList)
start_time = time.time()
newstep = newSolution.generateRobotPathWhenKequalM(8)
print("--- K neurons method time: %10f seconds ---" % (time.time() - start_time))
print ("============The task assigned list is", newSolution.taskAssigned2)
print(newstep)
nndist = newSolution.calculateTravelDistance()
print("the total travel distance for NN is", nndist)
aaa = TP.TracePlot(tasklist,newstep, valrange)
aaa.getRobotTracyPlot(f,1,3,2, "Travel Distance for NN is "+str(np.round(nndist,2)))

# This is the only way to get a subplot out of a Figure Object!!
allaxes = f.get_axes()
# This is to add a line in a subplot and annotation
allaxes[1].axvline(np.round(nndist,2), color='r', linestyle='dashed', linewidth=5)
allaxes[1].text(nndist*1.1, allaxes[1].get_ylim()[1]*0.9, 'NN Solution: {:.2f}'.format(nndist),color='r', size=20)
plt.show()