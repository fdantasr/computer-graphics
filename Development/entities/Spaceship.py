from OpenGL.GL import *
import pywavefront as pw
from pywavefront import visualization
import numpy as np

# variable light position
light_position = [0, 0, 0, 1]
amb_light = [0.2, 0.2, 0.2, 1]
diff_light = [0.5, 0.5, 0.5, 1]
spec_light = [1, 1, 1, 1]

# variable material colors
chrome_amb = [0.25, 0.25, 0.25, 1.0]
chrome_dif = [0.4, 0.4, 0.4, 1.0]
chrome_spe = [0.774597, 0.774597, 0.774597, 1.0]
chrome_shi = 0.6*128.0

class Spaceship:
    def __init__(self, obj):
        self.obj = pw.Wavefront(obj)
        self.vertex = np.array([0.0,0.0,0.0],np.float32)
        self.position = [0, 0, 0]
        self.RESISTANCE = 1.3
        self.RESISTANCEB = 0.3
        self.VELOCITY = 0.05
        self.roll = 0
        self.resistanceX = 0
        self.left = 0
        self.right = 0

    def light(self):
        glLightfv(GL_LIGHT0, GL_POSITION, light_position)
        glLightfv(GL_LIGHT0, GL_AMBIENT, amb_light)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, diff_light)
        glLightfv(GL_LIGHT0, GL_SPECULAR, spec_light)
        glLightfv(GL_LIGHT0, GL_QUADRATIC_ATTENUATION,
                  0.1)  # set light attenuation
        glLightfv(GL_LIGHT0, GL_LINEAR_ATTENUATION,
                  0.1)  # set light attenuation
        self.apply_material()

    def apply_material(self):
        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHTING)
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
        glMaterialfv(GL_FRONT, GL_SPECULAR, [1, 1, 1, 1])
        glMaterialfv(GL_FRONT, GL_SHININESS, 50)

    def draw(self):
        glPushMatrix()  # glPushMatrix() saves the current matrix state and pushes it onto a stack for later use
        glTranslatef(
            self.position[0], self.position[1], self.position[2]
        )  # glTranslatef moves the current matrix by the specified x, y, and z values
        glTranslatef(light_position[0], light_position[1], light_position[2])
        glPushMatrix()  # glPushMatrix() saves the current matrix state and pushes it onto a stack for later use
        glRotatef(
            3,
            1,
            0,
            0,  # rotate the obj by 3 degrees on the x axis
        )  # glRotatef rotates the current matrix by the specified angle around the specified x, y, and z values
        glTranslatef(
            0, -1, 1  # move the obj by the specified x, y, and z values
        )  # glTranslatef moves the current matrix by the specified x, y, and z values
        glScalef(
            0.6, 0.6, 0.6  # scales the obj size by 0.2
        )  # glScalef scales the current matrix by the specified x, y, and z values
        glColor3f(
            0.5,
            0,
            0,
        )  # glColor3f sets the current color to the specified red, green, and blue values

        visualization.draw(self.obj)

        glPopMatrix()  # glPOPMatrix() pops the current matrix state off the stack
        glPopMatrix()  # glPOPMatrix() pops the current matrix state off the stack

        self.light()

    def updateMovement(self):
      self.position += self.vertex

      if (not (abs(self.position[0]) <= 7)):
          self.position[0] -= self.vertex[0]

      if (self.position[1] > 15.0):
          self.position[1] = 15.0
      elif (self.position[1] < 0.0):
          self.position[1] = 0.0
          self.vertex[1] = 0.0

    def calculateVelocity(self):
      
      if(self.position[1]==0.0):
          if(self.left):
            self.vertex[0] += - np.cos(0)*self.VELOCITY
            self.vertex[2] += - np.sin(0)*self.VELOCITY
            
          elif(self.right):
            self.vertex[0] += np.cos(0)*self.VELOCITY
            self.vertex[2] += np.sin(0)*self.VELOCITY   
  
          self.resistanceX = (pow(self.RESISTANCE,abs(self.vertex[0]))-1.0)*self.RESISTANCEB
        
      if(self.vertex[0]>self.resistanceX):
          self.vertex[0] -= self.resistanceX
      elif(self.vertex[0]<-self.resistanceX):
          self.vertex[0] += self.resistanceX
      elif(abs(self.vertex[2])<self.resistanceX):
          if(abs(self.vertex[0])>0):
              self.vertex[0] = 0.0
              self.vertex[2] = 0.0

