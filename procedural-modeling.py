import maya.cmds as cmds
import random
import math

#UI
if 'UI' in globals():
    if cmds.window(UI, exists=True):
        cmds.deleteUI(UI, window=True)

# GLOBAL VARIABLES
houseWidth = 5
houseDepth = 5
houseHeight = 4
frontyard = 2
backyard = 3
roadWidth = 3

UI = cmds.window(title='Build a Neighbourhood', width=450)

cmds.columnLayout(rowSpacing=15)
cmds.separator(style="none", height=5)
cmds.text(label='Choose what you would like to have in your neighbourhood:')
cmds.text(label='(Clear the scene before generating.)')

cmds.intSliderGrp('StreetNum', label='Number of streets:', f=True, min=1, max=10, value=1)
cmds.intSliderGrp('HouseDis', label='Distance between houses:', f=True, min=2, max=5, value=2)
cmds.intSliderGrp('HouseNum', label='Number of houses:', f=True, min=1, max=24, value=1)
# cmds.checkBox('Fencing', label='Include Fencing')
cmds.checkBox('StreetLights', label='Include Streetlights', value=True)
cmds.checkBox('Greenery', label='Include Greenery', value=True)

cmds.button(label='Generate Neighbourhood', command=('generateNeighbourhood()'))

# cmds.separator(style="none", height=5)
# cmds.button(label="Clear Namespace", command=('clearNamespace()'))
# cmds.separator(style="none", height=5)

cmds.button(label="Clear Scene", command=('clearScene()'))

cmds.showWindow(UI)

def clearNamespace():
    cmds.namespace(set=":")  # used to move out of namespace (for debugging)

def clearScene():
    cmds.select(all=True)
    cmds.delete()

# create neighbourhood
def generateNeighbourhood():

    numStreets = cmds.intSliderGrp('StreetNum', q=True, v=True)
    numHouses = cmds.intSliderGrp('HouseNum', q=True, v=True)
    houseDistance = cmds.intSliderGrp('HouseDis', q=True, v=True)

    housePlotX = frontyard + houseWidth + backyard
    housePlotZ = houseDistance * 2 + houseDepth

    # streetLength = math.ceil(numHouses/2) * houseWidth + (math.ceil(numHouses/2) + 1) * houseDistance
    streetLength = housePlotZ * math.ceil(numHouses/2)
    streetWidth = housePlotX * 2 + roadWidth

    # print(housePlotX)
    # print(housePlotZ)
    print("streetLength: " + str(streetLength))

    # generating materials
    generateMaterials()

    nbrhoodWidth = streetWidth * numStreets
    # create ground
    ground = cmds.polyCube(n='ground', width=nbrhoodWidth, height=0.1, depth=streetLength)
    cmds.move(-(0.1 / 2.0), moveY=True)

    cmds.select('ground')
    cmds.hyperShade(assign=(":groundMat"))

    streets = []

    # GENERATING STREETS
    for i in range(numStreets):
        streetDisplacement = (-nbrhoodWidth/2.0) + (0.5 * streetWidth) + (streetWidth * i)

        generateStreet(streetLength, i)
        cmds.select('Street' + str(i) + 'grp')
        cmds.move(streetDisplacement, moveX=True)

    #check if fencing is selected
    # if (cmds.checkBox('Fencing', query=True, value=True) == True):
    #
    #     side1 = generateFence()
    #
    #     for i in range(width-1):
    #         cmds.move(-(width/2.0)-0.5+ (i+1), 0.25, height/2.0)
    #         cmds.duplicate(st=True)
    #
    #     side2 = generateFence()
    #
    #     for i in range(width-1):
    #         cmds.move(-(width/2.0)-0.5+ (i+1), 0.25, -height/2.0)
    #         cmds.duplicate(st=True)
    #
    #     side3 = generateFence()
    #
    #     for i in range(height-1):
    #         cmds.move(width/2.0, 0.25, -(height/2.0)-0.5+ (i+1))
    #         cmds.rotate(0, 90, 0)
    #         cmds.duplicate(st=True)
    #
    #     side4 = generateFence()
    #
    #     for i in range(height-1):
    #         cmds.move(-width/2.0, 0.25, -(height/2.0)-0.5+ (i+1))
    #         cmds.rotate(0, 90, 0)
    #         cmds.duplicate(st=True)
    #
    #     cmds.select(all=True)
    #     cmds.group(n='fence')

    #check if trees are selected
    # if (cmds.checkBox('Greenery', query=True, value=True) == True):
    #     trees = generateTrees(width, height)d

# generate materials to be used
def generateMaterials():
    # CREATING GROUND MATERIAL
    # create ground material if it doesn't already exist
    if not (cmds.objExists('groundMat') and cmds.objectType('groundMat') == 'lambert'):
        groundShader = cmds.shadingNode('lambert', asShader=True, name="groundMat")
    cmds.setAttr(":groundMat.color", 0.48, 0.86, 0.43)

    # ROAD MATERIAL
    if not (cmds.objExists('roadMat') and cmds.objectType('roadMat') == 'lambert'):
        roadShader = cmds.shadingNode('lambert', asShader=True, name="roadMat")
    cmds.setAttr(":roadMat.color", 0.7, 0.595, 0.595)

    # ROAD BORDER MATERIAL
    if not (cmds.objExists('borderMat') and cmds.objectType('borderMat') == 'lambert'):
        roadShader = cmds.shadingNode('lambert', asShader=True, name="borderMat")
    cmds.setAttr(":borderMat.color", 0.95, 0.912, 0.907)

    # HOUSE COLOURS
    if not (cmds.objExists('houseBlueMat') and cmds.objectType('houseBlueMat') == 'lambert'):
        roadShader = cmds.shadingNode('lambert', asShader=True, name="houseBlueMat")
    cmds.setAttr(":houseBlueMat.color", 0.47, 0.843, 0.98)

    if not (cmds.objExists('houseOrangeMat') and cmds.objectType('houseOrangeMat') == 'lambert'):
        roadShader = cmds.shadingNode('lambert', asShader=True, name="houseOrangeMat")
    cmds.setAttr(":houseOrangeMat.color", 1, 0.627, 0.439)

    if not (cmds.objExists('houseYellowMat') and cmds.objectType('houseYellowMat') == 'lambert'):
        roadShader = cmds.shadingNode('lambert', asShader=True, name="houseYellowMat")
    cmds.setAttr(":houseYellowMat.color", 1.0, 0.99, 0.385)

    if not (cmds.objExists('houseGreenMat') and cmds.objectType('houseGreenMat') == 'lambert'):
        roadShader = cmds.shadingNode('lambert', asShader=True, name="houseGreenMat")
    cmds.setAttr(":houseGreenMat.color", 0.647, 0.96, 0.478)

    # HOUSE MATERIALS
    if not (cmds.objExists('roofMat') and cmds.objectType('roofMat') == 'lambert'):
        roadShader = cmds.shadingNode('lambert', asShader=True, name="roofMat")
    cmds.setAttr(":roofMat.color", 0.388, 0.259, 0.192)

    if not (cmds.objExists('doorBlueMat') and cmds.objectType('doorBlueMat') == 'lambert'):
        roadShader = cmds.shadingNode('lambert', asShader=True, name="doorBlueMat")
    cmds.setAttr(":doorBlueMat.color", 0.181, 0.409, 0.576)

    if not (cmds.objExists('doorGreenMat') and cmds.objectType('doorGreenMat') == 'lambert'):
        roadShader = cmds.shadingNode('lambert', asShader=True, name="doorGreenMat")
    cmds.setAttr(":doorGreenMat.color", 0.218, 0.432, 0.169)

    if not (cmds.objExists('doorOrangeMat') and cmds.objectType('doorOrangeMat') == 'lambert'):
        roadShader = cmds.shadingNode('lambert', asShader=True, name="doorOrangeMat")
    cmds.setAttr(":doorOrangeMat.color", 0.8, 0.296, 0.161)

    if not (cmds.objExists('doorYellowMat') and cmds.objectType('doorYellowMat') == 'lambert'):
        roadShader = cmds.shadingNode('lambert', asShader=True, name="doorYellowMat")
    cmds.setAttr(":doorYellowMat.color", 0.978, 0.756, 0.14)

    if not (cmds.objExists('doorMat') and cmds.objectType('doorMat') == 'lambert'):
        roadShader = cmds.shadingNode('lambert', asShader=True, name="doorMat")
    cmds.setAttr(":doorMat.color", 0.268, 0.308, 0.615)

    if not (cmds.objExists('glassMat') and cmds.objectType('glassMat') == 'lambert'):
        roadShader = cmds.shadingNode('lambert', asShader=True, name="glassMat")
    cmds.setAttr(":glassMat.color", 0.679, 0.988, 1.0)
    cmds.setAttr(':glassMat.transparency', 0.3, 0.3, 0.3)

    if not (cmds.objExists('greeneryMat') and cmds.objectType('greeneryMat') == 'lambert'):
        roadShader = cmds.shadingNode('lambert', asShader=True, name="greeneryMat")
    cmds.setAttr(":greeneryMat.color", 0.235, 0.5, 0.189)

# generate ground and road
def generateStreet(length, streetNum):

    # creating namespace to keep track of all objects in street
    nsStreet = "Street" + str(streetNum)
    cmds.select(clear=True)

    if cmds.namespace(exists=nsStreet):
        cmds.namespace(removeNamespace=nsStreet, mergeNamespaceWithRoot=True)

    cmds.namespace(add=nsStreet)
    cmds.namespace(set=nsStreet)

    # create road
    road = cmds.polyCube(n='road', width=roadWidth, height=0.08, depth=length)
    cmds.move((0.08 / 2.0), moveY=True)

    rightBorder = cmds.polyCube(n='rightBorder', width=0.4, height=0.1, depth=length)
    cmds.move((0.1 / 2.0), moveY=True)
    cmds.move(-1.5, moveX=True)

    leftBorder = cmds.polyCube(n='rightBorder', width=0.4, height=0.1, depth=length)
    cmds.move((0.1 / 2.0), moveY=True)
    cmds.move(1.5, moveX=True)

    # APPLYING MATERIAL TO ROAD
    cmds.select(road)
    cmds.hyperShade(assign=(":roadMat"))

    cmds.select(rightBorder, leftBorder)
    cmds.hyperShade(assign=(":borderMat"))

    generateHouses(streetNum)

    cmds.select(nsStreet + ":*")
    streetObjects = cmds.ls(selection=True)
    streetGroup = cmds.group(empty=True, n="Street" + str(streetNum)+'grp')
    cmds.parent(streetObjects, streetGroup)

    # moving objects outside of namespace?
    cmds.namespace(set=":")
    cmds.namespace(removeNamespace=":" + nsStreet, mergeNamespaceWithRoot=True)

# generate houses
def generateHouses(streetNum):
    nsStreet = "Street" + str(streetNum)
    numHouses = cmds.intSliderGrp('HouseNum', q=True, v=True)
    houseDistance = cmds.intSliderGrp('HouseDis', q=True, v=True)
    streetDistance = roadWidth/2.0 + frontyard + houseDepth/2.0

    genStreetLight = cmds.checkBox('StreetLights', q=True, v=True)
    genGreenery = cmds.checkBox('Greenery', q=True, v=True)

    houses = [] # array to store all house models
    streetlights = []
    trees = []
    bushes = []

    housePlotZ = houseDistance * 2 + houseDepth
    streetLength = housePlotZ * math.ceil(numHouses / 2)

    rowCount = 1
    streetLightPosition = 0
    streetLightCount = 0
    treeCount = 0
    bushCount = 0

    #controlling the random color so each color shows up at least once in each 4-digit sequence
    randomColorSequence = []
    for i in range(8):
        randNums = [1,2,3,4]
        random.shuffle(randNums)
        randomColorSequence = randomColorSequence + randNums
    # print(randomColorSequence)

    for i in range(numHouses):
        houses.append(modelHouse(streetNum, i, randomColorSequence[i]))
        streetDisplacement = (-streetLength/2.0) + houseDistance + (0.5 * houseWidth) + ((rowCount - 1) * 2) * (houseDistance + (0.5 * houseWidth))

        if i % 2 == 0: # if house's position in array is even,
            # print(houses[i])
            cmds.select(houses[i])
            cmds.rotate(90, y=True)
            cmds.move(-streetDistance, moveX=True)
            cmds.move(streetDisplacement, moveZ=True)

            if i == streetLightPosition and genStreetLight: # even numbered streetlight
                streetlights.append(modelStreetlight())
                cmds.select(streetlights[streetLightCount])
                cmds.move(-(houseWidth/2.0 + houseDistance/2.0), moveZ=True)
                cmds.move(-(roadWidth/2.0 + frontyard/2.0), moveX=True)
                cmds.move(streetDisplacement, moveZ=True, relative=True)
                print(streetDisplacement)
                streetLightCount += 1
                streetLightPosition += 3

            if genGreenery:
                randGreenery = random.randint(1, 3)
                # if 1, generate tree
                if randGreenery == 1:
                    trees.append(modelTree())
                    cmds.select(trees[treeCount])
                    cmds.move((houseWidth / 2.0 + houseDistance / 2.0), moveZ=True)
                    cmds.move(-(roadWidth / 2.0 + frontyard / 1.5), moveX=True)
                    cmds.move(streetDisplacement, moveZ=True, relative=True)
                    treeCount += 1
                # if 2, generate bush
                elif randGreenery == 2:
                    bushes.append(modelBush())
                    cmds.select(bushes[bushCount][0])
                    cmds.move((houseWidth / 2.0 + houseDistance / 2.0), moveZ=True)
                    cmds.move(-(roadWidth / 2.0 + frontyard / 1.3), moveX=True)
                    cmds.move(streetDisplacement, moveZ=True, relative=True)
                    bushCount += 1
                # if 3, generate no greenerys
        else:
            cmds.select(houses[i])
            cmds.rotate(-90, y=True)
            cmds.move(streetDistance, moveX=True)
            cmds.move(streetDisplacement, moveZ=True)
            rowCount += 1

            if i == streetLightPosition and genStreetLight: # odd numbered streetlight
                streetlights.append(modelStreetlight())
                cmds.select(streetlights[streetLightCount])
                cmds.move(-(houseWidth/2.0 + houseDistance/2.0), moveZ=True)
                cmds.move((roadWidth/2.0 + frontyard/2.0), moveX=True)
                cmds.move(streetDisplacement, moveZ=True, relative=True)
                print(streetDisplacement)
                streetLightCount += 1
                streetLightPosition += 1

            if genGreenery:
                randGreenery = random.randint(1, 3)
                # if 1, generate tree
                if randGreenery == 1:
                    trees.append(modelTree())
                    cmds.select(trees[treeCount])
                    cmds.move((houseWidth / 2.0 + houseDistance / 2.0), moveZ=True)
                    cmds.move((roadWidth / 2.0 + frontyard / 1.5), moveX=True)
                    cmds.move(streetDisplacement, moveZ=True, relative=True)
                    treeCount += 1
                # if 2, generate bush
                elif randGreenery == 2:
                    bushes.append(modelBush())
                    cmds.select(bushes[bushCount][0])
                    cmds.move((houseWidth / 2.0 + houseDistance / 2.0), moveZ=True)
                    cmds.move((roadWidth / 2.0 + frontyard / 1.3), moveX=True)
                    cmds.move(streetDisplacement, moveZ=True, relative=True)
                    bushCount += 1
                # if 3, generate no greenerys

# poly model houses
def modelHouse(streetNum, houseNum, randomCol):
    houseBase = cmds.polyCube(h=houseHeight, w=houseWidth, d=houseDepth, sz=2, sx=2, n='houseBase')
    cmds.move((houseHeight / 2.0), moveY=True)

    # GENERATING HOUSE BASE
    houseTop = cmds.polyPrism(l=houseDepth, w=houseWidth,sh=2, sc=1, n='houseTop')
    # cmds.polyPrism(l=houseDepth, w=houseWidth, n='houseTop')
    cmds.rotate(90, 0, -30)
    cmds.move(5.443, moveY=True)

    cmds.select(houseTop[0] + '.e[9]', houseTop[0] + '.e[12]')
    cmds.polyMoveEdge(ty=-2.83)
    cmds.select(houseTop[0] + '.vtx[9:10]')
    cmds.polyMoveVertex(ty=-0.8)

    # cmds.select(houseBase, houseTop)
    houseBase = cmds.polyUnite(houseBase, houseTop, n='house')
    # cmds.delete(ch=True)  # deletes construction history
    cmds.polyMergeVertex(houseBase, d=0.01)
    cmds.delete(ch=True)  # deletes construction history

    # GENERATING HOUSE ROOF
    houseRoof = cmds.polyCube(h=0.3, width=houseWidth+1, depth=houseDepth+1, sx=2, n='roof')
    cmds.move(3.9, moveY=True)

    cmds.select(houseRoof[0] + '.e[9]', houseRoof[0] + '.e[12]', houseRoof[0] + '.e[15]', houseRoof[0] + '.e[18]')
    cmds.polyMoveEdge(ty=1.6)
    cmds.polySoftEdge(a=0)
    cmds.delete(ch=True)  # deletes construction history

    cmds.select(houseRoof)
    cmds.hyperShade(assign=(":roofMat"))

    # GENERATING CHIMNEY
    randChimney = random.randint(1, 10)

    if randChimney > 4:
        randChimneyX = random.choice([-1.3, 1.3])
        chimneyBase = cmds.polyCube(width=0.9, height=2, depth=0.9, n='chimneyBase')
        cmds.move(randChimneyX, 5, -1.3)
        chimneyInner = cmds.polyCube(width=0.65, height=3, depth=0.65, n='chimneyBase')
        cmds.move(randChimneyX, 5, -1.3)

        chimney = cmds.polyCBoolOp(chimneyBase, chimneyInner, op=2, n="chimney")
        cmds.delete(ch=True)

        cmds.select(chimney[0])
        if randomCol == 1:  # blue
            cmds.hyperShade(assign=(":houseBlueMat"))
        elif randomCol == 2:  # green
            cmds.hyperShade(assign=(":houseGreenMat"))
        elif randomCol == 3:  # orange
            cmds.hyperShade(assign=(":houseOrangeMat"))
        elif randomCol == 4:  # yellow
            cmds.hyperShade(assign=(":houseYellowMat"))

        houseRoof = cmds.group(houseRoof[0], chimney[0], n='houseRoof')
    else:
        houseRoof = cmds.group(houseRoof[0], n='houseRoof')

    # GENERATING FRONT DOOR
    randDoorX = random.choice([-0.9, 0, 0.9])

    doorBase = cmds.polyCube(width=1.5, height=2.2, depth=0.2, n='door')
    cmds.move(randDoorX, 1.1, 2.55)
    doorInner = cmds.polyCube(width=1.2, height=2.1, depth=0.5, n='doorInner')
    cmds.move(randDoorX, 1, 2.55)

    doorFrame = cmds.polyCBoolOp(doorBase, doorInner, op=2, n="doorFrame")
    cmds.delete(ch=True)

    door = cmds.polyCube(width=1.3, height=2.1, depth=0.1, n='doorInner')
    cmds.move(randDoorX, 1.05, 2.55)
    cmds.hyperShade(assign=(":doorMat"))

    # GENERATING WINDOWS
    window1 = random.randint(1, 2)
    window2 = random.randint(1, 2)
    window3 = random.randint(1, 2)
    window4 = random.randint(1, 2)

    windowFrames = cmds.group(empty=True, n="windowFrames")
    windows = cmds.group(empty=True, n="windows")
    if window1 == 1:
        winZ = 1
        windowBase1 = cmds.polyCube(width=0.2, height=1.5, depth=1.5, n='windowBase')
        cmds.move(2.5, 1.6, winZ)
        windowInner1= cmds.polyCube(width=0.5, height=1.3, depth=1.3, n='windowBase')
        cmds.move(2.5, 1.6, winZ)

        windowFrame1 = cmds.polyCBoolOp(windowBase1, windowInner1, op=2, n="windowFrame")
        cmds.delete(ch=True)

        window1 = cmds.polyCube(width=0.1, height=1.4, depth=1.4, n='window1')
        cmds.move(2.5, 1.6, winZ)
        cmds.hyperShade(assign=(":glassMat"))

        cmds.parent(windowFrame1[0], windowFrames)
        cmds.parent(window1[0], windows)

    if window2 == 1:
        winZ = -1
        windowBase2 = cmds.polyCube(width=0.2, height=1.5, depth=1.5, n='windowBase')
        cmds.move(2.5, 1.6, winZ)
        windowInner2= cmds.polyCube(width=0.5, height=1.3, depth=1.3, n='windowBase')
        cmds.move(2.5, 1.6, winZ)

        windowFrame2 = cmds.polyCBoolOp(windowBase2, windowInner2, op=2, n="windowFrame")
        cmds.delete(ch=True)

        window2 = cmds.polyCube(width=0.1, height=1.4, depth=1.4, n='window2')
        cmds.move(2.5, 1.6, winZ)
        cmds.hyperShade(assign=(":glassMat"))

        cmds.parent(windowFrame2[0], windowFrames)
        cmds.parent(window2[0], windows)

    if window3 == 1:
        winZ = 1
        windowBase3 = cmds.polyCube(width=0.2, height=1.5, depth=1.5, n='windowBase')
        cmds.move(-2.5, 1.6, winZ)
        windowInner3= cmds.polyCube(width=0.5, height=1.3, depth=1.3, n='windowBase')
        cmds.move(-2.5, 1.6, winZ)

        windowFrame3 = cmds.polyCBoolOp(windowBase3, windowInner3, op=2, n="windowFrame")
        cmds.delete(ch=True)

        window3 = cmds.polyCube(width=0.1, height=1.4, depth=1.4, n='window3')
        cmds.move(-2.5, 1.6, winZ)
        cmds.hyperShade(assign=(":glassMat"))

        cmds.parent(windowFrame3[0], windowFrames)
        cmds.parent(window3[0], windows)

    if window2 == 1:
        win4 = -1
        windowBase4 = cmds.polyCube(width=0.2, height=1.5, depth=1.5, n='windowBase')
        cmds.move(-2.5, 1.6, winZ)
        windowInner4= cmds.polyCube(width=0.5, height=1.3, depth=1.3, n='windowBase')
        cmds.move(-2.5, 1.6, winZ)

        windowFrame4 = cmds.polyCBoolOp(windowBase4, windowInner4, op=2, n="windowFrame")
        cmds.delete(ch=True)

        window4 = cmds.polyCube(width=0.1, height=1.4, depth=1.4, n='window4')
        cmds.move(-2.5, 1.6, winZ)
        cmds.hyperShade(assign=(":glassMat"))

        cmds.parent(windowFrame4[0], windowFrames)
        cmds.parent(window4[0], windows)

    # ASSIGNING RANDOM HOUSE MATERIAL
    cmds.select(houseBase[0])
    if randomCol == 1: # blue
        cmds.hyperShade(assign=(":houseBlueMat"))
        cmds.select(doorFrame[0], windowFrames)
        cmds.hyperShade(assign=(":doorBlueMat"))
    elif randomCol ==2: # green
        cmds.hyperShade(assign=(":houseGreenMat"))
        cmds.select(doorFrame[0], windowFrames)
        cmds.hyperShade(assign=(":doorGreenMat"))
    elif randomCol == 3: # orange
        cmds.hyperShade(assign=(":houseOrangeMat"))
        cmds.select(doorFrame[0], windowFrames)
        cmds.hyperShade(assign=(":doorOrangeMat"))
    elif randomCol == 4:  # yellow
        cmds.hyperShade(assign=(":houseYellowMat"))
        cmds.select(doorFrame[0], windowFrames)
        cmds.hyperShade(assign=(":doorYellowMat"))

    # GENERATING BACK DOOR
    backDoorFrame = cmds.duplicate(doorFrame[0], n='backdoorFrame')
    cmds.move(-randDoorX, 0, -2.55)
    # freeze transformations
    cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False)
    randDoorX2 = random.choice([-0.9, 0, 0.9])
    cmds.move(randDoorX2, 0, -2.55)

    cmds.select(clear=True)

    backDoorInner = cmds.duplicate(door[0], n='backdoorInner')
    cmds.select(backDoorInner[0])
    cmds.move(randDoorX2, 1.05, -2.55)

    backDoor = cmds.group(backDoorFrame[0], backDoorInner[0], n='backdoor')

    house = cmds.group(houseBase[0],houseRoof, windowFrames, windows, doorFrame[0], door[0], backDoor, n='house')

    return house

# poly model streetlights
def modelStreetlight():
    poleBase = cmds.polyCylinder(sa=20, sz=1, r=0.25, h=0.1, n='poleBase')
    cmds.move(0.05, moveY=True)

    poleCircleBase = cmds.polyCylinder(sa=20, sz=1, r=0.15, h=0.4, n='poleCircleBase')
    cmds.move(0.2, moveY=True)

    pole = cmds.polyCylinder(sa=20, sz=1, r=0.075, h=4, n='poleBase')
    cmds.move(2.0, moveY=True)

    lightCircleBase = cmds.polyCylinder(sa=20, sz=1, r=0.11, h=0.2, n='lightCircleBase')
    cmds.move(4.0, moveY=True)

    lightBase = cmds.polyCube(width=0.42, height=0.15, depth=0.42, sz=1, sx=1, n='lightBase')
    cmds.move(4.1, moveY=True)

    light = cmds.polyCube(width=0.5, height=0.65, depth=0.5, n='light')
    cmds.move(4.45, moveY=True)
    cmds.select(light[0] + '.f[3]')
    cmds.scale(0.7, 1, 0.7)

    lightTop = cmds.polyCube(width=0.55, height=0.25, depth=0.55, sz=1, sx=1, n='lightTop')
    cmds.move(4.8, moveY=True)

    lightCircleTop = cmds.polyCylinder(sa=20, sz=1, r=0.11, h=0.15, n='lightCircleTop')
    cmds.move(4.95, moveY=True)

    cmds.select(poleBase, poleCircleBase, pole, lightCircleBase, lightBase, lightTop, lightCircleTop)
    cmds.hyperShade(assign=(":roofMat"))

    cmds.select(light)
    cmds.hyperShade(assign=(":glassMat"))

    # ADDING BEVELS
    cmds.select(lightTop[0] + '.e[1]', lightTop[0] + '.e[2]', lightTop[0] + '.e[6]', lightTop[0] + '.e[7]')
    cmds.polyBevel(fraction=1.2, offset=1.0, oaf=True, sa=30)
    cmds.delete(ch=True)

    cmds.select(lightBase[0] + '.e[0]', lightBase[0] + '.e[3]', lightBase[0] + '.e[10]', lightBase[0] + '.e[11]')
    cmds.polyBevel(fraction=1.0, offset=1.0, oaf=True, at=180, sa=30)
    cmds.delete(ch=True)

    cmds.select(poleBase[0] + ".e[20:39]")
    cmds.polyBevel(o=0.3, oaf=True, at=180, sa=30)
    cmds.delete(ch=True)

    cmds.select(lightCircleTop[0] + ".e[20:39]")
    cmds.polyBevel(o=0.3, oaf=True, at=180, sa=30)
    cmds.delete(ch=True)

    cmds.select(poleCircleBase[0] + ".e[20:39]")
    cmds.polyBevel(fraction=0.4, offset=1.0, oaf=True, sa=30)
    cmds.delete(ch=True)

    cmds.select(lightCircleBase[0] + ".e[0:19]")
    cmds.polyBevel(fraction=0.4, offset=1.0, oaf=True, sa=30)
    cmds.delete(ch=True)

    streetLight = cmds.group(poleBase[0], poleCircleBase[0], pole[0], lightCircleBase[0], lightBase[0], light[0], lightTop[0], lightCircleTop[0], n='streetLight')

    return streetLight

# poly model trees
def modelTree():

    leaves = cmds.polySphere(r=0.9)
    cmds.move(2.8, moveY=True)
    cmds.hyperShade(assign=(":greeneryMat"))

    trunk = cmds.polyCylinder(sa=8, sz=1, sy=3, r=0.15, h=3, n='trunk')
    cmds.move(1.5, moveY=True)
    cmds.hyperShade(assign=(":roofMat"))

    cmds.select(trunk[0] + '.e[0:7]')
    cmds.scale(1.2, 1, 1.2)

    cmds.select(trunk[0] + '.e[8:15]')
    cmds.move(-0.04, moveZ=True, relative=True)

    cmds.select(trunk[0] + '.e[16:23]')
    cmds.scale(0.85, 1, 0.85)

    cmds.select(leaves[0])
    cmds.polyRetopo(targetFaceCount=1000, n='leaves')
    cmds.polyTriangulate()
    cmds.polySoftEdge(a=0)
    cmds.delete(ch=True)
    cmds.polyReduce(p=93)
    cmds.delete(ch=True)

    tree = cmds.group(leaves[0], trunk[0], n='tree')
    return tree

def modelBush():

    bush1 = cmds.polySphere(r=0.8)
    cmds.move(0.5, moveY=True)
    bush2 = cmds.polySphere(r=0.6)
    cmds.move(0.3, 0.3, -0.7)

    bush = cmds.polyUnite(bush1, bush2, n='bush')
    cmds.delete(ch=True)  # deletes construction history

    cmds.select(bush[0])
    cmds.polyRetopo(targetFaceCount=1000, n='bush')
    cmds.polyTriangulate()
    cmds.polySoftEdge(a=0)
    cmds.delete(ch=True)
    cmds.polyReduce(p=85)

    cmds.hyperShade(assign=(":greeneryMat"))

    return bush

# # create fence (poly model later)
# def generateFence():
#     singleFence = cmds.polyCube(n='fence', width=0.072, height=1, depth=2.264)
#     return singleFence
