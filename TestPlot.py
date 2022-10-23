import matplotlib.pyplot as plt
import numpy as np

# Draw a Fig First
fig  = plt.figure(num=1, figsize=(4,4))

# plt.plot() interface does not orientate to any object, it is a state-based interface
# figure and axes are OOP based interface
# axes = plt.subplot(221) # This returns a axes object on a default (or last called) Figure Object
# fig, axe = plt.subplots(3,3) # This returns a Figure object as well as a ndarray object
# plt.subplot(334) # use subplot method to create a subplot at #4 Position if the last called Fig is seperated as 2x2
# plt.plot([1,2,3,4,5],[2,4,9,16,25]) # plt always draw on the last called instance, which is a subplot(334)
# axes.plot([2,1])
# plt.show()

ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)
ax1.plot([1,2])
ax2.plot([1,1])
plt.show()