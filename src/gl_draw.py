import math

import gl_draw_ball


DEG_TO_RAD_FACTOR = 2 * math.pi / 360.0
TILE_Z = 4.0


# draws with front-left corner of map at origin, each tile 1.0 units big
def draw_map():
    start_row = int(game.ball_z) - 1
    end_row = start_row + 20
    if start_row < 0:
        end_row += start_row
        start_row = 0
    if end_row < 0:
        end_row = 0
    rows = game.map[start_row:end_row]
    z = -float(start_row)* TILE_Z
    gl.glColor3f(0.0, 0.0, 0.0)
    gl.glBegin(gl.GL_QUADS)
    try:
        for row in rows:
            x = 0.0
            for col in row:
                if col:
                    gl.glVertex3f(x, 0.0, z)
                    gl.glVertex3f(x+1.0, 0.0, z)
                    gl.glVertex3f(x+1.0, 0.0, z-TILE_Z)
                    gl.glVertex3f(x, 0.0, z-TILE_Z)
                x += 1.0
            z -= TILE_Z
    finally:
        gl.glEnd()


def draw():
    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
    
    gl.glLoadIdentity()
    gl.glTranslatef(0.0 - game.ball_x, -0.0, -4.0 + game.ball_z * TILE_Z)

    gl.glPushMatrix()
    try:
        gl.glTranslatef(-(math.floor((game.map_width-1) / 2.0) + 0.5),
                     -2.0,
                     0.5 * TILE_Z)
        draw_map()
    finally:
        gl.glPopMatrix()

    gl.glPushMatrix()
    try:
        gl.glTranslatef(game.ball_x,
                        -2.0 + game.ball_radius + game.ball_y,
                        -game.ball_z * TILE_Z)
        gl.glScalef(game.ball_radius, game.ball_radius, game.ball_radius)
        gl.glRotatef(-game.ball_x_rotate,
                     1.0,
                     0.0,
                     0.0)
        gl_draw_ball.draw()
    finally:
        gl.glPopMatrix()


def reshape(w, h):
    if h == 0:
        h = 1
    gl.glViewport(0, 0, w, h)
    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glLoadIdentity()
    gl.glScalef(2.3, 2.3, 1.0)
    gl.glTranslatef(0.0, 0.5, 0.0)
    glu.gluPerspective(60.0, float(w)/float(h), 1.0, 100.0)
    gl.glMatrixMode(gl.GL_MODELVIEW)    


def init(gl_, glu_, game_):
    global gl, glu, game
    gl = gl_
    glu = glu_
    game = game_
    gl.glClearColor(1.0, 1.0, 1.0, 0.0) # defaults to black
    gl.glClearDepth(1.0) # defaults to 1
    gl.glDepthFunc(gl.GL_LESS) # defaults to GL_LESS
    gl.glEnable(gl.GL_DEPTH_TEST) # defaults to depth test disabled
    gl.glShadeModel(gl.GL_SMOOTH) # default is GL_SMOOTH

    gl.glEnable(gl.GL_CULL_FACE) # default is culling disabled
    #gl.glFrontFace(gl.GL_CCW) # default is GL_CCW
    #gl.glCullFace(gl.GL_BACK) # default is GL_BACK

    #mat_specular = [ 1.0, 1.0, 1.0, 1.0 ]
    #mat_shininess = [ 50.0 ]
    #light_position = [ 1.0, 1.0, 1.0, 0.0 ]
    #gl.glMaterialfv(gl.GL_FRONT, gl.GL_SPECULAR, mat_specular)
    #gl.glMaterialfv(gl.GL_FRONT, gl.GL_SHININESS, mat_shininess)
    #gl.glLightfv(gl.GL_LIGHT0, gl.GL_POSITION, light_position)
    #gl.glEnable(gl.GL_LIGHTING)
    #gl.glEnable(gl.GL_LIGHT0)

    gl_draw_ball.init(gl)
