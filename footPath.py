#Reference from Veritasium youtube video on strandbeest https://www.youtube.com/watch?v=IFaAjR_RRJs
# and https://www.diywalkers.com/python-linkage-simulator.html

import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Parameters
rotationIncrements = 800
footSweepIncrements = 5

# Output


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
axleCenter = [0, 10.0]
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

# Calculate joint positions for each frame
jointx=[]
jointy=[]

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

    j= j_7[counter]
    

    jointx.append(j[0])
    jointy.append(j[1])

def calculate(jointx,jointy): 
    k=[0,0,0,0]  # x_min, x_max, y_min, y_max   
    k[0]=max(jointx) # ensures minimum condition triggered
    k[1]=min(jointx) # ensures maximum condition triggered
    k[2]=min(jointy)
    k[3]=max(jointy)
    n=len(jointy)

    for i in range(n):
        if (abs(jointy[i]-k[2])  < 0.09):
            if(jointx[i]<k[0]): k[0]= jointx[i]

            if(jointx[i]>k[1]):k[1]= jointx[i]


    stride= k[1]-k[0]
    height= k[3]-k[2]
    return stride,height,k

# Plot setup
def plot_footpath(x_positions, y_positions):
    stride, height, limits = calculate(x_positions, y_positions)

    plt.figure(figsize=(8, 6))
    plt.plot(x_positions, y_positions, 'r', label="Footpath")
    plt.axhline(y=limits[2], color='gray', linestyle='--', label="Height Limits")
    plt.axhline(y=limits[3], color='gray', linestyle='--')
    plt.axvline(x=limits[0], color='green', linestyle='--', label="Stride Limits")
    plt.axvline(x=limits[1], color='green', linestyle='--')

    # Annotate stride and height on the plot
    plt.text((limits[0] + limits[1]) / 2, (limits[2] + limits[3]) / 2, 
             f"Stride: {stride:.2f}", color='green', fontsize=12, ha='center')
    plt.text(limits[1] + 5, (limits[2] + limits[3]) / 2, 
             f"Height: {height:.2f}", color='gray', fontsize=12, va='center', rotation=90)

    plt.title("Strandbeest Footpath")
    plt.xlabel("Horizontal Position")
    plt.ylabel("Vertical Position")
    plt.legend()
    plt.grid()
    plt.show()


reslt=calculate(jointx,jointy)
print('Stride=',reslt[0],'\nHeight=',reslt[1])
plot_footpath(jointx,jointy)
