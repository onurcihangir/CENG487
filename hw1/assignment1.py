# Note:
# -----
# This Uses PyOpenGL and PyOpenGL_accelerate packages.  It also uses GLUT for UI.
# To get proper GLUT support on linux don't forget to install python-opengl package using apt
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
from vec3d import Vec3d
from mat3d import Mat3d
from Object import Object
import time

# Some api in the chain is translating the keystrokes to this octal string
# so instead of saying: ESCAPE = 27, we use the following.
ESCAPE = '\033'

# Number of the glut window.
window = 0


# A general OpenGL initialization function.  Sets all of the initial parameters.
def InitGL(Width, Height):  # We call this right after our OpenGL window is created.
    glClearColor(0.0, 0.0, 0.0, 0.0)  # This Will Clear The Background Color To Black
    glClearDepth(1.0)  # Enables Clearing Of The Depth Buffer
    glDepthFunc(GL_LESS)  # The Type Of Depth Test To Do
    glEnable(GL_DEPTH_TEST)  # Enables Depth Testing
    glShadeModel(GL_SMOOTH)  # Enables Smooth Color Shading

    # Add vertices to the object
    triangle.add_vertex(Vec3d(0.0, 1.0, 0.0, 1.0))
    triangle.add_vertex(Vec3d(1.0, -1.0, 0.0, 1.0))
    triangle.add_vertex(Vec3d(-1.0, -1.0, 0.0, 1.0))

    square.add_vertex(Vec3d(-1.0, 1.0, 0.0, 1.0))
    square.add_vertex(Vec3d(1.0, 1.0, 0.0, 1.0))
    square.add_vertex(Vec3d(1.0, -1.0, 0.0, 1.0))
    square.add_vertex(Vec3d(-1.0, -1.0, 0.0, 1.0))

    # Add transformation matrices to the object
    first_matrix = Mat3d()
    second_matrix = Mat3d()
    third_matrix = Mat3d()
    square.add_transformation(first_matrix.define_translation_matrix(-1, -1, 0)) # To rotate around one vertex, we perform transformation as TRT^-1
    square.add_transformation(second_matrix.define_rotation_matrix(5, "z"))
    square.add_transformation(third_matrix.define_translation_matrix(1, 1, 0))

    fourth_matrix = Mat3d()
    fifth_matrix = Mat3d()
    sixth_matrix = Mat3d()
    triangle.add_transformation(fourth_matrix.define_translation_matrix(1, 1, 0))
    triangle.add_transformation(fifth_matrix.define_rotation_matrix(5, "z"))
    triangle.add_transformation(sixth_matrix.define_translation_matrix(-1, -1, 0))

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

    # Move Left 1.5 units and into the screen 6.0 units.
    glTranslatef(-1.5, 0.0, -6.0)

    # Since we have smooth color mode on, this will be great for the Phish Heads :-).
    # Draw a triangle
    glBegin(GL_POLYGON)  # Start drawing a polygon
    glColor3f(1.0, 0.0, 0.0)  # Red
    glVertex3f(triangle.vertices[0].get_x(), triangle.vertices[0].get_y(), triangle.vertices[0].get_z())  # Top
    glColor3f(0.0, 1.0, 0.0)  # Green
    glVertex3f(triangle.vertices[1].get_x(), triangle.vertices[1].get_y(), triangle.vertices[1].get_z())  # Bottom Right
    glColor3f(0.0, 0.0, 1.0)  # Blue
    glVertex3f(triangle.vertices[2].get_x(), triangle.vertices[2].get_y(), triangle.vertices[2].get_z())  # Bottom Left
    glEnd()  # We are done with the polygon

    # Move Right 3.0 units.
    glTranslatef(3.0, 0.0, 0.0)

    # Draw a square (quadrilateral)
    glColor3f(0.3, 0.5, 1.0)  # Bluish shade
    glBegin(GL_QUADS)  # Start drawing a 4 sided polygon
    glVertex3f(square.vertices[0].get_x(), square.vertices[0].get_y(),
               square.vertices[0].get_z())  # Top Left
    glVertex3f(square.vertices[1].get_x(), square.vertices[1].get_y(),
               square.vertices[1].get_z())  # Top Right
    glVertex3f(square.vertices[2].get_x(), square.vertices[2].get_y(),
               square.vertices[2].get_z())  # Bottom Right
    glVertex3f(square.vertices[3].get_x(), square.vertices[3].get_y(),
               square.vertices[3].get_z())  # Bottom Left
    glEnd()  # We are done with the polygon

    # Perform transformation here
    triangle.transform_object(triangle.get_final_transformation_matrix())
    square.transform_object(square.get_final_transformation_matrix())

    #  since this is double buffered, swap the buffers to display what just got drawn.
    glutSwapBuffers()

    time.sleep(0.05)


# The function called whenever a key is pressed. Note the use of Python tuples to pass in: (key, x, y)
def keyPressed(*args):
    # If escape is pressed, kill everything.
    if args[0] == ESCAPE:
        sys.exit()


def main():
    global window
    global triangle
    global square

    triangle = Object()
    square = Object()

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

    # Initialize our window.
    InitGL(640, 480)

    # Start Event Processing Engine
    glutMainLoop()


# Print message to console, and kick off the main to get it rolling.
print("Hit ESC key to quit.")
main()
