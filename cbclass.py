import numpy as np
class celestialbody:
    def __init__(self, name, mass, currentpos, velocity, currentcombinedforce, point):
        self.name = name
        self.mass = mass
        self.currentpos = currentpos
        self.velocity = velocity
        self.currentcombinedforce = currentcombinedforce
        self.point = point 

    
    # Acceleration is proportional to mass, Newtons Force = mass * acceleration
    @property
    def acceleration(self): 
        return (self.currentcombinedforce / self.mass)
    
    #returns magnitude () 
    def getmagnitude(self, secondbodyposition):
        distance = secondbodyposition - self.currentpos
        return np.linalg.norm(distance)

    def getunitvector(self, magnitude, secondbodyposition):
        return ((secondbodyposition - self.currentpos)/magnitude)
    
    def twobodyforce(self, gravity, secondbodymass, secondbodyposition): 
        magnitude = self.getmagnitude(secondbodyposition)
        absoluteforce = (gravity * self.mass * secondbodymass)/np.square(magnitude)
        vectorforce = absoluteforce * (self.getunitvector(magnitude, secondbodyposition)) 
        return vectorforce
    
    #For clarity of code, This function just returns values and then update pos and vel from main.py
    def updatepositionandvelocity(self, timestep):
        nextposition = (self.currentpos) + (self.velocity*timestep) + (0.5*self.acceleration*(np.square(timestep)))
        nextvelocity = (self.velocity) + (self.acceleration*timestep)
        return nextposition, nextvelocity
    
    def printbodyattributes(self):
        print(f"Name: {self.name}\n Mass: {self.mass}\n Position: {self.currentpos}\n Velocity: {self.velocity}\n Force on object: {self.currentcombinedforce}")

class Moon(celestialbody):
    def __init__(self, name, currentpos, mass, velocity, force, orbits):
        super().__init__(name, currentpos, mass, velocity, force)
        self.orbits = orbits

