# NEOCIS Software Assessment 5/14/2025 CSAIZ
# 2D graphics projection of 3D object

from tkinter import *
import numpy as np
import math

# Global variables ----------------------------------------
# user defined variables
filePath = "C:\\Users\\christian.saiz\\Documents\\0_NOAA\\Coding_courses\\3DPoly\\Ex\\object.txt"
canvas_width = 800
canvas_height = 600
scale = 100 # each coordinate defined in the vertices is multiplied by this parameter

# derived variables
x_offset = canvas_width/2 # offset to center in canvas given that (0,0) is the top-left corner
y_offset = canvas_height/2
z_offset = 0 # projections only in xy plane

# function definitions ----------------------------------------

# returns a list of file lines
def get_lines(filePath):
    fileList = []
    with open(filePath, 'r') as file:
        for line in file:
            fileList.append(line)
    return fileList


# returns a list vertices
def get_vertices(fileData):
    # extract number of vertices 
    vnum = int(fileData[0].split(',')[0])
      
    vertices = []
    # start from 2 line collecting vertices
    for i in range(1,vnum+1):
        if fileData[i] != '\n':            
            # get id and coords "1,1.0,0.0,0.0"
            data = fileData[i].split(',')            
            coord = [float(data[1]),float(data[2])*-1,float(data[3])] # this will always contain 3 values            
            # append vertix to list
            vertices.append(coord)           
            
        else:
            print("Error retreiving vertix!")
            return -1

    #print(vertices) # list of vertices
    return vertices


# returns a list of face id nodes
def get_faces(fileData):
    #extract number of faces
    vnum = int(fileData[0].split(',')[0])
    fnum = int(fileData[0].split(',')[1])

    faces = []
    # start from line vnum+1 collecting vertices
    for i in range(vnum+1,vnum+fnum+1):
        if fileData[i] != '\n':
            # get face edges
            data = fileData[i].split(',')
            dataLen = len(data)
            # the edge count depends on the object
            thisface = []
            for j in range (0,dataLen):
                thisface.append(int(data[j]))
            #thisface = [int(data[0]),int(data[1]),int(data[2])]
            #print(thisface)
            faces.append(thisface)
        else:
            print("Error retreiving faces!")
            return -1

    return faces

# get the center of the 3D object
def get_center(vertices):    
    sum = np.array([0,0,0])
    # calculate average on xyz
    for vertix in vertices:
        vector = np.array(vertix) * scale
        sum = sum + vector
    center = sum/len(vertices)
    #print(sum,center)
    return center


# draw circles on each vertix
def draw_vertices(vertices, size):
    global canvas    
    xc, yc = [bodyCenter[0], bodyCenter[1]] # bodycenter offsets
    nodeid = 1
    for vertix in vertices:
        node = np.array(vertix) * scale
        # draw circles and apply center canvas and body center offsets
        canvas.create_oval(node[0] - xc + x_offset - size/2, node[1] - yc + y_offset - size/2,
                            node[0] - xc + x_offset + size/2, node[1] - yc + y_offset + size/2 , fill = 'blue')
        canvas.create_text(node[0] - xc + x_offset + size, node[1] - yc + y_offset + size, text = str(nodeid), fill="red")
        nodeid = nodeid + 1

# draw all faces based on a vertices and faces list
def draw_figure(vertices, faces):
    global canvas 
    xc, yc = [bodyCenter[0], bodyCenter[1]]  # bodycenter offsets
    # draw vertices 
    draw_vertices(vertices, 10)
    # draw edges
    nodeNum = len(faces[0]) # number of nodes in face                  
    # loop through the faces and connect edges
    for face in faces:
        # within a face, plot nodes 0 to nodeNum-1, each edge is (nodei,nodei+1)
        for i in range(0,nodeNum-1):
            nodeA = np.array(vertices[face[i]-1]) * scale
            nodeB = np.array(vertices[face[i+1]-1]) * scale   
            canvas.create_line(nodeA[0] - xc + x_offset, nodeA[1] - yc + y_offset, nodeB[0] - xc + x_offset, nodeB[1] - yc + y_offset, fill = 'blue')
        # plot last closing edge between node0 and last node
        nodeA = np.array(vertices[face[0]-1]) * scale
        nodeB = np.array(vertices[face[nodeNum-1]-1]) * scale
        canvas.create_line(nodeA[0] - xc + x_offset, nodeA[1] - yc + y_offset, nodeB[0] - xc + x_offset, nodeB[1] - yc + y_offset, fill = 'blue')     

   
# get matrix with xy plane projection factors for rotation around X-axis
def rotate_x(theta):
    return [
        [1, 0, 0],
        [0, math.cos(theta), -math.sin(theta)],
        [0, math.sin(theta), math.cos(theta)],
    ]

# get matrix with xy plane projection factors for rotation around Y-axis
def rotate_y(theta):
    return [
        [math.cos(theta), 0, math.sin(theta)],
        [0, 1, 0],
        [-math.sin(theta), 0, math.cos(theta)],
    ]

# get matrix with xy plane projection factors for rotation around Z-axis
def rotate_z(theta):
    return [
        [math.cos(theta), -math.sin(theta), 0],
        [math.sin(theta), math.cos(theta), 0],
        [0, 0, 1],
    ]

# draw 3D object on canvas based on dx,dy mouse displacement
def draw_body(dx,dy):
    global vertices, edges
    rf = 0.01 # rotation factor of dx,dy
    rotation_matrix = np.dot(rotate_x(dy*rf), np.dot(rotate_y(-dx*rf), rotate_z(0)))
    vertices = [np.dot(rotation_matrix, vertex) for vertex in vertices]
    canvas.delete('all')
    draw_figure(vertices, edges)


# this handler is triggered with a mouse click and drag motion
def mouse_handler(event):
    global prev    
    dx = event.x - prev.x
    dy = event.y - prev.y
    prev = event
    print("[dx,dy]:", dx, dy)
    draw_body(dx,dy)

# this handler is only triggeredd on the first mouse click, to provide initial previous mouse position
def button_handler(event):
    global prev
    prev = event
    


# main ------------------------------------------------------------
def main():
    global root, canvas, vertices, edges, bodyCenter
    
    
    # retreive relevant data from file
    data = get_lines(filePath)
    vertices = get_vertices(data)
    edges = get_faces(data)
    bodyCenter = get_center(vertices)
    # create window and canvas

    root = Tk()
    canvas = Canvas(root, width=canvas_width, height=canvas_height, background = 'white')
    canvas.pack()

    # draw initial view of object
    draw_body(0,0)    
    # bind mouse events for object rotation
    canvas.bind('<ButtonPress>', button_handler)
    canvas.bind("<B1-Motion>", mouse_handler)
    
    # mainloop event
    root.mainloop()


    return 0
# main ------------------------------------------------------------



if __name__ == "__main__":
    main()
