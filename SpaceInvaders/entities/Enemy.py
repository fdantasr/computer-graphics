from OpenGL.GL import *
from OpenGL.GLU import *
import pywavefront as pw
import numpy

class Enemy:
    def __init__(self, obj, coords):
        self.obj = pw.Wavefront(obj)
        self.position = coords

    def draw(self):
        glPushMatrix()  # glPushMatrix() saves the current matrix state and pushes it onto a stack for later use
        glTranslatef(
            self.position[0], self.position[1], self.position[2]
        )  # glTranslatef moves the current matrix by the specified x, y, and z values
        glScalef(
           0.5,0.5,0.5  # scales the obj size by 0.2
        )  # glScalef scales the current matrix by the specified x, y, and z values
        glPushMatrix()  # glPushMatrix() saves the current matrix state and pushes it onto a stack for later use
        # glColor3f(
        #     0.15, 0.40, 0.125  # set the color of the obj
        # )  # glColor3f sets the current color to be used when drawing
        # visualization.draw(self.obj)

        # glPopMatrix()  # glPOPMatrix() pops the current matrix state off the stack
        # glPopMatrix()  # glPOPMatrix() pops the current matrix state off the stack

    def move(self, x, y, z):
        self.position[0] += x
        self.position[1] += y
        self.position[2] += z
    
    def getVertices(self, material: str):
        vertices = self.obj.materials[material].vertices
        vertices = numpy.array(vertices, dtype=numpy.float32).reshape(-1,6)
        return vertices
