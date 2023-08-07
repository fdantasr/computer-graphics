from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np

class Particles:

    def __init__(self, vertex: list):
        self.vert = np.array(vertex, np.float32)


class ParticlesSystem:
    def __init__(self, position):
        self.position = np.array(position, np.float32)
        self.VELOCITY = 0.2
        self.TIMER = 0.05
        self.particles = []
        self.particlesInc = 0        
        self.ttl = 1
        
        for i in range(15):
            x = np.random.randn() * self.VELOCITY
            y = np.random.randn() * self.VELOCITY
            z = np.random.randn() * self.VELOCITY
            self.particles.append(Particles([x, y, z]))

    def draw(self):
        for i in range(15):
            positionX = self.position[0] - self.particles[i].vert[0] * self.particlesInc
            positionY = self.position[1] - self.particles[i].vert[1] * self.particlesInc
            positionZ = self.position[2] - self.particles[i].vert[2] * self.particlesInc

            glPushMatrix()
            glColor4f(0.4,0.4,0.4, self.ttl)
            glTranslatef(positionX, positionY, positionZ)
            glutSolidSphere(0.1, 5, 5)
            glPopMatrix()

        self.ttl -= self.TIMER
        self.particlesInc += 1