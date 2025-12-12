import random
import copy


def getDirection(sensorData): #DONE
    #direction can either be left,up,right,down, or stay
    #direction is randomly generated unless a wall is detected, in which case the robot will just stay and no direction is updated

    # generating random direction
    random_int = random.randint(1,4)
    if random_int == 1:
        direction='left'
        if sensorData[0]==0: # checking if robot can move in the randomly generated direction
            direction='stay'
    elif random_int == 2:
        direction = 'up'
        if sensorData[1]==0: # checking if robot can move in the randomly generated direction
            direction='stay'
    elif random_int == 3:
        direction = 'right'
        if sensorData[2]==0: # checking if robot can move in the randomly generated direction
            direction='stay'
    elif random_int == 4:
        direction = 'down'
        if sensorData[3]==0: # checking if robot can move in the randomly generated direction
            direction='stay'

    return direction

def actualMovement(direction, actualIndex, probLeave): #DONE
    if direction == 'stay':
        return actualIndex
    
    i1 = actualIndex[0]
    i2 = actualIndex[1]

    random_float = random.random()

    if random_float <= probLeave: # only enters this if-statement if the robot is indeed moving
        #print("robot is moving", direction)
        if direction == 'left':
            i2-=1
        elif direction == 'up':
            i1-=1
        elif direction == 'right':
            i2+=1
        elif direction == 'down':
            i1+=1

    return [i1,i2] # represents new actualIndex

def gainSensorData(environment,actualIndex): #DONE
    i1 = actualIndex[0]
    i2 = actualIndex[1]
    sensorData = [2,2,2,2] # left, up, right, down
    if environment[i1][i2-1]=='_': #checking left
        sensorData[0]=1 # represents empty space
    else:
        sensorData[0]=0 # represents obstacle

    if environment[i1-1][i2]=='_': #checking up
        sensorData[1]=1 
    else:
        sensorData[1]=0 

    if environment[i1][i2+1]=='_': #checking right
        sensorData[2]=1 
    else:
        sensorData[2]=0 

    if environment[i1+1][i2]=='_': #checking down
        sensorData[3]=1 
    else:
        sensorData[3]=0 

    return(sensorData)

def updateMaps(mapCollection, direction, sensorData, probLeave):

    if direction == 'stay': # this means that in that iteration, robot doesn't actually move, and it's map collection stays the same
        return mapCollection
    
    probStay = 1-probLeave # 1/3

    leftSensor = sensorData[0]
    upSensor = sensorData[1]
    rightSensor = sensorData[2]
    downSensor = sensorData[3]
    
    # STEP 1: Fill in newMapCollection (including duplicates and invalid maps)

    newMapCollection = {}

    itemCount = 1
    
    # THIS IS WHERE YOU LEFT OFF, need to finish left

    if direction=='left': 
        for key, value in mapCollection.items():
            newMapCollection[itemCount,probStay*key[1]]=value 
            itemCount+=1
            valueLeave=copy.deepcopy(value)         
            for i in range(len(valueLeave)): # go through 1,2,3 [[' ', '_', ' '], ['0', '*', '_'], [' ', '0', ' ']]
                for j in range(len(valueLeave[i])): #go through ' ', '_', ' '
                    if valueLeave[i][j] == '*':
                        valueLeave[i][j] = '_'
                        valueLeave[i][j-1] = '*' 

                        if upSensor==0 and valueLeave[i-1][j-1] != '_':
                            valueLeave[i-1][j-1] = 0

                        elif upSensor==1 and valueLeave[i-1][j-1] != 0:
                            valueLeave[i-1][j-1] = '_'   

                        if downSensor == 0 and valueLeave[i+1][j-1]!='_':
                            valueLeave[i+1][j-1]=0
                        elif downSensor == 1 and valueLeave[i+1][j-1]!=0:
                            valueLeave[i+1][j-1]='_'

                        if leftSensor==0:
                            #print("j is", j)
                            if j>=2: # means that there is enough space to the left
                                #print("is it here? j>=2")
                                if valueLeave[i][j-2] != '_':
                                    
                                    valueLeave[i][j-2] = 0                            
                            #if valueLeave[i][j-1] != '_'
                            else: 
                                #print("is it here? j<2")
                                for k in range(len(valueLeave)):
                                    
                                    valueLeave[k].insert(0,' ')
  
                                valueLeave[i][j-1] = 0

                        elif leftSensor==1:

                            if j>=2: # means that there is enough space to the left
                                if valueLeave[i][j-2] != 0:
                                    valueLeave[i][j-2] = '_'
                            else: 
                                for k in range(len(valueLeave)):
                                    
                                    valueLeave[k].insert(0,' ')
                                    
                                valueLeave[i][j-1] = '_'
                     
                        break

            newMapCollection[itemCount,probLeave*key[1]] = valueLeave
            itemCount+=1
        #print(newMapCollection)

   
    elif direction=='up': #Done 
        for key, value in mapCollection.items():
            newMapCollection[itemCount,probStay*key[1]]=value 
            itemCount+=1
            valueLeave=copy.deepcopy(value)
            #print("value is", valueLeave) # [[' ', '_', ' '], ['0', '*', '_'], [' ', '0', ' ']]
            for i in range(len(valueLeave)): # go through 1,2,3 [[' ', '_', ' '], ['0', '*', '_'], [' ', '0', ' ']]
                for j in range(len(valueLeave[i])): #go through ' ', '_', ' '                
                    if valueLeave[i][j] == '*':
                        valueLeave[i][j] = '_'
                        valueLeave[i-1][j] = '*'
                        if leftSensor==0 and valueLeave[i-1][j-1]!='_':
                            valueLeave[i-1][j-1]=0
                        elif leftSensor==1 and valueLeave[i-1][j-1]!=0:
                            valueLeave[i-1][j-1]='_'

                        if rightSensor==0 and valueLeave[i-1][j+1]!='_':
                            valueLeave[i-1][j+1]=0
                        elif rightSensor==1 and valueLeave[i-1][j+1]!=0:
                            valueLeave[i-1][j+1]='_'
                           
                        if upSensor==0: # have to insert a whole other value[0] - valueLeave.insert(0,[]
                            if i <= 1: # means there isn't already a layer above and have to insert a new one
                                newLayer = [' ']*len(value[i])
                                newLayer[j]=0
                                valueLeave.insert(0,newLayer)
                            elif valueLeave[i-2][j]!='_': # means there is an existing upper layer
                                valueLeave[i-2][j]=0
                                             
                        elif upSensor==1:
                            if i <= 1: # means there isn't already a layer above and have to insert a new one
                                newLayer = [' ']*len(value[i])
                                newLayer[j]='_'
                                valueLeave.insert(0,newLayer)
                            elif valueLeave[i-2][j]!=0: # means there is an existing upper layer, also checking to make sure there isn't already an obstacle
                                valueLeave[i-2][j]='_'                       
                        break
                
                                
                            


            newMapCollection[itemCount,probLeave*key[1]] = valueLeave
            itemCount+=1

    elif direction=='right': #DONE 
        for key, value in mapCollection.items():
            newMapCollection[itemCount,probStay*key[1]]=value 
            itemCount+=1
            valueLeave=copy.deepcopy(value)
            #print("value is", valueLeave) # [[' ', '_', ' '], ['0', '*', '_'], [' ', '0', ' ']]
            for i in range(len(valueLeave)): # go through 1,2,3 [[' ', '_', ' '], ['0', '*', '_'], [' ', '0', ' ']]
                for j in range(len(valueLeave[i])): #go through ' ', '_', ' '
                    if valueLeave[i][j] == '*':
                        valueLeave[i][j] = '_'
                        valueLeave[i][j+1] = '*'
                    #need to account for sensor data of up, right, and down
                        '''
                        if upSensor==0: # this means we need to add an obstacle above *
                            if valueLeave[i-1][j+1]!=0:
                                valueLeave[i-1][j+1]=0    
                                valueLeave[i-1].append(' ') #this is simply ensuring all the value[i] are same length, need to check if this works properly
                        else: 
                            if valueLeave[i-1][j+1]!='_':
                                valueLeave[i-1][j+1]='_'
                                valueLeave[i-1].append(' ')  #this is simply ensuring all the value[i] are same length, need to check if this works properly
                        '''

                        if upSensor==0 and valueLeave[i-1][j+1]!='_': # this means we need to add an obstacle above *
                            valueLeave[i-1][j+1]=0  
                        elif upSensor == 1 and valueLeave[i-1][j+1]!=0: 
                            valueLeave[i-1][j+1]='_'
                            
                        '''
                        if downSensor==0: # this means we need to add an obstacle to the right of *
                            if valueLeave[i+1][j+1]!=0:    
                                valueLeave[i+1][j+1]=0
                                valueLeave[i+1].append(' ')
                        else:  
                            if valueLeave[i+1][j+1]!='_':   
                                valueLeave[i+1][j+1]='_'
                                valueLeave[i+1].append(' ') 
                        '''

                        if downSensor==0 and valueLeave[i+1][j+1]!='_': # this means we need to add an obstacle to the right of *   
                            valueLeave[i+1][j+1]=0
                        elif downSensor == 1 and valueLeave[i+1][j+1]!=0:
                            valueLeave[i+1][j+1]='_'


                        if rightSensor==0: # this means we need to add an obstacle to the right of *
                            #print("HELLO", j+1,len(valueLeave[i])-1)
                            #if len(valueLeave[i])!=len(valueLeave[i-1]): # we need to update all rows 
                            if j+1>=(len(valueLeave[i])-1):    
                                for k in range(len(valueLeave)):
                                    
                                    valueLeave[k].append(' ')
                                    
                                  
                                #valueLeave[i][len(valueLeave[i])-1] = 0
                                #print("testning", valueLeave[i][j+1])
                                valueLeave[i][j+2] = 0

                                '''
                                for k in range(len(valueLeave)):
                                    
                                    valueLeave[k].insert(0,' ')
                                    
                                valueLeave[i][j-1] = 0
                                '''
                                #valueLeave[i].append(0)
                            elif valueLeave[i][j+2] != '_':
                                valueLeave[i][j+2] = 0
                        elif rightSensor==1:  
                            #if len(valueLeave[i])!=len(valueLeave[i-1]): 
                            if j+1>=(len(valueLeave[i])-1): 
                                for k in range(len(valueLeave)):   
                                    valueLeave[k].append(' ')
                                    
                                #valueLeave[i][len(valueLeave[i])-1] = '_'
                                #valueLeave[i].append('_')
                                valueLeave[i][j+2] = '_'

                            elif valueLeave[i][j+2] != 0:
                                valueLeave[i][j+2] = '_'
                                               
                        break
            newMapCollection[itemCount,probLeave*key[1]] = valueLeave
            itemCount+=1

        #print(newMapCollection)

    elif direction=='down':
        dontContinue=1
        for key, value in mapCollection.items():
            lennn = copy.deepcopy(len(mapCollection[key]))
            break

        for key, value in mapCollection.items():
            newMapCollection[itemCount,probStay*key[1]]=value 
            itemCount+=1
            valueLeave=copy.deepcopy(value)
            length = copy.deepcopy(len(valueLeave))
            #print("value is", valueLeave) # [[' ', '_', ' '], ['0', '*', '_'], [' ', '0', ' ']]
            for i in range(length): # go through 1,2,3 [[' ', '_', ' '], ['0', '*', '_'], [' ', '0', ' ']]
                for j in range(len(valueLeave[i])): #go through ' ', '_', ' '  

                    if valueLeave[i][j] == '*':
                        valueLeave[i][j] = '_'
                        valueLeave[i+1][j] = '3'

                        if leftSensor == 0 and valueLeave[i+1][j-1]!='_': # should exist no matter what
                            valueLeave[i+1][j-1]=0
                        #elif leftSensor == '_' and valueLeave[i+1][j-1]!=0:
                        elif leftSensor == 1 and valueLeave[i+1][j-1]!=0:
                            valueLeave[i+1][j-1]='_'

                        if rightSensor == 0 and valueLeave[i+1][j+1]!='_': # should exist no matter what
                            valueLeave[i+1][j+1]=0
                        elif rightSensor == 1 and valueLeave[i+1][j+1]!=0:
                            valueLeave[i+1][j+1]='_'

                        if downSensor == 0:
                            if i<=len(valueLeave)-3: # represents there being enough rows
                                if valueLeave[i+2][j] != '_':
                                    valueLeave[i+2][j] = 0
                            else:
                                newLayer = [' ']*len(value[i])
                                newLayer[j]=0
                                valueLeave.append(newLayer)

                        elif downSensor == 1:
                            if i<=len(valueLeave)-3: # represents there being enough rows
                                if valueLeave[i+2][j] != 0:
                                    valueLeave[i+2][j] = '_'
                            else:
                                newLayer = [' ']*len(value[i])
                                newLayer[j]='_'
                                valueLeave.append(newLayer)


                        break
                

            newMapCollection[itemCount,probLeave*key[1]] = valueLeave
            itemCount+=1

            for key, value in newMapCollection.items():
                for i in range(len(value)): # go through 1,2,3 [[' ', '_', ' '], ['0', '*', '_'], [' ', '0', ' ']]
                    for j in range(len(value[i])):
                        if value[i][j]=='3':
                            value[i][j]='*'

        # print("TESTING INVALID MAPS")
        # for key, value in newMapCollection.items():
        #     print("Map:", key[0], " Probability:", key[1], ":", end = " " )
        #     print("")
        #     for k in range(len(value)):
        #         for l in range(len(value[k])):
        #             print(value[k][l],end = " ")
        #         print("")
            

    #return newMapCollection        
            

    # STEP 2: Check for invalid maps, remove them, and normalize the probability distribution

    for key, value in newMapCollection.items(): # marking each invalid map as 'invalid'
        #print("testing", len(value), value)
        #print("testing,", key)
        for i in range(len(value)): #check each map
            #print("value is", value)
            for j in range(len(value[i])):

                if value[i][j]=='*':

                    if leftSensor==0:
                        if value[i][j-1]!=0 and value[i][j-1]!='0' :
                            #print('value i', value[i])
                            newMapCollection[key] = 'invalid'
                            #print("testing left", key)
                            break

                    elif leftSensor==1:
                        if value[i][j-1]!='_':
                            newMapCollection[key] = 'invalid'
                            
                            break
                      
                    if upSensor==0:
                        if value[i-1][j]!=0:
                            newMapCollection[key] = 'invalid'
                            
                            break
                    elif upSensor==1:
                        
                        if value[i-1][j]!='_':
                            
                            newMapCollection[key] = 'invalid'
                            #print("testing up", key)
                            
                            break
                        
                    if rightSensor==0:
                        # print("TESTING MAPS")
                        # for key, value in newMapCollection.items():
                        #     print("TESTEST, Map:", key[0], " Probability:", key[1], ":", end = " " )
                        #     print("")
                        #     for k in range(len(value)):
                        #         for l in range(len(value[k])):
                        #             print(value[k][l],end = " ")
                        #         print("")
                        #     print("hiya")
        

                        #print(newMapCollection)
                        if value[i][j+1]!=0: # THIS IS THE ISSUE WITH ITERATION 5

                            
                            newMapCollection[key] = 'invalid'
                            break

                    elif rightSensor==1:
                        if value[i][j+1]!='_':
                            #print("MiSTAKE")
                            #print(newMapCollection)
                            newMapCollection[key] = 'invalid'
                            #print("testing right", key)
                            break

                    if downSensor==0:
                        if value[i+1][j]!=0 and value[i][j-1]!='0':
                            #print('value i', value[i+1])
                            newMapCollection[key] = 'invalid'
                            #print("testing down", key)
                            break
                    elif downSensor==1:
                        if value[i+1][j]!='_':
                            newMapCollection[key] = 'invalid'
                            
                            break
                    else:
                        continue


    newnewMapCollection = {}
    itemCount = 1
    probabilitySum = 0 # for normalizing later

    for key,value in newMapCollection.items(): # adding valid maps to a separate dictionary
        if value!='invalid':
            newnewMapCollection[itemCount,key[1]] = value
            itemCount+=1
            probabilitySum+=key[1]    
    
    newnewnewMapCollection = {}
    
    for key,value in newnewMapCollection.items():
        newProb = key[1]/probabilitySum
        newnewnewMapCollection[key[0],newProb] = value


    # STEP 3: create finalMapCollection - combine duplicate maps, and reassign index values

    finalMapCollection = {}
    itemCount = 1

    

    for key, value in newnewnewMapCollection.items():
        if value not in finalMapCollection.values():
            finalMapCollection[(itemCount,key[1])]= value

        else:
            tempKey = next(key for key, Value in finalMapCollection.items() if value == Value)
            newkey = (tempKey[0],key[1]+tempKey[1])
            finalMapCollection[newkey]=finalMapCollection.pop(tempKey)
        itemCount+=1

    '''
    finalMapCollection = {}
    itemCount = 1
    for key, value in newnewnewMapCollection.items():
        if value not in finalMapCollection.values():
            finalMapCollection[(itemCount,key[1])]= value

        else:
            tempKey = next(key for key, Value in finalMapCollection.items() if value == Value)
            newkey = (tempKey[0],key[1]+tempKey[1])
            finalMapCollection[newkey]=finalMapCollection.pop(tempKey)
        itemCount+=1
    '''


    # STEP 4: SORT THE MAPS BY ORDER (least algorthmically difficult)

    FinalMapCollection =  dict(sorted(finalMapCollection.items(), key=lambda item: item[0][0]))
    itemCounter = 1
    FInalMapCollection = {}

    for key, value in FinalMapCollection.items():
        FInalMapCollection[(itemCounter,key[1])]=value
        itemCounter+=1

    

    '''
    FinalMapCollection =  dict(sorted(finalMapCollection.items(), key=lambda item: item[0][0]))
    itemCounter = 1
    FInalMapCollection = {}

    for key, value in FinalMapCollection.items():
        FInalMapCollection[(itemCounter,key[1])]=value
        itemCounter+=1

    return FInalMapCollection
    '''


    #return newnewnewMapCollection # represents mapCollection after step 1
    #return finalMapCollection
    return FInalMapCollection   



def printMapCollection(mapCollection): #DONE

    for key, value in mapCollection.items():
        print("Map:", key[0], " Probability:", key[1], ":", end = " " )
        print("")
        for i in range(len(value)):
            for j in range(len(value[i])):
                print(value[i][j],end = " ")
            print("")


def printActualEnvironment(environment, actualIndex): #DONE
    #print(actualIndex)
    environment[actualIndex[0]][actualIndex[1]]='*'

    for i in range(len(environment)):
        for j in range(len(environment[i])):
            print(environment[i][j],end=" ")
        print("")


def generateNewenvironment(length, width):
    environment=[]
    environment.append([0]*length)
    for i in range(width-2):
        layer = ['_']*length
        layer[0]=0
        layer[len(layer)-1]=0
        environment.append(layer)

    environment.append([0]*length)
    return environment



# START CODE

#environment = [[0,0,0,0,0,],[0,'_','_','_',0],[0,0,'_','_',0],[0,'_',0,'_',0], [0,'_','_','_',0], [0,0,0,0,0]]
#environment = [[0,0,0,0,0,0],[0,'_','_','_','_',0],[0,'_','_','_','_',0],[0,'_','_','_','_',0], [0,'_','_','_','_',0], [0,0,0,0,0,0]]
#environment = [[0,0,0,0,0,0],[0,'_','_','_','_',0],[0,'_','_','_','_',0], [0,'_','_','_','_',0], [0,0,0,0,0,0]]
#environment = [[0,0,0,0,0,0],[0,'_',0,'_','_',0],[0,0,'_','_','_',0], [0,'_','_',0,'_',0], [0,'_','_',0,'_',0], [0,0,'_','_','_',0], [0,'_','_',0,'_',0], [0,'_',0,'_','_',0], [0,0,0,0,0,0]]

# environment = [[0,0,0,0,0,0],
#                [0,'_','_','_','_',0], 
#                [0,'_','_','_','_',0], 
#                [0,'_','_','_','_',0], 
#                [0,'_','_','_','_',0], 
#                [0,'_','_','_','_',0], 
#                [0,'_','_',0,'_',0], 
#                [0,'_','_','_','_',0], 
#                [0,'_','_','_','_',0], 
#                [0,'_',0,'_','_',0], 
#                [0,'_','_','_','_',0], 
#                [0,0,0,0,0,0]]



# environment = [[0,0],
#                [0,'_',0,0,0,0], 
#                [0,'_','_','_','_',0], 
#                #[0,'_','_','_','_',0], 
#                #[0,'_','_','_','_',0], 
#                #[0,'_','_','_','_',0], 
#                [0,'_',0,'_',0], 
#                [0,'_','_','_','_',0], 
#                #[0,'_','_','_','_',0], 
#                [0,'_',0,'_','_',0], 
#                [0,'_','_','_',0], 
#                [0,0,0,0,0]]

# environment = [[0,0,0,0,0,0],
#                [' ',0,'_','_','_','_',0],
#                [' ',' ',0,'_','_','_','_',0],
#                [' ',' ',' ',0,'_','_','_','_',0],
#                [' ',' ',' ',' ',0,0,0,0,0,0]]


# environment = [[0,0,0,0,0,0,0,0,0,0,0,0],
#                [0,'_','_','_',0,'_','_','_','_','_','_',0],
#                [0,'_','_','_','_','_',0,0,0,'_','_',0],
#                [0,'_','_',0,0,'_','_',0,'_','_','_',0],
#                [0,'_','_',0,'_','_','_','_',0,0,'_',0],
#                #[0,'_','_','_','_','_','_','_','_','_','_',0],
#                #[0,'_','_','_','_','_','_','_','_','_','_',0],
#                [0,0,0,0,0,0,0,0,0,0,0,0]]

# environment = [[0,0,0,0],
#                [0,'_','_',0],
#                [0,'_','_',0],
#                [0,'_','_',0],
#                [0,0,0,0]]


environment = [[0,0,0,0,0,0],
               [0,'_','_','_','_',0],
               [0,'_',0,0,'_',0],
               [0,'_',0,0,'_',0],
               [0,'_',0,0,'_',0],
               [0,'_','_','_','_',0],
               [0,0,0,0,0,0]]


# environment = generateNewenvironment(7,8)
# environment[3][4]=0
#print(newEnvironment)



# make rectangle
# what are ways you can make the agent get confused, cases where the sensor data would get confused


actualIndex = [1,2] # first index represents up or down, second index represents right or left
probLeave = 2/3
mapCollection = {(1,1):[[' ', ' ', ' '],[' ','*',' '],[' ', ' ', ' ']]}
#mapCollection = {(1,1):[[3,3,3,],[3,'*',3],[3,3,3]]}
printActualEnvironment(copy.deepcopy(environment),actualIndex)


# creating initial environment
sensorData = gainSensorData(environment,actualIndex)
print(sensorData)

if sensorData[0]==1: # checking left, if it is empty space
    mapCollection[1,1][1][0] = '_'
else:
    mapCollection[1,1][1][0] = 0

if sensorData[1]==1: # checking up, if it is empty space
    mapCollection[1,1][0][1] = '_'
else:
    mapCollection[1,1][0][1] = 0

if sensorData[2]==1: # checking right, if it is empty space
    mapCollection[1,1][1][2] = '_'
else:
    mapCollection[1,1][1][2] = 0

if sensorData[3]==1: # checking down, if it is empty space
    mapCollection[1,1][2][1] = '_'
else:
    mapCollection[1,1][2][1] = 0

print("")
printMapCollection(mapCollection)

print("________") # this marks where the actual coding starts


''' Current steps
direction = getDirection(sensorData)
print(direction)
actualIndex = actualMovement(direction,actualIndex,probLeave)
print(actualIndex)
sensorData=gainSensorData(environment,actualIndex)
print(sensorData)

printActualEnvironment(copy.deepcopy(environment),actualIndex)
'''


#printActualEnvironment(copy.deepcopy(environment),actualIndex)



for i in range(600):
    print("     ITERATION",i+1)
    direction = getDirection(sensorData)
    actualIndex=actualMovement(direction,actualIndex,probLeave)
    sensorData=gainSensorData(environment,actualIndex)
    print("robot is trying to move", direction, "robot gains", sensorData)
    mapCollection = updateMaps(mapCollection,direction,sensorData,probLeave)
    printMapCollection(mapCollection)
    print(" ")


printActualEnvironment(copy.deepcopy(environment),actualIndex)

#print(newEnvironment)