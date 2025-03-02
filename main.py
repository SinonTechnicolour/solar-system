import numpy as np
from matplotlib import pyplot as plt
import matplotlib.animation as animation
from cbclass import celestialbody as cb #cb stands for celestial bodies throughout this project. 
from cbclass import Moon as m

print("hello world")

#takes the value of gravity in use and the list of celestialbodies and adds the forces to the list of bodies
def addallforcesbetweenplanetstodict(gravityvalue, listofcbs): 
    listofcbs = {
    earth:{},
    sun:{},
    mars:{},
    jupiter:{},
    saturn:{},
    neptune:{},
    mercury:{},
    venus:{},
    uranus:{}
    }
    for i, bodyi in enumerate(listofcbs.keys()):
        j = i+1
        for bodyj in list(listofcbs.keys())[i+1:]:
            if bodyi.name == bodyj.name:
                pass
            else:
                print(i, j, bodyi, bodyj)
                listofcbs[bodyi][j]=bodyi.twobodyforce(gravityvalue, bodyj.mass, bodyj.currentpos) 
                listofcbs[bodyj][i]=(-1*(listofcbs[bodyi][i+1]))
                j+=1
    return listofcbs

#updates the position and velocity attributes within discrete examples of the cb class based on force, takes a list with all cbs as input
def updatecbspositionandvelocity(listofcbs, timestep):
    for key in listofcbs.keys():
        key.currentcombinedforce = np.array([0,0,0])
        for value in listofcbs[key]:
            key.currentcombinedforce = np.add(key.currentcombinedforce,listofcbs[key][value])
        
        key.currentpos, key.velocity = key.updatepositionandvelocity(timestep)
        
#to be called by mpl    
def simulate(listofcbs, timestep, gravity):
    listofcbs = addallforcesbetweenplanetstodict(gravity, listofcbs)
    updatecbspositionandvelocity(listofcbs, timestep)
        


#START VALUES FOR X,Y,Z and VX,VY,VZ from NASA Horizons API
#example format for cb class: planetname = cb("planetname, mass, currentpos, velocity, force")
earth = cb("Earth", 5.972e24, np.array([-1.352755691812412E+08, 6.116401076129713E+07, 02.353456791794300E+04]), np.array([-1.294302096212603E+01, -2.717804952151386E+01, 1.019574352167041E-03]), np.array([0,0,0]))
sun = cb("Sun",1.989e30, np.array([-7.988634901289927E+05, -7.614964374967902E+05, 2.587556848305213E+04]), np.array([1.260082195736638E-02,-5.184066937527316E-03,-2.144536918918256E-04]), np.array([0,0,0]))
mars = cb("Mars", 6.39e23, np.array([-1.705078259658501E+08,1.788722506792968E+08,7.952027070522420E+06]), np.array([-1.668708010363948E+01,-1.457869007509080E+01,1.039081377919446E-01]),np.array([0,0,0]))
jupiter = cb("Jupiter", 1.898e27, np.array([9.633709630487323E+07,7.560505171162552E+08,-5.291122383421361E+06]), np.array([-1.311001435573838E+01,-2.274558735522654E+00,2.839620649828056E-01]),np.array([0,0,0]))
saturn = cb("Saturn", 5.683e26, np.array([1.419598919083191E+09,-2.203911047869837E+08,-5.268942960872686E+07]), np.array([9.460734979374144E-01,9.526091133604890E+00,-2.038630813215390E-01]),np.array([0,0,0]))
neptune = cb("Neptune", 1.024e26, np.array([4.469418935171612E+09,-7.010303460947002E+07,-1.015587249056920E+08]), np.array([4.880340580428192E-02,5.466147716575340E+00,-1.138608711271414E-01]),np.array([0,0,0]))
mercury = cb("Mercury", 3.285e23, np.array([4.348792498208769E+07,2.058483406643132E+07,-2.291706994364512E+06]), np.array([-3.063033163261347E+01,4.602719001738175E+01,6.572234092009960E+00]),np.array([0,0,0]))
venus = cb("Venus", 4.867e24, np.array([-8.106652093903564E+07,7.050194242102133E+07,5.636055420686472E+06]), np.array([-2.336771886321154E+01,-2.637525908067103E+01,9.866649505096099E-01]),np.array([0,0,0]))
uranus =  cb("Uranus", 8.681e25, np.array([1.633738109797280E+09,2.423385637297977E+09,-1.216497248135650E+07]), np.array([-5.696890576773002E+00,3.489307038044661E+00,8.654868535910132E-02]),np.array([0,0,0]))

# base strength of gravity (real world value)
bsg=6.6743e-11
# gravity variable to be changed by user as necessary
gravity=bsg 

# default timestep
defaulttimestep = 100000
# timestep
t = defaulttimestep

# base dict for all planets that forces get added to 
basecbs = {
    earth:{},
    sun:{},
    mars:{},
    jupiter:{},
    saturn:{},
    neptune:{},
    mercury:{},
    venus:{},
    uranus:{}
}

# dict for forces
cbsforces = basecbs
cbsforces=  addallforcesbetweenplanetstodict(gravity, cbsforces)
updatecbspositionandvelocity(cbsforces, t )
#dict with points to be plotted by mpl
cbspoints = basecbs

#mpl
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.set_xlim3d(-2e16, 2e16)
ax.set_ylim3d(-2e16, 2e16)
ax.set_zlim3d(-2e16, 2e16)

for key in cbspoints.keys(): 
        point, = ax.plot(key.currentpos[0],key.currentpos[1],key.currentpos[2], marker="o" )
        cbspoints[key] = point, 

#square to help guide where middle is 
ax.plot(0,0,0, marker = "s")


#updates the position of the point based on the frame, each frame gives the next value in the x, y and z axis
i=0
def update_points(frames, cbspoints, listofcbs, timestep, gravity):
    #simulate(listofcbs, timestep, gravity)
    listofcbs = addallforcesbetweenplanetstodict(gravity, listofcbs)
    updatecbspositionandvelocity(listofcbs, timestep)
    for key in cbspoints.keys(): 
        print(frames)
        print(cbspoints[key])
        cbspoints[key].set_data([key.currentpos[0]],[key.currentpos[1]])
        cbspoints[key].set_3d_properties([key.currentpos[2]])

# Add labels to axis and graph title 
ax.set_title('Example')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Show

ani=animation.FuncAnimation(fig, update_points,interval = 0.001, frames = 10000000, fargs=(cbspoints, cbsforces, t, gravity))
plt.show()
