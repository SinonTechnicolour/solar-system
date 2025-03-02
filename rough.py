

for key in cbs.keys():
    key.currentcombinedforce = np.array([0,0,0])
    key.printbodyattributes()
    for value in cbs[key]:
        key.currentcombinedforce = np.add(key.currentcombinedforce, cbs[key][value])
    key.printbodyattributes()
