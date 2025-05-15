# NEOCIS Software Assessment 5/14/2025 CSAIZ
# 2D graphics projection of 3D object

from tkinter import *
import numpy as np
import math

# Global variables ----------------------------------------
x_offset = 200
y_offset = 200
z_offset = 200

# class definitions ----------------------------------------
class vertix:
    def __init__(self, idv, coord):
        self.idv = idv
        self.coord = coord
    
class polyObject:
    def __init__(self, vnum, enum, vertices, edges):        
        self.vnum = vnum
        self.enum = enum    
        self.vertices = vertices # list of vertix classes
        self.faces = faces
# use as print(myobj.vnum, myobj.vertices[1].idv)


# function definitions ----------------------------------------

# returns a list of file lines
def get_lines(filePath):
    fileList = []
    with open(filePath, 'r') as file:
        for line in file:
            fileList.append(line)
    return fileList


# returns a list of vertix classes
def get_vertices_class(fileData):
    # extract number of vertices 
    vnum = int(fileData[0].split(',')[0])
      
    vertices = []
    # start from 2 line collecting vertices
    for i in range(1,vnum+1):
        if fileData[i] != '\n':            
            # get id and coords "1,1.0,0.0,0.0"
            data = fileData[i].split(',')            
            idv = int(data[0])
            coord = [float(data[1]),float(data[2]),float(data[3])] # this will always contain 3 values
            # create vertix object
            thisvertix = vertix(idv,coord)
            #print(thisvertix.idv, thisvertix.coord)
            # append vertix to list
            vertices.append(thisvertix)           
            
        else:
            print("Error retreiving vertix!")
            return -1

    #print(vertices) # list of vertices
    return vertices


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
            coord = [float(data[1]),float(data[2]),float(data[3])] # this will always contain 3 values            
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


def draw_figure(vertices, faces):
    global canvas
    # loop through the faces and connect edges
    for face in faces:        
        #print(face, vertices[face[0]-1].coord,vertices[face[1]-1].coord,vertices[face[2]-1].coord)       
        node0 = np.array(vertices[face[0]-1]) * 100.0 #x0,y0,z0
        node1 = np.array(vertices[face[1]-1]) * 100.0 #x1,y1,z1
        node2 = np.array(vertices[face[2]-1]) * 100.0 #x2,y2,z2
        #print("---")
        #print(node0, node1, node2)
        canvas.create_line(node0[0] + x_offset, node0[1] + y_offset, node1[0] + x_offset, node1[1] + y_offset) # node0-1
        canvas.create_line(node1[0] + x_offset, node1[1] + y_offset, node2[0] + x_offset, node2[1] + y_offset) #node 1-2
        canvas.create_line(node0[0] + x_offset, node0[1] + y_offset, node2[0] + x_offset, node2[1] + y_offset) #node0-2

        #print(np.array(node0)*100,np.array(node1)*100,np.array(node2)*100 )



def rotate_x(theta):
    return [
        [1, 0, 0],
        [0, math.cos(theta), -math.sin(theta)],
        [0, math.sin(theta), math.cos(theta)],
    ]

def rotate_y(theta):
    return [
        [math.cos(theta), 0, math.sin(theta)],
        [0, 1, 0],
        [-math.sin(theta), 0, math.cos(theta)],
    ]

def rotate_z(theta):
    return [
        [math.cos(theta), -math.sin(theta), 0],
        [math.sin(theta), math.cos(theta), 0],
        [0, 0, 1],
    ]

def animate():
    global vertices, edges
    rotation_matrix = np.dot(rotate_x(0.4), np.dot(rotate_y(0.2), rotate_z(0.1)))
    vertices = [np.dot(rotation_matrix, vertex) for vertex in vertices]

    canvas.delete('all')
    draw_figure(vertices, edges)

    root.after(100, animate)

        
# main ------------------------------------------------------------
def main():
    global canvas, vertices, edges, root

    filePath = "C:\\Users\\christian.saiz\\Documents\\0_NOAA\\Coding_courses\\3DPoly\\Ex\\object.txt"
    
    data = get_lines(filePath)
    vertices = get_vertices(data)
    edges = get_faces(data)
    
    # create window and canvas
    root = Tk()
    canvas = Canvas(root, width=640, height=480, background = 'white')
    canvas.pack()

    animate()
    #draw_figure(a,b)



##    print("-a-")
##    for item in a:
##        print(item.coord)
##    print("-b-")
##    print(b)
##
##    print("---")
##    print(a[0].coord[0])

    #vertices = [vertix(1,[1,2,3]), vertix(2,[10,20,30])]
    

    #myobj = polyObject(6,8,vertices, edges)
    #myobj.vnum = 6
    #myobj.enum = 8

    #a = vertix()
    #b = vertix()
    #a.idx = 0
    #a.coord = [1,2,3]
    #b.idx = 1
    #b.coord = [10,20,30]
    
    #myobj.vertices = [vertix(1,[1,2,3]), vertix(2,[10,20,30])]
    #myobj.edges = [5,6,4,7,8,9]
    
    #print(myobj.vnum, myobj.vertices[1].idv)

    return 0
# main ------------------------------------------------------------



if __name__ == "__main__":
    main()
