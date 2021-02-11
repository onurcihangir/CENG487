# Note:
# -----
# This Uses PyOpenGL and PyOpenGL_accelerate packages.  It also uses GLUT for UI.
# To get proper GLUT support on linux don't forget to install python-opengl package using apt
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
import os
import numpy

from shape import Shape
from camera import Camera
from objParser import ObjParser
from catmullclark import CatmullClark

# Some api in the chain is translating the keystrokes to this octal string
# so instead of saying: ESCAPE = 27, we use the following.
ESCAPE = '\053'

# Number of the glut window.
window = 0
oldX = 320
oldY = 240


# A general OpenGL initialization function.  Sets all of the initial parameters.
def InitGL(Width, Height):  # We call this right after our OpenGL window is created.
    glClearColor(0.0, 0.0, 0.0, 0.0)  # This Will Clear The Background Color To Black
    glClearDepth(1.0)  # Enables Clearing Of The Depth Buffer
    glDepthFunc(GL_LESS)  # The Type Of Depth Test To Do
    glEnable(GL_DEPTH_TEST)  # Enables Depth Testing
    glShadeModel(GL_SMOOTH)  # Enables Smooth Color Shading
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()  # Reset The Projection Matrix
    # Calculate The Aspect Ratio Of The Window
    gluPerspective(45.0, float(Width) / float(Height), 0.1, 100.0)

    glMatrixMode(GL_MODELVIEW)


# The function called when our window is resized (which shouldn't happen if you enable fullscreen, below)
def ReSizeGLScene(Width, Height):
    if Height == 0:  # Prevent A Divide By Zero If The Window Is Too Small
        Height = 1

    glViewport(0, 0, Width, Height)  # Reset The Current Viewport And Perspective Transformation
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width) / float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)


# The main drawing function.
def DrawGLScene():
    # Clear The Screen And The Depth Buffer
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()  # Reset The View

    glLoadMatrixf(camera.lookAt)

    shape.draw_lines()
    shape.draw()

    glWindowPos2i(10,10)
    text = "Subdivision Level : " + str(shape._subdivision_level)
    for ch in text:
        glutBitmapCharacter(GLUT_BITMAP_8_BY_13, ord(ch))

    #  since this is double buffered, swap the buffers to display what just got drawn.
    glutSwapBuffers()


# The function called whenever a key is pressed. Note the use of Python tuples to pass in: (key, x, y)
def keyPressed(*args):
    # If escape is pressed, kill everything.
    # Convert bytes shape to string
    key = args[0].decode("utf-8")
    # Allow to quit by pressing 'Esc' or 'q'
    if key == chr(27):
        os._exit(1)
    elif key == '+':
        shape._subdivider.add_subdivision()
    elif key == '-':
        shape._subdivider.remove_subdivision()
    elif key == 'f':
        camera.reset()


def mousePressed(button, state, x, y):
    global left_mouse
    global right_mouse
    global oldX
    global oldY
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and glutGetModifiers() == GLUT_ACTIVE_ALT:
        left_mouse = True
        oldX = x
        oldY = y
    else:
        left_mouse = False
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN and glutGetModifiers() == GLUT_ACTIVE_ALT:
        right_mouse = True
        oldX = x
        oldY = y
    else:
        right_mouse = False

def mouseDragged(x, y):
    oldy = oldY
    oldx = oldX
    if left_mouse:
        yloc = (oldy - y)*0.001
        xloc = (x - oldx)*0.001
        oldx = x
        oldy = y
        camera.rotate(-xloc, yloc)
    if right_mouse:
        yloc = (oldy - y)*0.001
        oldy = y
        camera.zoom(yloc)

def main():
    global window
    global shape
    global camera

    camera = Camera()
    vertices, faces = ObjParser.parse()
    shape = Shape(vertices, faces)
    shape._subdivider = CatmullClark(shape)

    glutInit(sys.argv)

    # Select type of Display mode:
    #  Double buffer
    #  RGBA color
    # Alpha components supported
    # Depth buffer
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)

    # get a 640 x 480 window
    glutInitWindowSize(640, 480)

    # the window starts at the upper left corner of the screen
    glutInitWindowPosition(0, 0)
    window = glutCreateWindow("CENG487 Template")

    # Display Func
    glutDisplayFunc(DrawGLScene)

    # When we are doing nothing, redraw the scene.
    glutIdleFunc(DrawGLScene)

    # Register the function called when our window is resized.
    glutReshapeFunc(ReSizeGLScene)

    # Register the function called when the keyboard is pressed.
    glutKeyboardFunc(keyPressed)

    glutMouseFunc(mousePressed)

    glutMotionFunc(mouseDragged)


    # Initialize our window.
    InitGL(640, 480)

    # Start Event Processing Engine
    glutMainLoop()


# Print message to console, and kick off the main to get it rolling.
print("ESC key -> quit\n" +
      "alt/right click -> zoom\n" +
      "alt/left click -> rotate\n" +
      "+ -> increase subdivision\n" +
      "- -> decrease subdivision\n" +
      "f -> reset view")
main()
