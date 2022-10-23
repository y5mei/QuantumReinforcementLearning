import random
import math

class AminKNeuronMethod:
    def __init__(self,target_list,robot_list):
        self.target_list = target_list # list of position of tasks
        self.robot_list = robot_list # list of position of robots
        self.m = len(target_list) # num of tasks
        self.k = len(robot_list) # num of robots
        self.wx = [0]*self.k # this is the connecting weights for x coordinates
        self.wy = [0]*self.k # this is the connecting weights for y coordinates
        self.Dmin = 0 # Dmin is the min distance between any two targets, this is a scale factor that controls when the loop will converge
        # By default, when delta_distance < 0.5*Dmin, we say the path plan converged.
        self.arrived2Task = [0]*self.k # this is 1 if the robot arrived to a task already, and will not move anymore;
        self.taskAssigned2 = [None]*self.m # this is the list which task is assigned to which robot, return None if not decide yet
        # initialize the connecting weights by the position of the robots
        for i in range(self.k):
            self.wx[i] = robot_list[i][0]
            self.wy[i] = robot_list[i][1]

        # find Dmin, which is the min distance between any two targets, or 0.001
        currentDmin = float('inf')
        for i in range(self.m):
            for j in range(i+1, self.m,1):
                xi, yi = self.target_list[i]
                xj, yj = self.target_list[j]
                dist = (xi-xj)**2+(yi-yj)**2

                if dist < currentDmin:
                    currentDmin = dist

        self.Dmin = min(math.sqrt(currentDmin), 0.001)
        print("the min distance  is ", self.Dmin)

        # This is the path for all the robots, a list of size k, each list element is a list of robot step's coordinate
        self.path = []
        for robot in self.robot_list:
            self.path.append([robot])


    # return a random shuffled list of index that represent the sequence
    # of target_list that we suppose to use in each of the learning iteration
    # from the last index, i, generate random number, j, between [0, i] include i
    # then exchange the number at index j the number at index i
    def fisherYateShuffle(self):
        arr = [_ for _ in range(self.m)]
        for i in range(self.m-1, 0, -1):
            j = random.randint(0,i)
            arr[i], arr[j] = arr[j], arr[i]
        return arr

    def neighborhoodFunction(self, t, j, alpha=0.05, G0=10, r=0.4):
        '''
        :param t: the number of iteration
        :param j: is the index for the winner
        :param alpha: is the change rate represent the computational time
        :param G0: is a non linear function, smaller with t increase
        :param r: is a small constant represent the neighbourhood
        :return: the neighborhood result (the travelling distance) of each of the K nodes (robots)
        See Eq-5 from Amin's paper from IJR&A 2006
        '''
        G = (1-alpha)**(t)*G0
        winner_x = self.wx[j]
        winner_y = self.wy[j]
        square_distance_to_winner= []
        for i in range(self.k):  # for each of the robots
            x = self.wx[i]
            y = self.wy[i]
            square_dist = (x-winner_x)**2+(y-winner_y)**2 # the squared distance from the winner robots to all the other robots
            square_distance_to_winner.append(square_dist)
        # return a list of float for how far each of the robots should move
        res = [math.exp(-1*d2/G) if d2 < r*r else 0 for d2 in square_distance_to_winner]
        return res
    def neighborhoodFunctionwithXYPosition(self, t, winnerX, winnerY, alpha=0.05, G0=10, r=0.4):
        '''
        :param t: the number of iteration
        :param j: is the index for the winner
        :param alpha: is the change rate represent the computational time
        :param G0: is a non linear function, smaller with t increase
        :param r: is a small constant represent the neighbourhood
        :return: the neighborhood result of each of the K nodes
        See Eq-5 from Amin's paper
        '''
        G = (1-alpha)**(t)*G0
        winner_x = winnerX
        winner_y = winnerY
        square_distance_to_winner= []
        for i in range(self.k):
            x = self.wx[i]
            y = self.wy[i]
            square_dist = (x-winner_x)**2+(y-winner_y)**2
            square_distance_to_winner.append(square_dist)

        res = [math.exp(-1*d2/G) if d2 < r*r else 0 for d2 in square_distance_to_winner]
        return res

    def oneStep(self, t=0, belta = 0.5):
        inputSeq = self.fisherYateShuffle()
        visited = [0]*self.k # initally, all the output neurons are not visited
        print("the input seq is ", inputSeq)
        for i in inputSeq:
            # for each input task point (x,y)
            x, y = self.target_list[i]

            # 0) calculate the distance of each j to i, dij
            dij = []
            for dummy in range(self.k):
                xj = self.wx[dummy]
                yj = self.wy[dummy]
                dij.append(math.sqrt((x-xj)**2+(y-yj)**2))
            # 1) Competition, find the not visited winner neuron, winner_index
            winner_index = 0
            winner_dist2 = float('inf')
            for j in range(self.k):
                if visited[j] == 0:
                    robx = self.wx[j]
                    roby = self.wy[j]
                    dist2 = (x-robx)*(x-robx)+(y-roby)*(y-roby)
                    if dist2 < winner_dist2:
                        winner_dist2 = dist2
                        winner_index = j

            # 2) after found the winner, mark the winner as visited
            visited[winner_index] = 1
            # 3) compute the neighbourhood function for all the output neurons
            print("the winner is robot ", winner_index, "the dist to target ", i, " is ", winner_dist2)
            neighbourhood_list = self.neighborhoodFunction(t, winner_index)
            # from the paper, if Dij is smaller than 0.5*Dmin ( the min Dis between any two targets)
            # 4) learning for all the output layer neurons
            for l in range(self.k):
                if dij[l] < 0.5*self.Dmin:
                    self.wx[l] = x
                    self.wy[l] = y
                    print(" the distance between i, j:", i, l, " is ", dij[l], ", this is smaller than ", self.Dmin)
                else:
                    constant = belta*neighbourhood_list[l]
                    self.wx[l] = self.wx[l]+constant * (x-self.wx[l])
                    self.wy[l] = self.wy[l] + constant * (y-self.wy[l])
            # Record the position change
            robot_position = [list(a) for a in zip(self.wx, self.wy)]
            for item in range(len(self.path)):
                self.path[item].append(robot_position[item])


        # return [self.wx, self.wy]

    def oneStepWhenKequalM(self, t=0, belta = 0.5):
        # in case of K equal M, all the robots will be uniquely assigned with a task
        # For every epoch, the process flow should be:
        # For every task as input:
        #     try to find a winner for it based on distance
        #     if this input was occupied already by some robot, return the robot directly
        #     else we have to find a winner for the input task
        #     but the winner need to be not arrived to other task yet,
        #     if so, choose the second winner as winner.
        #   then, for the winner and its neighbors (that are not arrived to any target yet), move the learned distance
        inputSeq = self.fisherYateShuffle()
        visited = [0]*self.k # initially, all the output neurons are not visited (all the robots are not winner yet)
        current_winner = set()
        # print("the input seq is ", inputSeq)
        for i in inputSeq:
            winner_index = 0
            winner_dist2 = float('inf')
            # for each input task point (x,y)
            x, y = self.target_list[i]
            # 0) calculate the distance of each j to i, dij
            dij = []
            for dummy in range(self.k):
                xj = self.wx[dummy]
                yj = self.wy[dummy]
                dij.append(math.sqrt((x-xj)**2+(y-yj)**2))
            sortlist = list(enumerate(dij))
            sortlist.sort(key=lambda x: x[1])  # short from dist small to big

            # 1.1) if there is a winner already, directly select this winner
            if self.taskAssigned2[i] is not None:
                continue
                winner_index = self.taskAssigned2[i]
                winner_dist2 = dij[winner_index]**2
            else:
            # 1.2) otherwise, Competition to find the not visited winner neuron, winner_index
                for ind, dis in sortlist:
                    # find the 1st robot that has not been a winner yet, and has not been assigned to a task yet,
                    if visited[ind] == 0 and self.arrived2Task[ind] == 0:
                        winner_index = ind
                        winner_dist2 = dis ** 2
                        break

            # 2) after found the winner, mark the winner as visited
            visited[winner_index] = 1
            # 3) compute the neighbourhood function for all the output neurons
            # from the paper, if Dij is smaller than 0.5*Dmin (the min Dis between any two targets)
            # we set the robot directly to the target
            # print("the winner is robot ", winner_index, "the dist to target ", i, " is ", winner_dist2)
            # if the square of the distance between the winner and the task is smaller than 0.5*self.Dmin (critical value)
            # we say the task is finally assigned to the robot, and we say the robot had already arrived to the task
            if winner_dist2 <= 0.5 * self.Dmin:
                neighbourhood_list = self.neighborhoodFunction(t, winner_index)
                self.wx[winner_index] = x
                self.wy[winner_index] = y
                self.arrived2Task[winner_index] = 1
                self.taskAssigned2[i] = winner_index
                current_winner.add(winner_index)
            else:
                neighbourhood_list = self.neighborhoodFunction(t, winner_index)

            # 4) learning (change the connecting weights) for all the output layer neurons
            for l in range(self.k):
                # if a robot arrived to a target, it will not learn anymore
                if self.arrived2Task[l] == 1:
                    continue

                if dij[l] < 0.5*self.Dmin:
                    # if a robot can arrived to a task, then, assign the robot directly to the task,
                    # and do not move it anymore (I think this code will never be runned)
                    self.wx[l] = x
                    self.wy[l] = y
                    # print(" the distance between i, j:", i, l, " is ", dij[l], ", this is smaller than ", self.Dmin)
                    self.arrived2Task[l]=1
                    self.taskAssigned2[i]=l
                # otherwise, move all the neighbourhood robots according to the neighborhood function
                # but do not move the previous winner twice
                else:
                    if l in current_winner: # do not move any previous winner in this epoch
                        constant = 0
                    else:
                        constant = belta*neighbourhood_list[l] # move accroding to the neighbourhood function
                    self.wx[l] = self.wx[l] + constant * (x-self.wx[l])
                    self.wy[l] = self.wy[l] + constant * (y-self.wy[l])
            # Record the position change
            robot_position = [list(a) for a in zip(self.wx, self.wy)]
            for item in range(len(self.path)):
                self.path[item].append(robot_position[item])


        # return [self.wx, self.wy]

    def generateRobotPath(self,tmax = 10):

        for t in range(0, tmax, 1):
            print ("============Now Print iteration ",t ,"=====================")
            self.oneStep(t)
        return self.path

    def generateRobotPathWhenKequalM(self, tmax=10):
        # loop oneStepWhenKequalM(t) until all the robots arrived to a task
        t = 0
        while True:
            # print("============Now Print iteration ", t, "=====================")
            # print("============The task assigned list is", self.taskAssigned2)
            self.oneStepWhenKequalM(t)
            t+=1
            if sum(self.arrived2Task) == self.k or t >= tmax:
                break
        return self.path

        # for t in range(0, tmax, 1):
        #     print("============Now Print iteration ", t, "=====================")
        #     print ("============The task assigned list is", self.taskAssigned2)
        #     self.oneStepWhenKequalM(t)
        # return self.path

    def calculateTravelDistance(self):
        realt = len(self.path[0])
        totalDist = 0
        for robot in range(len(self.path)):
            for index in range(realt-1):
                x1, y1 = self.path[robot][index]
                x2, y2 = self.path[robot][index+1]
                dist = ((x1-x2)**2+(y1-y2)**2)**(0.5)
                totalDist+=dist
        return totalDist





