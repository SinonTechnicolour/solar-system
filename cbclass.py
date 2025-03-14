import numpy as np
from datetime import datetime
from datetime import timedelta
import requests

class celestialbody:
    def __init__(self, name, mass, currentpos, velocity, vectorforce, horizonid, point):
        self.name = name
        self.mass = mass
        self.currentpos = currentpos
        self.velocity = velocity
        self.vectorforce = vectorforce
        self.horizonid = horizonid
        self.point = point 

    
    # Acceleration is proportional to mass, Newtons Force = mass * acceleration
    @property
    def acceleration(self): 
        return (self.vectorforce / self.mass)
    
    #returns magnitude () 
    def getmagnitude(self, secondbodyposition):
        distance = secondbodyposition - self.currentpos
        return np.linalg.norm(distance)

    def getunitvector(self, magnitude, secondbodyposition):
        return ((secondbodyposition - self.currentpos)/magnitude)
    
    def twobodyforce(self, gravity, secondbodymass, secondbodyposition): 
        magnitude = self.getmagnitude(secondbodyposition)
        absoluteforce = (gravity * self.mass * secondbodymass)/np.square(magnitude)
        twobodyvectorforce = absoluteforce * (self.getunitvector(magnitude, secondbodyposition)) 
        return twobodyvectorforce
    
    #For clarity of code, This function just returns values and then update pos and vel from main.py
    def updatepositionandvelocity(self, timestep):
        # application of constant acceleration formulae
        nextposition = (self.currentpos) + (self.velocity*timestep) + (0.5*self.acceleration*(np.square(timestep)))
        nextvelocity = (self.velocity) + (self.acceleration*timestep)
       # return nextposition, nextvelocity
        self.currentpos = nextposition
        self.velocity = nextvelocity





    def getstartpositionandvelocity(self): 
        def splitstring(s, start, end):
            p1, p2 = s.split(start,1)
            result = p2.split(end, 1)[0]
            print(result)
            return result
    
        datetoday = datetime.now()
        datetomorrow = datetime.now() + timedelta(days=1)
        url=f"https://ssd.jpl.nasa.gov/api/horizons.api?format=json&COMMAND='{self.horizonid}'&OBJ_DATA='NO'&MAKE_EPHEM='YES'&EPHEM_TYPE='VECTORS'&CENTER='500@0'&START_TIME='{datetoday}'&STOP_TIME='{datetomorrow}'&STEP_SIZE='1d'&QUANTITIES='1,9,20,23,24,29'"
        response = requests.post(url)
        responsejson = response.json()
        if response.ok: 
            print("connected to nasa")
        
            stringresponse = responsejson["result"]
        else:
            print("accessing local json")
    
        data = splitstring(stringresponse, "$$SOE",  "$$EOE")

        positionvectors = data.splitlines()[2]
        velocityvectors = data.splitlines()[3]
        x = float(splitstring(positionvectors, "X ="," Y"))
        y = float(splitstring(positionvectors, "Y ="," Z"))
        z = float(positionvectors.split("Z =",1)[1])
        print(z)
        vx = float(splitstring(velocityvectors, "VX="," VY"))
        vy = float(splitstring(velocityvectors, "VY="," VZ"))
        vz = float(velocityvectors.split("VZ=",1)[1])
        print(vz)
        
        self.currentpos = (np.array([x,y,z]))*1000
        self.velocity = (np.array([vx,vy,vz]))*1000

        print(self.currentpos)
        print(self.velocity)

        
    
    def printbodyattributes(self):
        print(f"Name: {self.name}\n Mass: {self.mass}\n Position: {self.currentpos}\n Velocity: {self.velocity}\n Force on object: {self.vectorforce}")

class Moon(celestialbody):
    def __init__(self, name, currentpos, mass, velocity, force, orbits):
        super().__init__(name, currentpos, mass, velocity, force)
        self.orbits = orbits

