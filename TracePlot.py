import matplotlib.pyplot as plt
import numpy as np
from numpy.random import rand

## TracePlot is a class that can be initialized with
## 1) list of [x,y] coordinates for tasks
## 2) list of list of [x,y] coordinates for each robots's trace [[Rb_1_Trace], [Rb_2_Trace], [Rb3_Trace]]
## People can use filed robotPlot to get a matplot.plt for the trace of each of the robots
class TracePlot:
    def __init__(self, target_list, robot_tracy_list=None, rangelimit=5):
        self.target_list = target_list
        self.num_target = len(target_list)
        self.robot_tracy_list = robot_tracy_list
        # make the constructor also work for no robot input
        if robot_tracy_list:
            self.num_robots = len(robot_tracy_list)
            self.num_movements = len(robot_tracy_list[0])
        else:
            self.num_robots = 0
            self.num_movements= 0
        self.axisLimits = self.findAxisLimits()
        self.rangelimit = rangelimit
        # self.robotPlot = self.plotRobotTracy()
# find the range of x, y axis from the input data
    def findAxisLimits(self):
        xMax = -np.inf
        xMin = np.inf
        yMax = -np.inf
        yMin = np.inf
        for i in range(self.num_target):
            x, y = self.target_list[i]
            if x > xMax:
                xMax = x
            if x < xMin:
                xMin = x
            if y > yMax:
                yMax = y
            if y < yMin:
                yMin = y
        for j in range(self.num_robots):
            for k in range(self.num_movements):
                x,y = self.robot_tracy_list[j][k]
                if x > xMax:
                    xMax = x
                if x < xMin:
                    xMin = x
                if y > yMax:
                    yMax = y
                if y < yMin:
                    yMin = y

        return [xMin, xMax, yMin, yMax]
    # def preparePlot(self):
    #     plt.axis(self.axisLimits)
    #     plt.xlabel("X axis")
    #     plt.ylabel("Y axis")
    #     plt.title("The Trace of Robots with Minial Travel")
    #     x, y = np.asarray(self.target_list).T
    #     plt.scatter(x, y, color="green", s=100, marker="s")
    #     return plt
    # def plotRobotTracy(self):
    #     newplt = self.preparePlot()
    #     cmap = [np.random.rand(self.num_robots,) for _ in range(self.num_robots)]
    #     for i in range(self.num_robots):
    #         x0,y0 = self.robot_tracy_list[i][0]
    #         newplt.plot(x0, y0, color= "red", marker="o", markersize=8)
    #         x, y = np.asarray(self.robot_tracy_list[i]).T
    #         plt.plot(x, y, color = "red", marker="o", markersize=3)
    #     return newplt

    def getNumRobots(self):
        return self.num_robots
    def getRobotTracyPlot(self, f, row, col, position, title="The Trace of Robots with Minial Travel"):
        axes = f.add_subplot(row, col, position)
        # Prepare the axis and the tasks

        # axes.axis(self.axisLimits)
        axes.set_xlabel("X axis")
        axes.set_ylabel("Y axis")
        axes.set_title(title)
        plt.xlim(0, self.rangelimit)
        plt.ylim(0, self.rangelimit)
        plt.axis([0, self.rangelimit, 0, self.rangelimit])
        x, y = np.asarray(self.target_list).T
        axes.scatter(x, y, color="green", s=100, marker="s")
        # print the label of the tasks
        for i in range(len(x)):
            axes.annotate("T"+str(i),(x[i],y[i]*1.01))

        # print the robot trace
        for i in range(self.num_robots):
            x0,y0 = self.robot_tracy_list[i][0]
            axes.plot(x0, y0, color= "red", marker="o", markersize=8)
            axes.annotate("R"+str(i),(x0,y0))
            x, y = np.asarray(self.robot_tracy_list[i]).T
            axes.plot(x, y, color = "red", marker="o", markersize=2)
        # axes.axis('equal')
        # This line make the path output in a square:
        axes.set_aspect(1.0/axes.get_data_ratio(), adjustable='box')
        axes.grid(True)
        ticks = [_ for _ in range(self.rangelimit+1)]
        axes.set_xticks(ticks)
        axes.set_yticks(ticks)

        return f


#############################################################
### unit test
#############################################################
# target = [[2, 0], [0, 2]]
# robot1 = [[1, 2], [0.5, 2], [0.25, 2], [0.125, 2], [0.0625, 2]]
# robot2 = [[2, 2], [2, 1], [2, 0.5], [2, 0.25], [2, 0.125]]
# robot3 = [[5, 5], [5, 4], [5, 3], [2, 3.5], [1.5, 1]]
# robot_path = [robot1, robot2, robot3]
# myPlot = TracePlot(target, robot_path)
# a = myPlot.robotPlot
# a.show()