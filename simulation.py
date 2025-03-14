import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
import matplotlib.animation as animation
from cbclass import celestialbody as cb #cb stands for celestial bodies throughout this project. 
from cbclass import Moon as m

print("hello world")

class simulation:
    def __init__(self, basecbs, viewwindow, gravity, frames, howmanycalcsskipped):
        self.basecbs = basecbs
        self.viewwindow = viewwindow
        self.gravity = gravity
        self.frames = frames 
        self.howmanycalcsskipped = howmanycalcsskipped

    @staticmethod
    def addallforcesbetweenplanetstodict(gravityvalue, listofcbs): 
            for i, bodyi in enumerate(listofcbs.keys()):
                j = i+1
                for bodyj in list(listofcbs.keys())[i+1:]:
                    listofcbs[bodyi][j]=bodyi.twobodyforce(gravityvalue, bodyj.mass, bodyj.currentpos) 
                    listofcbs[bodyj][i]=(-1*(listofcbs[bodyi][j]))
                    j+=1
            return listofcbs
    
    #updates the position and velocity attributes within discrete examples of the cb class based on force, takes a list with all cbs as input
    @staticmethod
    def updatecbspositionandvelocity(listofcbs, timestep):
        for key in listofcbs.keys():
            # resets contents of vector force array 
            key.vectorforce = np.array([0,0,0])
            for value in listofcbs[key]:
                key.vectorforce = np.add(key.vectorforce,listofcbs[key][value])
            key.updatepositionandvelocity(timestep)
    
    def runsimulation(self):
        #takes the value of gravity in use and the list of celestialbodies and adds the forces to the list of bodies

        #timestep
        t = 1000

        # dict for forces
        cbsforces = self.basecbs
        cbsforces=  self.addallforcesbetweenplanetstodict(self.gravity, cbsforces)
        self.updatecbspositionandvelocity(cbsforces, t )
        #dict with points to be plotted by mpl
        cbspoints = self.basecbs

        #mpl
        fig = plt.figure()

        ax = fig.add_subplot(projection='3d')
        ax.set_xlim3d(-self.viewwindow, self.viewwindow)
        ax.set_ylim3d(-self.viewwindow, self.viewwindow)
        ax.set_zlim3d(-self.viewwindow, self.viewwindow)

        for key in cbspoints.keys():
                key.point, = ax.plot([key.currentpos[0]],[key.currentpos[1]],[key.currentpos[2]], marker="o" )
                print(key.point,)


        #updates the position of the point based on the frame, each frame gives the next value in the x, y and z axis
        def update_points(frames, cbspoints, listofcbs, timestep, gravity, endpoint):

            for i in range(self.howmanycalcsskipped):
                
                listofcbs = self.addallforcesbetweenplanetstodict(gravity, listofcbs)
                self.updatecbspositionandvelocity(listofcbs, timestep)


            for key in cbspoints.keys(): 
                key.printbodyattributes()
                print(f"loop {frames}")
                (key.point).set_data([key.currentpos[0]],[key.currentpos[1]])
                (key.point).set_3d_properties(key.currentpos[2])

            if frames == endpoint:
                plt.close()
            
            return update_points

        # Add labels to axis and graph title 
        ax.set_title('Solar System Sim')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        # Show
        ani=animation.FuncAnimation(fig, update_points,interval = 0.5, frames = 10000000, fargs=(cbspoints, cbsforces, t, self.gravity, self.frames))
        plt.show()
