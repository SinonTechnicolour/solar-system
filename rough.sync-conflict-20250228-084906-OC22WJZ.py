for key in listofcbs.keys():
    key.currentcombinedforce = np.array([0,0,0])
    for value in listofcbs[key]:
        key.currentcombinedforce = np.add(key.currentcombinedforce,listofcbs[key][value])
    key.printbodyattributes()

def updatepositionandvelocity(listofcbs):
    for key in listofcbs.keys():
    key.currentcombinedforce = np.array([0,0,0])
    for value in listofcbs[key]:
        key.currentcombinedforce = np.add(key.currentcombinedforce,listofcbs[key][value])
    key.printbodyattributes()
