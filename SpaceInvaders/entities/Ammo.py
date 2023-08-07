from OpenGL.GL import *
from OpenGL.GLU import *
import pywavefront
from pywavefront import visualization


class Ammo():
    def __init__(self, position):
        self.position = position
        self.obj = pywavefront.Wavefront("./assets/ammo.obj")

    def draw(self):
        # glEnable(GL_COLOR_MATERIAL)
        glPushMatrix()
        glTranslatef(
            self.position[0], self.position[1], self.position[2]
        )
        glPushMatrix()
        glScalef(0.3,0.3,0.3)
        glColor3f(0.95, 0, 0)
        visualization.draw(self.obj)
        glPopMatrix()
        glPopMatrix()
        # glDisable(GL_COLOR_MATERIAL)

    def move(self):
      # if (self.position[1] <= 3.0):
      #   self.position += [0, 0.03, -.4]
      # else: 
      self.position += [0, 0.05, -.4]

    def isOutOfBounds(self):
        return self.position[2] <= -40