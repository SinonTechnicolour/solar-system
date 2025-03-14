import pyforms
from cbclass import celestialbody as cb
from simulation import simulation
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlText
from pyforms.controls import ControlButton
from pyforms.controls import ControlCombo
import numpy as np

import matplotlib
matplotlib.use("TKCairo")

class ChangeBodyValues(BaseWidget):
    def __init__(self, planet):
        super(ChangeBodyValues,self).__init__('Manipulate Values')
        self.planet = planet
        self._massmult = ControlText("Mass Multiplier: ", default = "1")
        self._velocitymult = ControlText("Velocity Multiplier: ", default = "1")
        self.closeEvent = self._applyChanges
        self.formset = [
            'h1: Change Values:',
            ' enter numbers only, if this is not upheld window will close  \n  without updating values',
            '_massmult',
            '_velocitymult',
            
        ]
    def _applyChanges(self, close):
        try:
            self.planet.mass = np.multiply(self.planet.mass, int(self._massmult.value))
            self.planet.velocity = np.multiply(self.planet.velocity, int(self._velocitymult.value))
            self.planet.printbodyattributes()

        except:
            print(int(self._massmult.value))



class SolarSim(BaseWidget):
    earth = cb("Earth", 5.972e24, np.array([0,0,0]), np.array([0,0,0]), np.array([0,0,0]),399, None)
    sun = cb("Sun",1.989e30, np.array([0,0,0]), np.array([0,0,0]), np.array([0,0,0]),10, None)
    mars = cb("Mars", 6.39e23, np.array([0,0,0]), np.array([0,0,0]),np.array([0,0,0]),499, None)
    jupiter = cb("Jupiter", 1.898e27, np.array([0,0,0]), np.array([0,0,0]),np.array([0,0,0]),599, None)
    saturn = cb("Saturn", 5.683e26, np.array([0,0,0]), np.array([0,0,0]),np.array([0,0,0]),699, None)
    neptune = cb("Neptune", 1.024e26, np.array([0,0,0]), np.array([0,0,0]),np.array([0,0,0]),899, None)
    mercury = cb("Mercury", 3.285e23, np.array([0,0,0]), np.array([0,0,0]),np.array([0,0,0]),199, None)
    venus = cb("Venus", 4.867e24, np.array([0,0,0]), np.array([0,0,0]),np.array([0,0,0]),299, None)
    uranus =  cb("Uranus", 8.681e25, np.array([0,0,0]), np.array([0,0,0]),np.array([0,0,0]),70, None)
    

    #dictionary of cbs
    cbs = {
        sun:{},
        mercury:{},
        venus:{},
        earth:{},
        mars:{},
        jupiter:{},
        saturn:{},
        neptune:{},
        uranus:{}
    }

    for key in list(cbs.keys()):
        key.getstartpositionandvelocity()

    def __init__(self):
        super(SolarSim,self).__init__('Solar System Simulator')

        
        self._grav = ControlText('Strength of Gravity Multiplier',default = "1")
        self._frames = ControlText('Simulation Length (in frames drawn)',default = "200")
        self._choosebodytochange = ControlCombo()
        self._viewwindow = ControlCombo()
        self._updatevalues = ControlButton('Update')
        self._updatevalues.value = self.__inputDialogue
        
 
        # adds planets as selectable option and has a corresponding view window value that gets passed to simulation dependant on which planet gets selected e.g "Mercury" --> 5.25e10
        # considered adding view window property to cbclass but felt it wasn't that much more efficient of an implementation
        self._viewwindow.add_item("Mercury", 5.25e10)
        self._viewwindow.add_item("Venus", 6.75e10)
        self._viewwindow.add_item("Earth", 1e11)
        self._viewwindow.add_item("Mars", 2e11)
        self._viewwindow.add_item("Jupiter",7.5e11)
        self._viewwindow.add_item("Saturn",1.5e12)
        self._viewwindow.add_item("Uranus",2.5e12)
        self._viewwindow.add_item("Neptune",4.3e12)
        
        # adds values to the _choosebodytochange dropdown, key.name is the name of the body put into the selector for the user, key is the body that corresponds to the name
        # that gets passed into the constructor of the ChangeBodyValues window
        for key in list(self.cbs.keys()):
            self._choosebodytochange.add_item(key.name, key)     

        #runs simulation on close (executes _executeSim function)
        self.closeEvent = self._executeSim

        
        self.formset = [
            'h1:  Solar System Simulator',
            "  Welcome! Close this window to begin simulation with chosen values. If you don't  \n  change any values the default values are used which are pulled directly from NASA Horizons API  \n   \n\n Enter numbers only or simulation will not be drawn  ",
            '_grav',
            '_frames',
            'Select from the dropdown a planet to change the mass or velocity properties of',
            ('_choosebodytochange','_updatevalues'),
            'Choose the view window through which you wish to view the simulation. Planet specified is the outermost FULL orbit visible in the simulation plot',
            '_viewwindow',
            
        ]
        
    def __inputDialogue(self):
        self._choosebodytochange.value.printbodyattributes()
        win = ChangeBodyValues(self._choosebodytochange.value)
        win.parent = self
        win.show()
    
    def _executeSim(self, closed):
        
        finalgravvalue = (np.multiply(int(self._grav.value), 6.6743e-11))
        endpoint = int(self._frames.value)
        finalsimulation = simulation(self.cbs, self._viewwindow.value, finalgravvalue,endpoint, 100)
        finalsimulation.runsimulation()
  




#opening a window (instantiating SolarSim class)
pyforms.start_app( SolarSim, geometry = (210,210,210,210 ) )


