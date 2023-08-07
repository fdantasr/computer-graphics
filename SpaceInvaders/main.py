
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.arrays import vbo
from OpenGL.GL import shaders

from PIL import Image

from entities.Enemy import Enemy
from entities.Spaceship import Spaceship

import time
import random

from entities.Particles import ParticlesSystem

ENEMY_OBJECT = "./assets/asteroid/asteroid.obj"
SPACESHIP_OBJECT = "./assets/ship.obj"

INITAL_ENEMY_TIME = 0  # time when a new enemy is created

PERFORMANCE_COUNTER = (
    time.perf_counter()
)  # time.perf_counter() returns the value (in fractional seconds) of a performance counter, i.e. a clock with the highest available resolution to measure a short duration

NEW_ENEMY_TIME = INITAL_ENEMY_TIME  # time when a new enemy is created

enemies = [
    Enemy(ENEMY_OBJECT, [0.0, 1.0, -15])
]  # Create an enemy object at position [x,y,z]
spaceship = Spaceship(SPACESHIP_OBJECT)  # Create a spaceship object
particlesSystem = []

def init():
    glClearColor(0.0, 0.0, 0.0, 0.0)  # set background color to black and opaque
    glShadeModel(GL_SMOOTH)  # set shading to smooth
    glClearColor(0.0, 0.0, 0.0, 0.0)  # set background color to black and opaque
    glClearDepth(1.0)  # set background depth to farthest
    glEnable(GL_DEPTH_TEST)  # enables depth testing
    glDepthFunc(GL_LEQUAL)  # the type of depth test to do
    glHint(
        GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST
    )  # really nice perspective calculations

    glEnable(GL_LIGHT0)  # enables lighting
    glEnable(
        GL_COLOR_MATERIAL
    )  # enables opengl to use glColor3f to define material color
    glShadeModel(GL_SMOOTH)  # set shading to smooth
    glLightModeli(GL_LIGHT_MODEL_TWO_SIDE, GL_FALSE)  # enable two-sided lighting
    glDepthFunc(GL_LEQUAL)  # the type of depth test to do
    glEnable(GL_DEPTH_TEST)  # enables depth testing
    glEnable(GL_LIGHTING)  # enables lighting
    glEnable(GL_LIGHT0)  # enables light0

    apply_shader()
    apply_texture()

def main():
    glutInit()  # initialize glut
    glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)  # set display mode
    glutInitWindowSize(1920, 1080)  # set window size
    glutInitWindowPosition(100, 100)  # set window position
    glutCreateWindow("Space Invaders Alpha˜0.1")  # create window with title
    init()  # initialize

    glutDisplayFunc(display)  # set display callback function
    glutSpecialFunc(keyboard)  # set keyboard callback function
    glutSpecialUpFunc(keyboardUP)
    glutReshapeFunc(resize)  # set resize callback function
    glutTimerFunc(40, animation, 1)  # call animation() after 10 milliseconds
    glutMainLoop()  # get into an infinite loop

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # clear the screen
    glMatrixMode(GL_MODELVIEW)  # indicate we are specifying camera transformations
    spaceship.calculateVelocity()
    spaceship.updateMovement()
    
    for ammo in spaceship.ammo:
      ammo.draw()

    spaceship.draw()  # draw spaceship

    for enemy in enemies:  # draw enemies
        enemy.draw()
        apply_light()
        vbo_buffer_bind(enemy)
        glUseProgram(0)
        glPopMatrix()
        glPopMatrix()
    
    glPushMatrix()
    for i, particles in enumerate(particlesSystem):
        particles.draw()
        if (particles.ttl < 0):
            del particlesSystem[i]
    glPopMatrix()

    glutSwapBuffers()  # swap buffers

######################################################### utils #################################################################

def apply_light():
    glUseProgram(asteroid_shader)
    glUniform4f( LIGTH_LOCATIONS['Global_ambient'], 0.1, 0.1, 0.1, 1.0 )
    glUniform4f( LIGTH_LOCATIONS['Light_ambient'], 0.1, 0.18725, 0.1745, 1.0 )
    glUniform4f( LIGTH_LOCATIONS['Light_diffuse'], 0.396, 0.74151, 0.69102, 1.0 )
    glUniform3f( LIGTH_LOCATIONS['Light_location'], 0.0, 5.0, 0.0 )
    glUniform4f( LIGTH_LOCATIONS['Light_specular'], 0.297254, 0.30829, 0.306678, 1.0 )
    
    glUniform4f( LIGTH_LOCATIONS['Material_ambient'], .1,.1,.1, 1.0 )
    glUniform4f( LIGTH_LOCATIONS['Material_diffuse'], .4,.4,0.9, 1 )
    glUniform4f( LIGTH_LOCATIONS['Material_specular'], 0.7,0.7,0.7, 1 )
    glUniform1f( LIGTH_LOCATIONS['Material_shininess'], 0.4*128.0 )

def vbo_buffer_bind(obj):
    vertices = obj.getVertices('None')
    VBO = vbo.VBO(vertices)
  
    VBO.bind()
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)  
    glEnableClientState(GL_TEXTURE_COORD_ARRAY)
    glVertexPointer(3, GL_FLOAT, 32, VBO+20)
    glNormalPointer(GL_FLOAT, 32, VBO+8)
    glTexCoordPointer(2, GL_FLOAT, 32, VBO)
    
    glUniform4f( LIGTH_LOCATIONS['Material_diffuse'], 0.1,0.1,0.1, 1 )  
    glDrawArrays(GL_TRIANGLES, 0, vertices.shape[0])
    VBO.unbind()

def keyboard(key, x, y):
    if key == GLUT_KEY_LEFT:  # if left arrow key is pressed
        spaceship.left = 1  # move spaceship left
    elif key == GLUT_KEY_RIGHT:  # if right arrow key is pressed
        spaceship.right = 1  # move spaceship right
    elif (key == GLUT_KEY_F1):
        spaceship.fireAmmo()

def keyboardUP(key, x, y):
    if key == GLUT_KEY_LEFT:  
        spaceship.left = 0  
    elif key == GLUT_KEY_RIGHT:  
        spaceship.right = 0  
    

def hitEnemy(ammo, enemy):
    x = enemy.position[0]
    return ammo.position[2] <= enemy.position[2] and x-2.3 <= ammo.position[0] <= x + 2.3


def checkFiredAmmo():
  usedAmmo = {}
  hitEnemies = {}
  countAmmo = len(spaceship.ammo) - 1

  for currentAmmo in range(countAmmo, -1, -1):
      totalEnemies = len(enemies) - 1
      
      if spaceship.ammo[currentAmmo].isOutOfBounds():
          usedAmmo[currentAmmo] = True

      for currentEnemy in range(totalEnemies, -1, -1):
          if hitEnemy(spaceship.ammo[currentAmmo], enemies[currentEnemy]):
              hitEnemies[currentEnemy] = True
              usedAmmo[currentAmmo] = True
              particlesSystem.append(ParticlesSystem(enemies[currentEnemy].position))
              del spaceship.ammo[currentAmmo]
              del enemies[currentEnemy]
              break


def animation(value):
    global PERFORMANCE_COUNTER, NEW_ENEMY_TIME  # global variables
    
    for ammo in spaceship.ammo:
        ammo.move()
    checkFiredAmmo()
    randomCords = [
        random.randint(-12, 12),
        1,
        random.randint(-35, -30),
    ]  # random coordinates for new enemy

    if time.perf_counter() - PERFORMANCE_COUNTER > 0.01:  # if 0.01 seconds have passed
        PERFORMANCE_COUNTER = time.perf_counter()  # update performance_counter

        if time.perf_counter() - NEW_ENEMY_TIME > 2:  # if 1 second has passed
            NEW_ENEMY_TIME = time.perf_counter()  # update NEW_ENEMY_TIME
            enemies.append(Enemy(ENEMY_OBJECT, randomCords))  # create a new enemy

        for enemy in enemies:  # move enemies
            enemy.move(0, 0, +0.1)
        glutPostRedisplay()  # redraw the scene
        glutTimerFunc(50, animation, 1)  # call animation() after 10 milliseconds

def resize(width, height):  # resize the window when the window is resized
    glViewport(0, 0, width, height)  # set the viewport to cover the new window
    glMatrixMode(GL_PROJECTION)  # to operate on the projection matrix
    glLoadIdentity()  # reset matrix
    gluPerspective(
        40, width / height, 1, 100.0
    )  # set the perspective (angle of sight, width, height, , depth)
    glMatrixMode(GL_MODELVIEW)  # to operate on the model-view matrix
    glLoadIdentity()  # reset matrix
    gluLookAt(0, 5, 10, 0, 2, 0, 0, 1, 0)  # set the camera position

def apply_shader():
    VERTEX_SHADER = shaders.compileShader(open('./shaders/asteroid.vert', 'r').read(), GL_VERTEX_SHADER)
    FRAGMENT_SHADER = shaders.compileShader(open('./shaders/asteroid.frag', 'r').read(), GL_FRAGMENT_SHADER)

    global asteroid_shader
    asteroid_shader = glCreateProgram()
    glAttachShader(asteroid_shader, VERTEX_SHADER)
    glAttachShader(asteroid_shader, FRAGMENT_SHADER)
    glLinkProgram(asteroid_shader)

    global LIGTH_LOCATIONS
    LIGTH_LOCATIONS = {
        'Global_ambient': glGetUniformLocation( asteroid_shader, 'Global_ambient' ),
        'Light_ambient': glGetUniformLocation( asteroid_shader, 'Light_ambient' ),
        'Light_diffuse': glGetUniformLocation( asteroid_shader, 'Light_diffuse' ),
        'Light_location': glGetUniformLocation( asteroid_shader, 'Light_location' ),
        'Light_specular': glGetUniformLocation( asteroid_shader, 'Light_specular' ),
        'Material_ambient': glGetUniformLocation( asteroid_shader, 'Material_ambient' ),
        'Material_diffuse': glGetUniformLocation( asteroid_shader, 'Material_diffuse' ),
        'Material_shininess': glGetUniformLocation( asteroid_shader, 'Material_shininess' ),
        'Material_specular': glGetUniformLocation( asteroid_shader, 'Material_specular' ),
    }

def apply_texture():
    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_BLEND)

    global textureID
    texture_img = Image.open('./assets/asteroid/rock.png')
    width, height, texture_img = texture_img.size[0], texture_img.size[1], texture_img.tobytes("raw", "RGB", 0, -1)
    textureID = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, textureID)
    gluBuild2DMipmaps(GL_TEXTURE_2D, 3, width, height, GL_RGB, GL_UNSIGNED_BYTE, texture_img)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER,GL_NEAREST)
    
def debugCameraAxes():
    glBegin(GL_LINES)
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(10.0, 0.0, 0.0)
    glEnd()

    glBegin(GL_LINES)
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, 10.0, 0.0)
    glEnd()

    glBegin(GL_LINES)
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, 0.0, 10.0)
    glEnd()

if __name__ == "__main__":
    main()
