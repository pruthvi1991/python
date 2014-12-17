import math
ami_radius = 2.5
theta = math.pi
i = theta/2
j = 0 ; k = 0 ; l = 0 ; m = 0 # dummy indices

rotor_cells = [10, 1, 10]    # Number of cells in rotor

rotor_grading = [1, 1, 1]    # Mesh grading of rotor

X = [0]; Y = [0]; Z = [0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1] # Lists for x,y,z coordinates of mesh

v1 = []; v2 = []; v3 = []; v4 = []; v5 = []; v6 = []; v7 = []; v8 = []; # Lists to hold block vertices

edge_x = []; edge_y = [];    # Lists to hold edge values

rotor_face1 = []; rotor_face2 = []; rotor_face3 = []; rotor_face4 = []; # Lists to hold rotor ami face vertices

front1 = []; front2 = []; front3 = []; front4 = []; front5 = []; front6 = []; front7 = []; front8 = [] # Lists to hold front face vertices

back1 = []; back2 = []; back3 = []; back4 = []; back5 = []; back6 = []; back7 = []; back8 = []; # Lists to hold back face vertices

def vertex(x,y,z): #Function to print vertexes in OpenFoam format :: (x y z)
    v = '(' + str(x) + ' ' + str(y) + ' ' + str(z) + ')'
    return v

def face(x,y,z,p): #Function to print vertexes in OpenFoam format :: (x y z p)
    f = '(' + str(x) + ' ' + str(y) + ' ' + str(z) + ' ' + str(p) + ')'
    return f

def block(x,y,z,p,q,r,s,t): #Function to print block in OpenFoam format :: hex (1 2 3 4 5 6 7 8)
    b = 'hex' + ' ' + '(' + str(x) + ' ' + str(y) + ' ' + str(z) + ' ' + str(p) + ' ' + str(q)\
    + ' ' + str(r) + ' ' + str(s) + ' ' + str(t) + ')'
    return b

def edges(): # Function to print edges in OpenFoam format :: edge <vertex1> <vertex2> (x y z)
    print 'edges'
    print '('
    for j in range(1,6):
        print '    arc ' + str(j) + ' ' + str(j+1) + ' ' + '(' + str(edge_x[j]) + ' ' +\
        str(edge_y[j]) + ' ' + str(Z[j])+')' + '     //e' + str(j)
    print '    arc ' + str(6) + ' ' + str(1) + ' ' + '(' + str(edge_x[5]) + ' ' +\
        str(edge_y[5]) + ' ' + str(Z[5])+')' + '     //e' + str(6)
    for k in range(0,5):
        print '    arc ' + str(k+8) + ' ' + str(k+9) + ' ' + '(' + str(edge_x[k]) + ' ' +\
        str(edge_y[k]) + ' ' + str(-Z[k])+')' + '     //e' + str(k+7)
    print '    arc ' + str(13) + ' ' + str(8) + ' ' + '(' + str(edge_x[5]) + ' ' +\
        str(edge_y[5]) + ' ' + str(-Z[5])+')' + '     //e' + str(12)
    print ');'
        #return e

def vertices(): #Function to print vertices in OpenFoam format :: vertices (<  >);
    print 'vertices'
    print '('
    for j in range(0,7):
        print '    ' + vertex(X[j], Y[j], Z[j]) + '      //v' +str(j)+ ' sliding interface_top'
    for j in range(0,7):
        print '    ' + vertex(X[j], Y[j], -Z[j]) + '     //v' +str(j+6) + ' sliding interface_bottom'
    print ');'
    
def blocks(): #Function to print blocks in OpenFoam format :: blocks (<  >);
    print 'blocks'
    print '('
    for j in range(0,5):
        print '    ' + block(v7[j], v8[j], v5[j], v6[j], v3[j], v4[j], v1[j], v2[j])\
        + ' (' + str(rotor_cells[0]) + ' ' + str(rotor_cells[1]) + ' ' + str(rotor_cells[2]) + ')' \
        + ' simpleGrading ' + '(' + ' ' + str(rotor_grading[0]) + ' ' + str(rotor_grading[1]) \
        + ' ' + str( rotor_grading[2]) + ')' + ' //' + 'b' + str(j+1) + ' ~rotor'
    print '    hex (' + str(0) + ' ' + str(0) + ' ' + str(7) + ' ' + str(7) + ' ' + str(1)\
    + ' ' + str(6) + ' ' + str(13) + ' ' + str(8) + ')' + ' (' + str(rotor_cells[0]) + ' ' \
    + str(rotor_cells[1]) + ' ' + str(rotor_cells[2]) + ')' + ' simpleGrading ' + '(' \
    + str(rotor_grading[0]) + ' ' + str(rotor_grading[1]) + ' ' + str(rotor_grading[2]) \
    + ')' + '  ' '//b12' + ' ~rotor'
    print ');'

def boundaries():
    print 'boundary\n('
    ami()
    
def ami():
    print '\n    couple1\n    {\n        type     patch;\n'  
    print '        faces\n        ('
    for j in range(0,5):
        print '            ' + face(rotor_face1[j], rotor_face2[j], rotor_face3[j], rotor_face4[j]) +\
        ' ' + '// rotor_face' + str(j+1) 
    print '            ' + '(' + str(8) + ' ' + str(13) + ' ' + str(6) + ' ' + str(1) + ')' + ' ' +\
    '// rotor_face' + str(6)
    print '        );\n    }'
        
def frontandback():
    print '    frontandback\n    {\n        type empty;\n        faces\n        ('
    for j in range(0,5):
        print '            ' + face(front1[j], front4[j], front2[j], front3[j]) + ' ' \
        + '    // rotor_front_face' + str(j)
    print '            ' + '(' + str(0) + ' ' + str(0) + ' ' + str(6) + ' ' + str(1) + ')' \
    + ' ' + '    // rotor_front_face' + str(21)
    for j in range(0,5):
        print '            ' + face(back1[j], back4[j], back2[j], back3[j]) + ' ' \
        + '    // rotor_back_face' + str(j + 5)
    print '            ' + '(' + str(7) + ' ' + str(7) + ' ' + str(13) + ' ' + str(8) + ')' \
    + ' ' + '    // rotor_back_face' + str(11)
    print '        );\n    }\n);'
   
while j<6: # Looping over rotor edge to define vertices position
    X.append(ami_radius*math.cos(i))
    Y.append(ami_radius*math.sin(i))
    #Z.append(0.1)
    edge_x.append(ami_radius*math.cos(i + (theta/6)))
    edge_y.append(ami_radius*math.sin(i + (theta/6)))
    i = i + theta/3
    j = j + 1
    #print vertex(X[j-1], Y[j-1], Z[j-1]) + '  //v' + str(j)

while k<5: # Looping over rotor vertices to define blocks. 
    v5.append(7),        v6.append(7),       v7.append(0)
    v8.append(0),         v1.append(k + 8),   v2.append(k + 9)
    v3.append(k + 2),     v4.append(k + 1)
    k = k + 1
    
    
while l<6: # Looping over rotor edge to define sliding boundary faces.
    rotor_face1.append(l+9),    rotor_face2.append(l+8),    rotor_face3.append(l+1)
    rotor_face4.append(l+2)
    l = l + 1
    
while m<6: # Looping over front and back to define empty boundary condition.
    front1.append(0),     front2.append(m+1),    front3.append(m+2),    front4.append(0)
    back1.append(7),     back2.append(m+8),    back3.append(m+9),    back4.append(7)
    m = m + 1
    
vertices()
print ''
blocks()
print ''
edges()
print ''
boundaries()
print ''
frontandback()
