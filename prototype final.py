import numpy as np
from matplotlib import pyplot as plt
import matplotlib.animation as animation


def getforce(bigg, earthmass, sunmass, unitvector, magnitudevector):
    absoluteforce = (bigg * earthmass * sunmass)/np.square(magnitudevector)
    vectorforce = absoluteforce* -1 * (unitvector)
    return vectorforce

def getnextpositionandvelocity(earthpos, earthvel, timestep, a):
    nextpos = earthpos + (earthvel*timestep) + (0.5*a*(np.square(timestep)))
    nextvel = earthvel + a*timestep
    return nextpos, nextvel 

bigg = 6.6743e-11

earthstart = np.array([148.24e9,0,0])

earthmass = 5.972e24
earthstartvel = np.array([0,0,29.78e3])
sunmass = 1.989e30
sunpos = [0, 0, 0]

#vars that change
earthpos = earthstart
earthvel = earthstartvel


magnitudevector = np.linalg.norm(earthpos)
unitvector = earthpos / magnitudevector 
print(earthpos)
print(magnitudevector)


a = (getforce(bigg, earthmass, sunmass, unitvector, magnitudevector))/earthmass
print(a)



listofpositions = np.array([[148.24e9,0,0]])


for i in range(100000):
    earthpos, earthvel = getnextpositionandvelocity(earthpos, earthvel,1000, a)
    magnitudevector = np.linalg.norm(earthpos)
    unitvector = earthpos / magnitudevector 
    a = (getforce(bigg, earthmass, sunmass, unitvector, magnitudevector))/earthmass
    if (i % 10) == 0:
        
        listofpositions = np.concatenate((listofpositions, [earthpos]), axis=0)






fig = plt.figure()
ax = fig.add_subplot(projection='3d')


ax.set_xlim3d(-2e11, 2e11)
ax.set_ylim3d(-100, 100)
ax.set_zlim3d(-2e11, 2e11)

# first position for the moving point, has a line that shows the full trajectory
ax.plot(0,0,0, marker = "s")
point, = ax.plot([listofpositions[0][0]],[listofpositions[0][1]],[listofpositions[0][2]], marker="o" )

#updates the position of the point based on the frame, each frame gives the next value in the x, y and z axis
i=0
def update_point(n, xyz, i,  point):
    if(n%3 == 0):
        i = n 
    if(n%3 == 1):
        i = n+2
    if(n%3==2):
        i = n + 1 


    point.set_data([xyz[i][0]],[xyz[i+1][1]])
    point.set_3d_properties([xyz[i+2][2]])
    
    return 0

# Add labels to axis and graph title 
ax.set_title('Example')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Show

ani=animation.FuncAnimation(fig, update_point,interval = 0.001, frames = 10000000, fargs=(listofpositions, i, point))

plt.show()










    

