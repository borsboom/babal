import math


def _normalize(v):
    d = math.sqrt(v[0]*v[0]+v[1]*v[1]+v[2]*v[2])
    v[0] /= d
    v[1] /= d
    v[2] /= d


def _drawtriangle(v1, v2, v3):
    gl.glNormal3fv(v1)
    gl.glVertex3fv(v1)
    gl.glNormal3fv(v2)
    gl.glVertex3fv(v2)
    gl.glNormal3fv(v3)
    gl.glVertex3fv(v3)


def _subdivide(v1, v2, v3):
    v12 = [0, 0, 0]
    v23 = [0, 0, 0]
    v31 = [0, 0, 0]
    for i in range(0, 3):
        v12[i] = v1[i] + v2[i]; 
        v23[i] = v2[i] + v3[i];     
        v31[i] = v3[i] + v1[i];    
    _normalize(v12)
    _normalize(v23)
    _normalize(v31)
    _drawtriangle(v1, v12, v31)
    _drawtriangle(v2, v23, v12)
    _drawtriangle(v3, v31, v23)
    _drawtriangle(v12, v23, v31)


def iif(b, t, f):
    if b:
        return t
    else:
        return f
    

def _draw_ball_triangles():
    x = 0.525731112119133606 
    z = 0.850650808352039932

    vdata = [[-x, 0.0, z], [x, 0.0, z], [-x, 0.0, -z], [x, 0.0, -z],
             [0.0, z, x], [0.0, z, -x], [0.0, -z, x], [0.0, -z, -x],
             [z, x, 0.0], [-z, x, 0.0], [z, -x, 0.0], [-z, -x, 0.0]]
    tindices = [[0,4,1], [0,9,4], [9,5,4], [4,5,8], [4,8,1],
                [8,10,1], [8,3,10], [5,3,8], [5,2,3], [2,7,3],
                [7,10,3], [7,6,10], [7,11,6], [11,0,6], [0,1,6],
                [6,1,10], [9,0,11], [9,11,2], [9,2,5], [7,2,11]]

    gl.glBegin(gl.GL_TRIANGLES)
    try:
        for i in range(0, len(tindices)):
            gl.glColor3f(iif(i&1, 1.0, 0.0),
                     iif(i&2, 1.0, 0.0),
                     iif(i&4, 1.0, 0.0))
            _subdivide(vdata[tindices[i][2]],
                      vdata[tindices[i][1]],
                      vdata[tindices[i][0]])
    finally:
        gl.glEnd()


SLICES = 10
STACKS = 12
STACK_COLOURS = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]


def _parm_vertex(a, b):
    gl.glVertex3f(math.cos(a) * math.sin(b),
                  math.sin(a) * math.sin(b),
                  math.cos(b))    


def _draw_ball_parametric():
    gl.glRotatef(90.0, 0.0, 1.0, 0.0)
    gl.glBegin(gl.GL_QUADS)
    try:
        for slice in range(0, SLICES):
            b0 = slice * math.pi / float(SLICES)
            b1 = (slice+1) * math.pi / float(SLICES)
            for stack in range(0, STACKS):
                gl.glColor3fv(STACK_COLOURS[stack/4])
                a0 = stack * 2 * math.pi / float(STACKS)
                a1 = (stack+1) * 2 * math.pi / float(STACKS)
                _parm_vertex(a0, b0)
                _parm_vertex(a0, b1)
                _parm_vertex(a1, b1)
                _parm_vertex(a1, b0)
    finally:
        gl.glEnd()


def init(gl_):
    global gl
    global _ball_list
    gl = gl_
    _ball_list = gl.glGenLists(1)
    gl.glNewList(_ball_list, gl.GL_COMPILE)
    try:
        #_draw_ball_triangles()
        _draw_ball_parametric()
    finally:
        gl.glEndList()

    
def draw():
    global _ball_list
    gl.glCallList(_ball_list)

