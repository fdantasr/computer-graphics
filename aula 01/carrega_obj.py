from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import pywavefront

#pacotes necessarios para executar
#pip install pywavefront
#pip install pyglet

T = 0.2
T2 = 0
T3 = 0

quadric = None

def display():
    global quadric
    global T
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glRotatef(T ,0,0,1)
    glRotatef(T2,0,1,0)
    glRotatef(T3,1,0,0)
    
    glColor3f(0.7, 0.7, 0.7) #Cor do objeto
    
    vertice = objeto.materials['default0'].vertices
    triang_count = len(vertice) / 3 #conta quantos triangulos tem no objeto
    
    glEnableClientState(GL_VERTEX_ARRAY) #habilita o uso de array de vertices, uma função só para tudo que é vertice. Substitui o glBegin e glEnd
    glVertexPointer(3, GL_FLOAT, 0, vertice) #diz que o array de vertices esta em 3 dimensoes e que nao tem nada entre um vertice e outro (0) e passa o array de vertices. 
    glDrawArrays(GL_TRIANGLES, 0, int(triang_count)) #desenha o que esta no array de vertices
    #visualization.draw(objeto)
    
    
    #gluCylinder(quadric,0.0,0.6,0.5,4,1);	
    #glutSolidTeapot(T)
    #glutSolidSphere(0.5, 8, 8)
    
    glPopMatrix()
    
    glutSwapBuffers()
    
def Keys(key, x, y):
    global T
    global T2
    global T3
    
    if(key == GLUT_KEY_LEFT ): 
        T -= 5 
    elif(key == GLUT_KEY_RIGHT ): 
        T += 5 
    elif(key == GLUT_KEY_UP ): 
        T2 -= 5 
    elif(key == GLUT_KEY_DOWN ): 
        T2 += 5 
    elif(key == GLUT_KEY_PAGE_UP ): 
        T3 += 5 
    elif(key == GLUT_KEY_PAGE_DOWN ): 
        T3 -= 5         
       
def animacao(value):
    global T
    #T += 5
    glutPostRedisplay()
    glutTimerFunc(30, animacao,1)

def init():
    global quadric
    glClearColor( 0.0, 0.0, 0.0, 0.0 )
    glClearDepth( 1.0 )

    glHint( GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST )

    glLightModelfv( GL_LIGHT_MODEL_AMBIENT, [0.3, 0.3, 0.3, 1.0] )
    glLightfv( GL_LIGHT0, GL_AMBIENT, [ 0.3, 0.3, 0.3, 1.0] )
    glLightfv( GL_LIGHT0, GL_DIFFUSE, [0.6, 0.6, 0.6, 1] )
    glLightfv( GL_LIGHT0, GL_POSITION, [2.0, 2.0, 1.0, 0.0])
    glEnable( GL_LIGHT0 )
    glEnable( GL_COLOR_MATERIAL )
    glShadeModel( GL_SMOOTH )
    glLightModeli( GL_LIGHT_MODEL_TWO_SIDE, GL_FALSE )
    
    glEnable(GL_DEPTH_TEST)
    glDepthMask(GL_TRUE)
    glDepthFunc(GL_LEQUAL)
    glDepthRange(0.0, 1.0)
   
    #quadric=gluNewQuadric()								
    #gluQuadricNormals(quadric, GLU_SMOOTH)				
    #gluQuadricTexture(quadric, GL_TRUE)

glutInit()
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(500, 500)
glutInitWindowPosition(100, 100)
wind = glutCreateWindow("A Coisa")
init()
objeto = pywavefront.Wavefront('maluco.obj')
glutDisplayFunc(display)
glutTimerFunc(30,animacao,1) #chama a funcao animacao a cada 30 milisegundos, chama o display. 
glutSpecialFunc(Keys) #Esse callback é chamado quando uma tecla especial é pressionada
glutMainLoop()
