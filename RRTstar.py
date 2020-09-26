import pygame 
import random as r
import pylineclip as lc

############################################
## Constants
############################################

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
PURPLE = (128,0,128)

# This sets the wdith of the screen 
WIDTH = 800
WINDOW_SIZE = [WIDTH, WIDTH]

# RRT Constants
NODE_RADIUS = 4     # The radius of a node as it is drawn on the pygame screen
RRT_RADIUS = 20     # The radius used to place new nodes
SEARCH_RADIUS = 30  # The radius searched when considering reconnecting nodes
END_RADIUS = 20     # The allowable distance from the end node needed to end the algorithm
NODES = 20          # The number of new nodes created in a single step of the algorithm

############################################
## Classes
############################################

class obstacle():
    '''
    This class represents an obstacle in the grid ans stores the positional data associated with a given obstacle
    '''

    def __init__(self,x1,y1,x2,y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

class node():
    '''
    This class represents an RRT node and stores the necessary information associated with that node.
    '''

    def __init__(self,x,y):
        # Positional Data
        self.x = x
        self.y = y

        # Node cost (distance of path to this point)
        self.cost = 0

        # Start/end or path
        self.start = False
        self.end = False
        self.path = None

    
############################################
## Functions
############################################

def between(sample,b1,b2):
    '''
    This function takes a sample integer and checks to see if that integer is between to outher boundary integers
    b1 and b2
    '''

    if b1 <= sample and sample <= b2:
        return True
    elif b2 <= sample and sample <= b1:
        return True
    else: 
        return False

def euclidean(x1,y1,x2,y2):
    '''
    This function calculates the Euclidean distance between two points. Note that the arguments are the
    individual x and y values of the two points, not two pairs of points.
    '''
    ans = ((x1-x2)**2 + (y1-y2)**2)**.5
    return ans

def updatePOS(closest,pos):
    '''
    This function is part of the RRT* algorithm that is used to set the location of a new node. To do this, a 
    random point is generated anywhere on the map and the node closest to that is found. This function takes those 
    two as inputs and calculates a new position by taking the nearest node and moving a constant distance (RRT_RADIUS)
    in the direction of the random point 

    closest - nearest node to random point
    pos - random point coordinates [x,y]
    '''

    # Vector from closest to pos 
    vector = [pos[0]-closest.x,pos[1]-closest.y]

    # Adjust vector to RRT radius length
    magnitude = (vector[0]**2 + vector[1]**2)**.5
    normed_vector = [x / magnitude * RRT_RADIUS for x in vector]

    # Calculate the position of the new node
    new_pos = [int(closest.x+normed_vector[0]),int(closest.y+normed_vector[1])]

    return new_pos

def drawBoard(obstacles, nodes):

    # Set the screen background
    screen.fill(WHITE)

    # Draw obstacles
    for i in obstacles:
        w = i.x2-i.x1
        h = i.y2-i.y1

        rectangle = pygame.rect.Rect(i.x1,i.y1,w,h)
        pygame.draw.rect(screen, BLACK, rectangle)

    # Draw nodes
    if nodes != []:
        for i in nodes:
            if i.start or i.end:
                continue
            pygame.draw.circle(screen,RED,(i.x,i.y),NODE_RADIUS)        # Draws node
            pygame.draw.line(screen,RED,(i.x,i.y),(i.path.x,i.path.y))  # Draws links between nodes
        pygame.draw.circle(screen,BLUE,(start.x,start.y),NODE_RADIUS)   # Draws start node
        pygame.draw.circle(screen,YELLOW,(end.x,end.y),END_RADIUS)      # Draws end circle around end node.
        pygame.draw.circle(screen,PURPLE,(end.x,end.y),NODE_RADIUS)     # Draws end node

def endGame(end_node):
    '''
    This function  is called at the end of the RRT* algorithm when a path to the end node has been found.
    It takes the end_node and redraws the complete path using purple instead of the standard red.
    '''

    # Draw the path in purple starting from the end node
    current = end_node
    while current.path is not None:
        pygame.draw.circle(screen,PURPLE,(current.x,current.y),NODE_RADIUS)     # Draw nodes in the path
        pygame.draw.line(screen,PURPLE,(current.x,current.y),(current.path.x,current.path.y))   # Draw links between nodes
        current = current.path  # Move back to the prior node in the path.
        
    # Update the screen
    pygame.display.flip()


############################################
## Visualization
############################################

# Initialize pygame
pygame.init()
 
# Set the size of the screen

screen = pygame.display.set_mode(WINDOW_SIZE)

# Set the screen background
screen.fill(WHITE)
 
# Set title of screen
pygame.display.set_caption("RRT* Pathfinding Algorithm")

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Go ahead and update the screen with what we've drawn.
pygame.display.flip()

# Shape variables
x1 = x2 = y1 = y2 = 0

# RRT variables
obstacles = []      # List to hold the obstacle objects
nodes = []          # List to hold the node objects
placed = False      # Has the user finished placing objects?
Started = False     # Has the user started the algorithm?
start = None        # start node
end = None          # end node
found = False       # Has a path been found from start to stop
drawing = False     # Is user currently drawing an obstacle (used to show obstacles as user is drawing with click-drag)

############################################
## Main Loop
############################################

done = False
while not done:

    # Board setup
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop

        # If user presses the spacebar, switch from placing obstacles to placing start and end or the algorithm starts.
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if placed:
                Started = True
            else:
                placed = True

        # Skip setup commands if algorithm has started
        if Started:
            continue

        # Create obstacle

        # User clicks and the position is svaed
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not placed:
            x1, y1 = event.pos
            drawing = True

        # Draw obstacle as user is dragging cursor on screen
        elif event.type == pygame.MOUSEMOTION and drawing == True:
            x2, y2 = event.pos
            w = x2-x1
            h = y2-y1
            drawBoard(obstacles,nodes)
            rectangle = pygame.rect.Rect(x1,y1,w,h)
            pygame.draw.rect(screen, BLACK, rectangle)

        # Draw and save obstacle when user releases mouse
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and not placed:
            x2, y2 = event.pos
            w = x2-x1
            h = y2-y1

            rectangle = pygame.rect.Rect(x1,y1,w,h)
            pygame.draw.rect(screen, BLACK, rectangle)
            obstacles.append(obstacle(x1,y1,x2,y2))
            drawing = False

        # Create start node
        elif pygame.mouse.get_pressed()[0] and placed and start is None:
            # User clicks the mouse. Get the position
            pos = pygame.mouse.get_pos()
            start = node(pos[0],pos[1])
            start.start = True
            nodes.append(start)
            pygame.draw.circle(screen,BLUE,(start.x,start.y),NODE_RADIUS)

        # Create end node
        elif pygame.mouse.get_pressed()[2] and placed and end is None:
            # User clicks the mouse. Get the position
            pos = pygame.mouse.get_pos()
            end = node(pos[0],pos[1])
            end.end = True
            pygame.draw.circle(screen,YELLOW,(end.x,end.y),END_RADIUS)
            pygame.draw.circle(screen,PURPLE,(end.x,end.y),NODE_RADIUS)

    # RRT* Algorithm
    if Started:

        # Set up algorithm
        invalid = False     # True if node placement is invalid
        num = 0             # Number of valid nodes succesfully placed
        
        # Add NODES amount of nodes
        while num<=NODES:

            # Generate random position
            pos = [r.randint(0,WIDTH-1),r.randint(0,WIDTH-1)]
            
            # Find the closest node to that position
            closest = start
            for i in nodes:
                distance = euclidean(i.x,i.y,pos[0],pos[1])
                if euclidean(closest.x,closest.y,pos[0],pos[1]) > euclidean(i.x,i.y,pos[0],pos[1]):
                    closest = i
                if distance == 0:
                    invalid = True
            
            # If the node is on top of another node, try again
            if invalid:
                invalid = False
                continue

            # Update the position to be RRT_RADIUS away from the closest node in the direction of the original position
            pos = updatePOS(closest,pos)

            # Check to see if the node is in an obstacle and if so try again
            for i in obstacles:
                if between(pos[0],i.x1,i.x2) and between(pos[1],i.y1,i.y2):
                    invalid = True
                    break

            if invalid:
                invalid = False
                continue

            # Find the cheapest node in RRT_RADIUS 
            cheapest = closest
            for i in nodes:
                if euclidean(i.x,i.y,pos[0],pos[1]) <= SEARCH_RADIUS and i.cost < cheapest.cost:
                    cheapest = i
            
            # If line between cheapest and new node intersects obstacle, try again
            for i in obstacles:
                xlist = [i.x1,i.x2]
                ylist = [i.y1,i.y2]
                x3,y3,x4,y4 = lc.cohensutherland(min(xlist), max(ylist), max(xlist), min(ylist), cheapest.x, cheapest.y, pos[0], pos[1])
                if x3 is not None or y3 is not None or x4 is not None or y4 is not None:
                    invalid = True
                    break

            if invalid:
                invalid = False
                continue
            
            # If completely successful, create new node connected to cheapest near node
            newNode = node(pos[0],pos[1])
            newNode.cost = cheapest.cost + euclidean(newNode.x,newNode.y,cheapest.x,cheapest.y)
            newNode.path = cheapest     # Stores the node that the newNode is linked to

            # Record and store the new node
            nodes.append(newNode)
            num+=1

            # Rewire nearby nodes if cheaper to do so
            for i in nodes:
                tempCost = newNode.cost + euclidean(newNode.x,newNode.y,i.x,i.y)
                if tempCost < i.cost and euclidean(newNode.x,newNode.y,i.x,i.y)< SEARCH_RADIUS:
                    i.path = newNode
                    i.cost = tempCost

            # Check if end has been found
            if euclidean(newNode.x,newNode.y,end.x,end.y) <= END_RADIUS:
                end.path = newNode
                found = True


        # Draw new nodes to board
        drawBoard(obstacles,nodes)

    # End node has been found
    if found:
        # Draw the path to the end node
        endGame(end)
        go = False

        # Allow the user to continue algorithm to add more nodes and optimize path
        while not go:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    go = True
                if event.type == pygame.QUIT:  # If user clicked close
                    done = True  # Flag that we are done so we exit this loop
                    go = True

    pygame.display.flip()
            
# End the pygame instance
pygame.quit()