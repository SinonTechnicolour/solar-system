import numpy as np
class celestialbody:
    def __init__(self, name, mass, currentpos, velocity, currentcombinedforce):
        self.name = name
        self.mass = mass
        self.currentpos = currentpos
        self.velocity = velocity
        self.currentcombinedforce = currentcombinedforce 

    
    
    
    
    # Acceleration is proportional to mass, Newtons Force = mass * acceleration
    @property
    def acceleration(self): 
        return (self.currentcombinedforce / self.mass)
    
    def getmagnitude(self, secondposition):
        return np.sqrt(np.square(secondposition) + np.square(self.currentpos))

    def getunitvector(self, magnitudevector):
        return (self.currentpos/magnitudevector)
    
    def twobodyforce(self, gravity, secondbodymass, secondbodyposition): 
        magnitudevector = self.getmagnitudevector(secondbodyposition)
        absoluteforce = (gravity * self.mass * secondbodymass)/np.square(magnitudevector)
        vectorforce = absoluteforce * (self.getunitvector(magnitudevector)) * -1
        return vectorforce
    
    #For clarity of code, This function just returns values and then update pos and vel from main.py
    def updatepositionandvelocity(self, timestep):
        nextposition = (self.currentpos) + (self.velocity*timestep) + (0.5*self.acceleration*(np.square(timestep)))
        nextvelocity = (self.velocity) + (self.acceleration*timestep)
        return nextposition, nextvelocity
    
    def printbodyattributes(self):
        print(f"Name: {self.name}\n Mass: {self.mass}\n Position: {self.currentpos}\n Velocity: {self.velocity}\n Force on object: {self.currentcombinedforce}")
        return 0 


class Moon(celestialbody):
    def __init__(self, name, currentpos, mass, velocity, force, orbits):
        super().__init__(name, currentpos, mass, velocity, force)
        self.orbits = orbits


