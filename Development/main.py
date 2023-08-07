import time
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from entities.Spaceship import Spaceship

# Constants
SPACESHIP_OBJECT = "./assets/ship.obj"
spaceship = Spaceship(SPACESHIP_OBJECT)


# Initialize timer variables
PERFORMANCE_COUNTER = time.perf_counter()
NEW_ENEMY_TIME = 0

def init():
    glClearColor(0.0, 0.0, 0.0, 0.0)  # set background color to black
    glEnable(GL_DEPTH_TEST)  # enables depth testing

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(1920, 1080)
    glutInitWindowPosition(100, 100)
    glutCreateWindow("Space Invaders")
    init()

    glutDisplayFunc(display)
    glutSpecialFunc(keyboard)
    glutSpecialUpFunc(keyboardUP)
    glutReshapeFunc(resize)
    glutTimerFunc(50, animation, 1)  # call animation() after 50 milliseconds

    glutMainLoop()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)

    spaceship.calculateVelocity()
    spaceship.updateMovement()
    spaceship.draw()

    glutSwapBuffers()

def keyboard(key, x, y):
    if key == GLUT_KEY_LEFT:
        spaceship.left = 1
    elif key == GLUT_KEY_RIGHT:
        spaceship.right = 1

def keyboardUP(key, x, y):
    if key == GLUT_KEY_LEFT:
        spaceship.left = 0
    elif key == GLUT_KEY_RIGHT:
        spaceship.right = 0

def resize(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(40, 16 / 9, 1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 5, 10, 0, 2, 0, 0, 1, 0)

def animation(value):
    global PERFORMANCE_COUNTER, NEW_ENEMY_TIME

    if time.perf_counter() - PERFORMANCE_COUNTER > 0.01:
        PERFORMANCE_COUNTER = time.perf_counter()
        glutPostRedisplay()  # redraw the scene

    glutTimerFunc(20, animation, 1)  # call animation() after 50 milliseconds

if __name__ == "__main__":
    main()
