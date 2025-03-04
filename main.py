import numpy as np
import matplotlib as mpl
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
earth = cb("Earth", 5.972e24, np.array([-1352.755691812412E+08, 6116.401076129713E+07, 02353.456791794300E+04]), np.array([-1294.302096212603E+01, -2717.804952151386E+01, 1019.574352167041E-03]), np.array([0,0,0]), None)
sun = cb("Sun",1.989e30, np.array([-7988.634901289927E+05, -7614.964374967902E+05, 2587.556848305213E+04]), np.array([1260.082195736638E-02,-5184.066937527316E-03,-2144.536918918256E-04]), np.array([0,0,0]), None)
mars = cb("Mars", 6.39e23, np.array([-1705.078259658501E+08,1788.722506792968E+08,7952.027070522420E+06]), np.array([-1668.708010363948E+01,-1457.869007509080E+01,1039.081377919446E-01]),np.array([0,0,0]), None)
jupiter = cb("Jupiter", 1.898e27, np.array([9633.709630487323E+07,7560.505171162552E+08,-5291.122383421361E+06]), np.array([-1311.001435573838E+01,-2274.558735522654E+00,2839.620649828056E-01]),np.array([0,0,0]), None)
saturn = cb("Saturn", 5.683e26, np.array([1419.598919083191E+09,-2203.911047869837E+08,-5268.942960872686E+07]), np.array([9460.734979374144E-01,9526.091133604890E+00,-2038.630813215390E-01]),np.array([0,0,0]), None)
neptune = cb("Neptune", 1.024e26, np.array([4469.418935171612E+09,-7010.303460947002E+07,-1015.587249056920E+08]), np.array([4880.340580428192E-02,5466.147716575340E+00,-1138.608711271414E-01]),np.array([0,0,0]), None)
mercury = cb("Mercury", 3.285e23, np.array([4348.792498208769E+07,2058.483406643132E+07,-2291.706994364512E+06]), np.array([-3063.033163261347E+01,4602.719001738175E+01,6572.234092009960E+00]),np.array([0,0,0]), None)
venus = cb("Venus", 4.867e24, np.array([-8106.652093903564E+07,7050.194242102133E+07,5636.055420686472E+06]), np.array([-2336.771886321154E+01,-2637.525908067103E+01,9866.649505096099E-01]),np.array([0,0,0]), None)
uranus =  cb("Uranus", 8.681e25, np.array([1633.738109797280E+09,2423.385637297977E+09,-1216.497248135650E+07]), np.array([-5696.890576773002E+00,3489.307038044661E+00,8654.868535910132E-02]),np.array([0,0,0]), None)

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
ax.set_xlim3d(-5e11, 5e11)
ax.set_ylim3d(-5e11, 5e11)
ax.set_zlim3d(-5e11, 5e11)

#ax.set_box_aspect((100, 100, 100))

for key in cbspoints.keys():
        key.point, = ax.plot([key.currentpos[0]],[key.currentpos[1]],[key.currentpos[2]], marker="o" )
        print(key.point,)

#square to help guide where middle is 
ax.plot(0,0,0, marker = "s")
newpoint, = ax.plot([1],[1],[1], marker="o")
print(newpoint)
#updates the position of the point based on the frame, each frame gives the next value in the x, y and z axis
def update_points(frames, cbspoints, listofcbs, timestep, gravity):
    print(frames)
    listofcbs = addallforcesbetweenplanetstodict(gravity, listofcbs)
    updatecbspositionandvelocity(listofcbs, timestep)
  
    for key in cbspoints.keys(): 
        print(frames)
        key.printbodyattributes()
        print(f"loop {frames}")
        (key.point).set_data([key.currentpos[0]],[key.currentpos[1]])
        (key.point).set_3d_properties(key.currentpos[2])

# Add labels to axis and graph title 
ax.set_title('Example')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Show

ani=animation.FuncAnimation(fig, update_points,interval = 0.5, frames = 10000000, fargs=(cbspoints, cbsforces, t, gravity))
plt.show()
