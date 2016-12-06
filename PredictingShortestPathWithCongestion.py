#importing classes to read the files and other operations
import sys
import time



#reading file name from command line input
try:
    filename = input("\nEnter the file Name:")
    
    #Opening file in read only format to read the data into edge, flow and capacity matrices
    file1 = open(filename, 'r')

#If file not found then print error message and exit from code
except IOError:
    print('\nIncorrect Filename\n')
    sys.exit(0)


#First split the file to lists based on new line character'\n'
f1 = file1.read().splitlines()

#Next split the lists into individual items by ','
f2 = [i.split(',') for i in f1]

#Initialize INF to use at the place where the path is not available or valid
INF=999999999

#a,b are s,t like start and terminal node in the given file
start=int(f2[0][1].strip())
dest=int(f2[0][2].strip())

#n is number of nodes
n=int(f2[0][0].strip())


#Initializing Edge, Flow, Capacity, Initial Load(calculated from Flow Matrix), G(Actual Edge Delay) and Actual Path Delay matrices to INF (Infinite value, in this case INF -> 999999999)
Edge=[[INF for row in range(0,n)] for col in range(0,n)]
Flow=[[INF for row in range(0,n)] for col in range(0,n)]
Capacity=[[INF for row in range(0,n)] for col in range(0,n)]
Load=[[INF for row in range(0,n)] for col in range(0,n)]
actualEdgeDelay=[[INF for row in range(0,n)] for col in range(0,n)]
designedApproachActualEdgeDelay=[[INF for row in range(0,n)] for col in range(0,n)]

#Initializing newly calculated Actual Edge Delay and Actual Path Delay after our Accept and Allocating one car at one time for each s-t pair
actualPathDelay=[[0 for row in range(0,n)] for col in range(0,n)]
designedApproachActualPathDelay=[[0 for row in range(0,n)] for col in range(0,n)]

#Initializing Load Matrix for Our Approach usage
newLoad=[[0 for row in range(0,n)] for col in range(0,n)]

#Make diagonal values of Edge, Flow, Capacity, Load, Actual Edge Delay, Actual Path Delay and our approach Actual Edge & Path Delay matrices to 0 /or if i==j to 0
for i in range(0,n):
    Edge[i][i]=0
    Flow[i][i]=0
    Capacity[i][i]=0
    Load[i][i]=0
    actualEdgeDelay[i][i]=0
    designedApproachActualEdgeDelay[i][i]=0
    actualPathDelay[i][i]=0
    designedApproachActualPathDelay[i][i]=0

#tot variable is length of total lines in the given file so that we can traverse till end of the file to get Edge, Flow and Capacity Matrix values
tot=len(f2)

#Loop to read each and every list from the f2 variable
for i in range(1,tot):
    code=f2[i][0]##First alphabet character to identify to which matrix or array to push into like if E then push to E[][],edge matrix
    fromNode=int(f2[i][1].strip())-1#From node, strip to eliminate any empty spaces
    toNode=int(f2[i][2].strip())-1#To node, strip to eliminate any empty spaces
    value1=int(f2[i][3].strip())#Value of From - To Node
    #Based on code character push to respective array/matrix
    if code=='E':
        Edge[fromNode][toNode] = value1
    elif code=='F':
        Flow[fromNode][toNode] = value1
    elif code=='C':
        Capacity[fromNode][toNode] = value1

#Printing Edge, Flow and Capacity matrix to check the file
print("\nGiven Edge Matrix in file:\n")
for elem in Edge:
    print(elem)
print("\nGiven Flow Matrix in file:\n")
for elem in Flow:
    print(elem)
print("\nGiven Capacity Matrix in file:\n")
for elem in Capacity:
    print(elem)


##This block of code is used to declare and initialize Dictionaries for Shortest Path dictionary, Path Route dictionary and Hop Count dictionary
if __name__ == '__main__':

    #Create newEdge empty dictionary for calculating Shortest Path
    shortestEdge={}

    #Create Paths empty dictionary for calculating Path Route
    shortPaths={}

    #Create HopCount empty dictionary for calculating Hop Count
    hopCount={}

    #Intialize shortestEdgedge dictionary based on Edge matrix/array (pushing values from E to newEdge dictionary) also initializing hopcount
    for i in range(1,n+1):
        shortestEdge[i]={}
        shortPaths[i]={}
        hopCount[i]={}
        for j in range(1,n+1):
            shortestEdge[i][j]=Edge[i-1][j-1]
            #Initializing shortPaths to i,j if no INFINITE value or i!=j, like identifying 1 hop paths first
            if i!=j and Edge[i-1][j-1]!=INF:
                shortPaths[i][j]=[i,j]
            elif i==j:
                shortPaths[i][j]=[i]
            elif Edge[i-1][j-1]==INF:
                shortPaths[i][j]=[0]
            hopCount[i][j]=0

##Applying floyd warshall algorithm to calculate all-pairs-shortest-paths for a given edge matrix
for k in range(1,n+1):
    for i in range(1,n+1):
        for j in range(1,n+1):
            if shortestEdge[i][k]+shortestEdge[k][j]<shortestEdge[i][j]:
                shortestEdge[i][j] = shortestEdge[i][k]+shortestEdge[k][j]
                #Saving path to new path after changing the value in shortest path adjacent matrix by taking shortPaths[ik]-lastvalue+shortPaths[kj] to remove duplicate nodes in path
                shortPaths[i][j]=shortPaths[i][k][0:len(shortPaths[i][k])-1]+shortPaths[k][j]

#Printing predicted path after performing floyd warshall algorithm
print("\nPredicted Path Length after performing all-pairs-shortest-paths for a single car is :\n")
for elem in shortestEdge:
    for y in shortestEdge[elem]:
        print(shortestEdge[elem][y],end="\t")
    print()

print("\nActual all-pairs-shortest-paths for a single car is:\n")
for elem in shortPaths:
    for y in shortPaths[elem]:
        count=len(shortPaths[elem][y])-1
        #Calculating hopCount while printing paths
        hopCount[elem][y]=count
        print(shortPaths[elem][y],end="\t")
    print()

#Calculation of maximum hopCount and printing hopCount values
maxhop=0
print("\nHop Count for Shirt Edge matrix:\n")
for elem in hopCount:
    for y in hopCount[elem]:
        if maxhop<hopCount[elem][y]:
            maxhop=hopCount[elem][y]
        if hopCount[elem][y]==1:
            newLoad[elem-1][y-1]=1
        print(hopCount[elem][y],'\t',end="")
    print()

#Calculation of Load Matrix (Edge Traffic)
for i in range(1,n+1):
    for j in range(1,n+1):
        if hopCount[i][j]==1:
            Load[i-1][j-1]=0
            for a in range(1,n+1):
                for b in range(1,n+1):
                    for k in range(0,hopCount[a][b]):
                        if shortPaths[i][j][0]==shortPaths[a][b][k]:
                            if shortPaths[i][j][1]==shortPaths[a][b][k+1]:
                                Load[i-1][j-1]=Load[i-1][j-1]+Flow[a-1][b-1]
        elif hopCount[i][j]!=0 and Edge[i-1][j-1]==INF:
            Load[i-1][j-1]=INF
        else:
            Load[i-1][j-1]=0

#Calculation of Actual Edge Delays(G matrix = (C+1)*E/(C+1-L)) for initial approach (Given by professor)
for i in range(0,n):
    for j in range(0,n):
        if Capacity[i][j]!=INF:
            if Capacity[i][j]>=Load[i][j]:
                actualEdgeDelay[i][j]=round(((Capacity[i][j]+1)*Edge[i][j])/((Capacity[i][j]+1)-Load[i][j]),2)
            else:
                actualEdgeDelay[i][j]=INF
        else:
            actualEdgeDelay[i][j]=INF

#Printing Actual Edge Delays (G Matrix)
print("\nActual Edge Delay G Matrix for approach provided:\n")
for elem in actualEdgeDelay:
    print(elem)

#Calculation of Actual Path Delay from Actual Edge Delays (G matrix) for initial approach (Given by professor)
for i in range(0,n):
    for j in range(0,n):
        if hopCount[i+1][j+1]==1:
            actualPathDelay[i][j]=actualEdgeDelay[i][j]
        elif hopCount[i+1][j+1]>1:
            for k in range(0,hopCount[i+1][j+1]):
                ab=shortPaths[i+1][j+1][k]-1
                cd=shortPaths[i+1][j+1][k+1]-1
                actualPathDelay[i][j]=round(actualPathDelay[i][j]+actualEdgeDelay[ab][cd],2)

for i in range(0,n):
    for j in range(0,n):
        if actualPathDelay[i][j]>=INF:
            actualPathDelay[i][j]=INF
        if actualEdgeDelay[i][j]>=INF:
            actualEdgeDelay[i][j]=INF
        

print("\nActual Path Delay G Matrix for approach provided:\n")
for elem in actualPathDelay:
    print(elem)


#Our approach for one complete set of cars for an s,t pair
#Approach : Accept and Allocate all s-t traffic "One car at one time for each s-t pair" such that s and t are one hop away from each other, followed by all s-t pairs that are two hops away and so on.
##Initial case for hop 1

startTime = time.time()
for i in range(0,n):
    for j in range(0,n):
        if Capacity[i][j]!=INF:
            if Capacity[i][j]>=newLoad[i][j]:
                designedApproachActualEdgeDelay[i][j]=round(((Capacity[i][j]+1)*Edge[i][j])/((Capacity[i][j]+1)-newLoad[i][j]),2)
            else:
                designedApproachActualEdgeDelay[i][j]=INF
        else:
            designedApproachActualEdgeDelay[i][j]=INF

##After done with 1 hop then for remaining hops apply the formula with hop matrix as load repeatedly to the same matrix as weights
for o in range(1,maxhop):
    #Reset New Load matrix to 0 once again for one such hopcount
    for x in range(0,n):
        for y in range(0,n):
            newLoad[x][y]=0
      
    for i in range(0,n):
        for j in range(0,n):
            if o+1<=hopCount[i+1][j+1]:
                u=shortPaths[i+1][j+1][o]
                v=shortPaths[i+1][j+1][o+1]
                if len(shortPaths[u][v])==2:
                    newLoad[u-1][v-1]=1

    for i in range(0,n):
        for j in range(0,n):
            designedApproachActualEdgeDelay[i][j]=round(((Capacity[i][j]+1)*designedApproachActualEdgeDelay[i][j])/((Capacity[i][j]+1)-newLoad[i][j]),2)

endTime = time.time()

print("\nActual Edge Delay G Matrix for our designed approach:\n")
for elem in designedApproachActualEdgeDelay:
    print(elem)

#Calculating Actual Path Delay based on Actual Edge Delay matrix
for i in range(0,n):
    for j in range(0,n):
        if hopCount[i+1][j+1]==1:
            designedApproachActualPathDelay[i][j]=designedApproachActualEdgeDelay[i][j]
        elif hopCount[i+1][j+1]>1:
            for k in range(0,hopCount[i+1][j+1]):
                ab=shortPaths[i+1][j+1][k]-1
                cd=shortPaths[i+1][j+1][k+1]-1
                designedApproachActualPathDelay[i][j]=round(designedApproachActualPathDelay[i][j]+designedApproachActualEdgeDelay[ab][cd],2)

for i in range(0,n):
    for j in range(0,n):
        if designedApproachActualPathDelay[i][j]>=INF:
            designedApproachActualPathDelay[i][j]=INF
        if designedApproachActualEdgeDelay[i][j]>=INF:
            designedApproachActualEdgeDelay[i][j]=INF
        
#Printing Actual Path Delay for designed approach
print("\nActual Path Delay G Matrix for our designed approach:\n")
for elem in designedApproachActualPathDelay:
    print(elem)

#Calculation of percentage change for Actual Path Length and Predicted Path Length
print("\nActual and Predicted path Difference (in percentage):\n")
perCalc=0
for i in range(0,n):
    for j in range(0,n):
        if i!=j:
            perCalc=designedApproachActualPathDelay[i][j]*100
            perCalc=(perCalc)/shortestEdge[i+1][j+1]
            perCalc=perCalc-100
            if perCalc>0:
                print(round(perCalc,2),end='\t')
            else:
                print("0",end='\t')
        else:
            print("0",end='\t')
    print()

ShortestPredEdgeLength=Edge[start-1][dest-1]
DesShortestPredEdgeLength=designedApproachActualEdgeDelay[start-1][dest-1]
if ShortestPredEdgeLength==INF:
    ShortestPredEdgeLength="\'NA\'"
if DesShortestPredEdgeLength==INF:
    DesShortestPredEdgeLength="\'NA\'"

#Printing the path lengths and edge lengths along with hopcount for given start and end nodes
print("\nShortest Predicted Path Length is:",shortestEdge[start][dest],"and Actual Path length is:",designedApproachActualPathDelay[start-1][dest-1],"from",start,"to",dest)
print("\nShortest Predicted Edge Length:",ShortestPredEdgeLength,"and Actual Edge length:",DesShortestPredEdgeLength,"from",start,"to",dest)
print("\nThe hop-count of the path between",start,"and",dest,"is:",hopCount[start][dest])


print ("\nStart Time: ",startTime,", End Time: ",endTime,", Total Time taken: ",endTime - startTime," seconds -> Time taken to execute the file")
