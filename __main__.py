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

    earth = cb("Earth", 5.972e24, np.array([-1352.755691812412E+08, 6116.401076129713E+07, 02353.456791794300E+04]), np.array([-1294.302096212603E+01, -2717.804952151386E+01, 1019.574352167041E-03]), np.array([0,0,0]), None)
    sun = cb("Sun",1.989e30, np.array([-7988.634901289927E+05, -7614.964374967902E+05, 2587.556848305213E+04]), np.array([1260.082195736638E-02,-5184.066937527316E-03,-2144.536918918256E-04]), np.array([0,0,0]), None)
    mars = cb("Mars", 6.39e23, np.array([-1705.078259658501E+08,1788.722506792968E+08,7952.027070522420E+06]), np.array([-1668.708010363948E+01,-1457.869007509080E+01,1039.081377919446E-01]),np.array([0,0,0]), None)
    jupiter = cb("Jupiter", 1.898e27, np.array([9633.709630487323E+07,7560.505171162552E+08,-5291.122383421361E+06]), np.array([-1311.001435573838E+01,-2274.558735522654E+00,2839.620649828056E-01]),np.array([0,0,0]), None)
    saturn = cb("Saturn", 5.683e26, np.array([1419.598919083191E+09,-2203.911047869837E+08,-5268.942960872686E+07]), np.array([9460.734979374144E-01,9526.091133604890E+00,-2038.630813215390E-01]),np.array([0,0,0]), None)
    neptune = cb("Neptune", 1.024e26, np.array([4469.418935171612E+09,-7010.303460947002E+07,-1015.587249056920E+08]), np.array([4880.340580428192E-02,5466.147716575340E+00,-1138.608711271414E-01]),np.array([0,0,0]), None)
    mercury = cb("Mercury", 3.285e23, np.array([4348.792498208769E+07,2058.483406643132E+07,-2291.706994364512E+06]), np.array([-3063.033163261347E+01,4602.719001738175E+01,6572.234092009960E+00]),np.array([0,0,0]), None)
    venus = cb("Venus", 4.867e24, np.array([-8106.652093903564E+07,7050.194242102133E+07,5636.055420686472E+06]), np.array([-2336.771886321154E+01,-2637.525908067103E+01,9866.649505096099E-01]),np.array([0,0,0]), None)
    uranus =  cb("Uranus", 8.681e25, np.array([1633.738109797280E+09,2423.385637297977E+09,-1216.497248135650E+07]), np.array([-5696.890576773002E+00,3489.307038044661E+00,8654.868535910132E-02]),np.array([0,0,0]), None)
    
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
            "  Welcome! Close this window to begin simulation with chosen values. If you don't  \n  change any values the default values are used which are from NASA Horizons API  \n  recorded on February 24th 2025  \n\n Enter numbers only or simulation will not be drawn  ",
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
        try:
            finalgravvalue = (np.multiply(int(self._grav.value), 6.6743e-11))
            endpoint = int(self._frames.value)
            finalsimulation = simulation(self.cbs, self._viewwindow.value, finalgravvalue,endpoint)
            finalsimulation.runsimulation()
        except:
            pass
        
 



#Execute the application
pyforms.start_app( SolarSim, geometry = (210,210,210,210 ) )


