#Reference from Veritasium youtube video on strandbeest https://www.youtube.com/watch?v=IFaAjR_RRJs
# and https://www.diywalkers.com/python-linkage-simulator.html

import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Parameters
rotationIncrements = 500
footSweepIncrements = 2

# Bar lengths (from Youtube video)
bar_a = 38
bar_b = 41.5
bar_c = 39.3
bar_d = 40.1
bar_e = 55.8
bar_f = 39.4
bar_g = 36.7
bar_h = 65.7
bar_i = 49
bar_j = 50
bar_k = 61.9
bar_l = 7.8
bar_m = 15


# Fixed points
axleCenter = [0, 10]
joint_0= [axleCenter[0], axleCenter[1]+ bar_l]
joint_3 = [axleCenter[0] - bar_a, axleCenter[1]]

# Joint dictionaries
j_0 = {}
j_1 = {}
j_2 = {}
j_3 = {}
j_4 = {}
j_5 = {}
j_6 = {}
j_7 = {}


# Store x and y values for animation
xVals = {}
yVals = {}

# Intersection function
def circIntersection(jointA, jointB, lengthA, lengthB, intersectionNum):
    xPos_a, yPos_a = jointA
    xPos_b, yPos_b = jointB
    Lc = math.sqrt((xPos_a - xPos_b)**2 + (yPos_a - yPos_b)**2)
    bb = ((lengthB**2) - (lengthA**2) + (Lc**2)) / (2 * Lc)
    h = math.sqrt((lengthB**2) - (bb**2))
    Xp = xPos_b + (bb * (xPos_a - xPos_b)) / Lc
    Yp = yPos_b + (bb * (yPos_a - yPos_b)) / Lc
    Xsolution1 = Xp + (h * (yPos_b - yPos_a)) / Lc
    Ysolution1 = Yp - (h * (xPos_b - xPos_a)) / Lc
    Xsolution2 = Xp - (h * (yPos_b - yPos_a)) / Lc
    Ysolution2 = Yp + (h * (xPos_b - xPos_a)) / Lc

    solutions = [[Xsolution1, Ysolution1], [Xsolution2, Ysolution2]]
    if intersectionNum == 0:                        #top intersection
        return max(solutions, key=lambda s: s[1])
    elif intersectionNum == 1:                      #bottom intersection
        return min(solutions, key=lambda s: s[1])
    elif intersectionNum == 2:                      #left-most intersection
        return min(solutions, key=lambda s: s[0])
    else:                                           #right-most intersection
        return max(solutions, key=lambda s: s[0])

# Split x and y values for plotting
def splitXY(i):
    xValues = []
    yValues = []
    joints = [j_0, j_1, j_2, j_3, j_4, j_5, j_6, j_7, j_5,j_4, j_2, j_3, j_6, j_1] #this order determines the lines connected
   
    for joint in joints:
        xValues.append(joint[str(i)][0])
        yValues.append(joint[str(i)][1])
    return [xValues, yValues]

# Calculate joint positions for each frame
for i in range(rotationIncrements):
    theta = (i / (rotationIncrements - 1)) * 2 * math.pi  #clockwise
    # theta = -(i / (rotationIncrements - 1)) * 2 * math.pi #anti-clockwise
    
    crankX = math.cos(theta) * bar_m
    crankY = math.sin(theta) * bar_m
    joint_1_at_theta = [crankX + joint_0[0], crankY + joint_0[1]]
    counter = str(i)

    j_0[counter] = [joint_0[0], joint_0[1]]
    j_3[counter] = [joint_3[0], joint_3[1]]
    j_1[counter] = joint_1_at_theta
    j_2[counter] = circIntersection(j_1[counter], j_3[counter], bar_j, bar_b, 0)
    j_6[counter] = circIntersection(j_1[counter], j_3[counter], bar_k, bar_c, 1) 
    j_4[counter] = circIntersection(j_2[counter], j_3[counter], bar_e, bar_d, 2)
    j_5[counter] = circIntersection(j_4[counter], j_6[counter], bar_f, bar_g, 2)
    j_7[counter] = circIntersection(j_5[counter], j_6[counter], bar_h, bar_i, 1)
    
    vals = splitXY(i)
    xVals[counter] = vals[0]
    yVals[counter] = vals[1]

# Plot setup
xlow, xhigh, ylow, yhigh = -120, 75, -80, 80
fig = plt.figure(figsize=(8, 8))
fig.set_facecolor('#f0f8ff')
ax = plt.axes(xlim=(xlow, xhigh), ylim=(ylow, yhigh))
ax.set_title("Strandbeest", fontsize=18)
line, = ax.plot([], [], '-o', ms=7, lw=3, mfc='cyan', color='black')

# Initialize function
def init():
    line.set_data([], [])
    return line,

# Animation function
def animate(i):
    line.set_data(xVals[str(i)], yVals[str(i)])
    return line,

# Animate
ani = animation.FuncAnimation(fig, animate, frames=rotationIncrements, interval=0, blit=True, init_func=init)
plt.show()

