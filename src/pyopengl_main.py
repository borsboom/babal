#!/usr/bin/env python
import sys

from OpenGL import GL
from OpenGL import GLU
from OpenGL import GLUT
from Game import Game
import gl_draw


def display_cb():
    GLUT.glutSetWindow(window)
    game.update()
    gl_draw.draw()
    GLUT.glutSwapBuffers()


def idle_cb():
    GLUT.glutSetWindow(window)
    GLUT.glutForceJoystickFunc()
    GLUT.glutPostRedisplay()


def visibility_cb(vis):
    # stop drawing if window not visible
    if vis:
        game.reset_timer()
        GLUT.glutIdleFunc(idle_cb)
    else:
        GLUT.glutIdleFunc(None)


def reshape_cb(w, h):
    gl_draw.reshape(w, h)
    

def keyboard_cb(key, x, y):
    if key == '\033' or key == 'q' or key == 'Q':
        sys.exit()
    elif key == ' ':
        game.begin_jump()
    elif key == 'p' or key == 'P':
        game.toggle_pause()


def keyboard_up_cb(key, x, y):
    if key == ' ':
        game.end_jump()


def special_cb(key, x, y):
    if key == GLUT.GLUT_KEY_LEFT:
        game.begin_left()
    elif key == GLUT.GLUT_KEY_RIGHT:
        game.begin_right()
    elif key == GLUT.GLUT_KEY_UP:
        game.begin_accel()
    elif key == GLUT.GLUT_KEY_DOWN:
        game.begin_decel()
        

def special_up_cb(key, x, y):
    if key == GLUT.GLUT_KEY_LEFT:
        game.end_left()
    elif key == GLUT.GLUT_KEY_RIGHT:
        game.end_right()
    elif key == GLUT.GLUT_KEY_UP:
        game.end_accel();
    elif key == GLUT.GLUT_KEY_DOWN:
        game.end_decel();


JOY_THRESH = 500
old_joy_button_mask = 0
old_joy_x = 0
old_joy_y = 0


def joystick_cb(button_mask, x, y, z):
    global old_joy_button_mask, old_joy_x, old_joy_y
    
    if button_mask and not old_joy_button_mask:
        game.begin_jump()
    elif old_joy_button_mask and not button_mask:
        game.end_jump()
    old_joy_button_mask = button_mask

    if old_joy_x < -JOY_THRESH and x >= -JOY_THRESH:
        game.end_left()
    elif old_joy_x > JOY_THRESH and x <= JOY_THRESH:
        game.end_right()
    if x < -JOY_THRESH and old_joy_x >= -JOY_THRESH:
        game.begin_left()
    elif x > JOY_THRESH and old_joy_x <= JOY_THRESH:
        game.begin_right()
    old_joy_x = x

    if old_joy_y < -JOY_THRESH and y >= -JOY_THRESH:
        game.end_accel()
    elif old_joy_y > JOY_THRESH and y <= JOY_THRESH:
        game.end_decel()
    if y < -JOY_THRESH and old_joy_y >= -JOY_THRESH:
        game.begin_accel()
    if y > JOY_THRESH and old_joy_y <= JOY_THRESH:
        game.begin_decel()
    old_joy_y = y


def main():
    GLUT.glutInit(sys.argv)
    GLUT.glutInitDisplayMode(GLUT.GLUT_RGBA | GLUT.GLUT_DOUBLE | GLUT.GLUT_DEPTH)
    GLUT.glutInitWindowSize(320, 240)
    global window
    window = GLUT.glutCreateWindow("Babal")

    GLUT.glutDisplayFunc(display_cb)
    GLUT.glutVisibilityFunc(visibility_cb)
    GLUT.glutReshapeFunc(reshape_cb)

    GLUT.glutIgnoreKeyRepeat(1)
    GLUT.glutKeyboardFunc(keyboard_cb)
    GLUT.glutKeyboardUpFunc(keyboard_up_cb)
    GLUT.glutSpecialFunc(special_cb)
    GLUT.glutSpecialUpFunc(special_up_cb)
    GLUT.glutJoystickFunc(joystick_cb, 0)

    map_file = None
    if len(sys.argv) > 1:
        map_file = open(sys.argv[1])

    global game
    game = Game(map_file)
    gl_draw.init(GL, GLU, game)

    # reshape_cb gets called when window is made visible

    GLUT.glutMainLoop()
