import maya.cmds as cmds;
import math;


# ball and stick models for cubic crystal lattices

# helper functions for simple cubic base of other lattices
# generates spheres at sc lattice points in for loops
def scBalls(x, y, z, radiusBall, latticeConst):
        xCoord = x*latticeConst
        yCoord = y*latticeConst
        zCoord = z*latticeConst
        nameSuffix = str(x) + str(y) + str(z)
        
        nameBall = 'ball' + nameSuffix
        cmds.polySphere(sx=10, sy=10, r=radiusBall, n=nameBall)
        cmds.setAttr(str(nameBall)+'.translate', xCoord, yCoord, zCoord)
        
# generates connectors between sc lattice points in for loops
def scSticks(x, y, z, dimX, dimY, dimZ, radiusStick, latticeConst):
    xCoord = x*latticeConst
    yCoord = y*latticeConst
    zCoord = z*latticeConst
    nameSuffix = str(x) + str(y) + str(z)
    
    if x != dimX:  
        nameStickX = 'stickX' + nameSuffix
        cmds.polyCylinder(r=radiusStick, h=latticeConst, sx=5, n=nameStickX, axis=(1, 0, 0))
        cmds.setAttr(str(nameStickX)+'.translate', xCoord + 0.5*latticeConst, yCoord, zCoord)
    
    if y != dimY:
        nameStickY = 'stickY' + nameSuffix
        cmds.polyCylinder(r=radiusStick, h=latticeConst, sx=5, n=nameStickY, axis=(0, 1, 0))
        cmds.setAttr(str(nameStickY)+'.translate', xCoord, yCoord + 0.5*latticeConst, zCoord)

    if z!= dimZ:
        nameStickZ = 'stickZ' + nameSuffix
        cmds.polyCylinder(r=radiusStick, h=latticeConst, sx=5, n=nameStickZ, axis=(0, 0, 1))
        cmds.setAttr(str(nameStickZ)+'.translate', xCoord, yCoord, zCoord + 0.5*latticeConst)



# simple cubic lattice
# dimX, dimY, dimZ are the number of unit cells in the given direction, latticeConst sets the lattice constant
# bool stick determines, if the model is constructed with sticks connecting the lattice points.
def scLattice( dimX = 1, dimY = 1, dimZ = 1, radiusBall = 0.1, radiusStick = 0.02, latticeConst = 1.0, sticks = True ):
    
    for x in xrange (0, dimX + 1):
        for y in xrange (0, dimY + 1):
            for z in xrange (0, dimZ + 1):
                scBalls(x, y, z, radiusBall, latticeConst)
                if sticks == True:
                    scSticks(x, y, z, dimX, dimY, dimZ, radiusStick, latticeConst)
                                        

# body centered cubic lattice
def bccLattice( dimX = 1, dimY = 1, dimZ = 1, radiusBall = 0.1, radiusStick = 0.02, latticeConst = 1.0, sticks = True):
    
    for x in xrange (0, dimX + 1):
        for y in xrange (0, dimY + 1):
            for z in xrange (0, dimZ + 1):
                xCoord = x * latticeConst
                yCoord = y * latticeConst
                zCoord = z * latticeConst
                nameSuffix = str(x) + str(y) + str(z)
                
                #scPart of bccLattice
                scBalls(x, y, z, radiusBall, latticeConst)
                if sticks == True:
                    scSticks(x, y, z, dimX, dimY, dimZ, radiusStick, latticeConst)
                
                # ball in body
         
                if x != dimX and y != dimY and z != dimZ:
                    xCoordBody = xCoord+0.5*latticeConst
                    yCoordBody = yCoord+0.5*latticeConst
                    zCoordBody = zCoord+0.5*latticeConst
                    
                    nameBallBody = 'ballBody' + nameSuffix
                    cmds.polySphere(sx=10, sy=10, r=radiusBall, n=nameBallBody)
                    cmds.setAttr(str(nameBallBody)+'.translate', xCoordBody, yCoordBody, zCoordBody)
                    
                    
                    #sticks in body
                    if sticks == True:
                        heightBC = latticeConst * math.sqrt(3)
                    
                        axes = [(1, 1, 1), (1, 1, -1), (1, -1, -1), (-1, 1, -1)]
                    
                        for i in xrange(0, 4):
                            nameStickBody = 'stickBody' + nameSuffix + '_' + str(i)
                        
                            cmds.polyCylinder(r=radiusStick, h=heightBC, sx=5, n=nameStickBody, axis=axes[i])
                            cmds.setAttr(str(nameStickBody)+'.translate', xCoordBody, yCoordBody, zCoordBody)
                    

                                
# face centered cubic lattice
                
def fccLattice( dimX=1, dimY=1, dimZ=1, radiusBall = 0.1, radiusStick = 0.02, latticeConst = 1.0, sticks = True ):
    
    for x in xrange (0, dimX + 1):
        for y in xrange (0, dimY + 1):
            for z in xrange (0, dimZ + 1):
                xCoord = x * latticeConst
                yCoord = y * latticeConst
                zCoord = z * latticeConst
                nameSuffix = str(x) + str(y) + str(z)
                
                scBalls(x, y, z, radiusBall, latticeConst)
                if sticks == True:
                    scSticks(x, y, z, dimX, dimY, dimZ, radiusStick, latticeConst)
                
                heightFCC = math.sqrt(2) * latticeConst
                xCoordFace = (0.5+x)*latticeConst
                yCoordFace = (0.5+y)*latticeConst
                zCoordFace = (0.5+z)*latticeConst
                
                faceTranslations = [(xCoordFace, yCoordFace, zCoord), (xCoord, yCoordFace, zCoordFace), (xCoordFace, yCoord, zCoordFace)]
                suffixDimChar = ['x', 'y', 'z']
                axes = [(1, 1, 0), (0, 1, 1), (1, 0, 1)]
                axesNeg = [(1, -1, 0), (0, -1, 1), (-1, 0, 1)]

                
                for i in xrange(0, 3):
                    if suffixDimChar[i] == 'x' and x != dimX and y!= dimY or suffixDimChar[i] == 'y' and z != dimZ and y != dimY or suffixDimChar[i] == 'z' and x != dimX and z!=dimZ:
                        #facecentered balls
                        nameFaceBall = 'faceBall' + suffixDimChar[i] + nameSuffix
                        cmds.polySphere(sx=10, sy=10, r=radiusBall, n=nameFaceBall)
                        cmds.setAttr(str(nameFaceBall)+'.translate', faceTranslations[i][0], faceTranslations[i][1], faceTranslations[i][2])
                        
                        #sticks to face centered balls
                        if sticks == True:
                            nameFaceStick1 = 'faceStick1_' + suffixDimChar[i] + nameSuffix
                            cmds.polyCylinder(r=radiusStick, h=heightFCC, sx=5, n=nameFaceStick1, axis=axes[i])
                            cmds.setAttr(str(nameFaceStick1)+'.translate', faceTranslations[i][0], faceTranslations[i][1], faceTranslations[i][2])

                            nameFaceStick2 = 'faceStick2_' + suffixDimChar[i] + nameSuffix
                            cmds.polyCylinder(r=radiusStick, h=heightFCC, sx=5, n=nameFaceStick2, axis=axesNeg[i])
                            cmds.setAttr(str(nameFaceStick2)+'.translate', faceTranslations[i][0], faceTranslations[i][1], faceTranslations[i][2])
                    

    
# diamond lattice
                
def diamondLattice(dimX=1, dimY=1, dimZ=1, radiusBall = 0.1, radiusStick = 0.02, latticeConst = 1.0, sticks = True):
  
    for x in xrange (0, dimX + 1):
        for y in xrange (0, dimY + 1):
            for z in xrange (0, dimZ + 1):

                scBalls(x, y, z, radiusBall, latticeConst)
                
                #coordinates for translation of spheres to lattice points
                xCoord = x * latticeConst
                yCoord = y * latticeConst
                zCoord = z * latticeConst
                
                xCoordFace = (x + 0.5) * latticeConst
                yCoordFace = (y + 0.5) * latticeConst
                zCoordFace = (z + 0.5) * latticeConst
                
                xCoordDia25 = (x + 0.25) * latticeConst
                yCoordDia25 = (y + 0.25) * latticeConst
                zCoordDia25 = (z + 0.25) * latticeConst
                
                xCoordDia75 = (x + 0.75) * latticeConst
                yCoordDia75 = (y + 0.75) * latticeConst
                zCoordDia75 = (z + 0.75) * latticeConst

                faceTranslations = [(xCoordFace, yCoordFace, zCoord), (xCoord, yCoordFace, zCoordFace), (xCoordFace, yCoord, zCoordFace)]
                
                nameSuffix = str(x) + str(y) + str(z)
                suffixDimChar = ['x', 'y', 'z']

                #fcc atoms
                for i in xrange(0, 3):
                    if suffixDimChar[i] == 'x' and x != dimX and y!= dimY or suffixDimChar[i] == 'y' and z != dimZ and y != dimY or suffixDimChar[i] == 'z' and x != dimX and z!=dimZ:
                        #facecentered balls
                        nameFaceBall = 'faceBall' + suffixDimChar[i] + nameSuffix
                        cmds.polySphere(sx=10, sy=10, r=radiusBall, n=nameFaceBall)
                        cmds.setAttr(str(nameFaceBall)+'.translate', faceTranslations[i][0], faceTranslations[i][1], faceTranslations[i][2])
                

                diamondTranslations = [(xCoordDia25, yCoordDia25, zCoordDia25), (xCoordDia75, yCoordDia75, zCoordDia25), (xCoordDia25, yCoordDia75, zCoordDia75), (xCoordDia75, yCoordDia25, zCoordDia75)]
                
                for i in xrange(0, 4):
                    if x != dimX and y != dimY and z != dimZ:
                        # 1/4 balls
                        nameDiaBall = 'diaBall' + str(i) + nameSuffix
                        cmds.polySphere(sx=10, sy=10, r=radiusBall, n=nameDiaBall)
                        cmds.setAttr(str(nameDiaBall)+'.translate', diamondTranslations[i][0], diamondTranslations[i][1], diamondTranslations[i][2])
                        
                        # bonds between lattice points
                        if sticks == True:
                            axes = [(-1, -1, -1), (1, 1, -1), (-1, 1, 1), (1, -1, 1)]
                            heightDia = math.sqrt(3) * 0.25 * latticeConst
                        
                            for j in xrange(0, 4):
                                #diamond sticks                
                                nameDiaStick = 'diaStick' + str(i) + str(j) + '_' + nameSuffix
                                cmds.polyCylinder(r=radiusStick, h=heightDia, sx=5, n=nameDiaStick, axis=axes[i])
                                cmds.setAttr(str(nameDiaStick)+'.translate', diamondTranslations[j][0] + 0.125*axes[i][0], diamondTranslations[j][1] + 0.125*axes[i][1], diamondTranslations[j][2] + 0.125*axes[i][2])
                                #print nameDiaStick + ' ' + str(axes[i])
                       
