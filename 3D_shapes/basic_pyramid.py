import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
verteces=((-1,-1,-1),
          (-1,-1,1),
          (1,-1,1),
          (1,-1,-1),
          (0,1,0)
    )
edges=((0,1),(0,3),(0,4),(1,2),(1,4),(2,3),(2,4),(3,4)


    )

surfaces=((0,1,2,3),(0,4,1),(0,4,3),(2,3,4),(4,1,2),)

colour=((0,0,1),(0,1,0),(1,0,0),(1,1,0),(1,0,1))

def pyramid():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verteces[vertex])
    glEnd()
    x=0
    
    glBegin(GL_QUADS)
    for surface in surfaces:
        glColor3fv(colour[x])
        for vertex in surface:
            glVertex3fv(verteces[vertex])
        x+=1
    glEnd()

def main():
    pygame.init()
    display=(800,600)
    pygame.display.set_mode(display,DOUBLEBUF|OPENGL)
    gluPerspective(45,(display[0]/display[1]),0.1,50.0)
    glTranslatef(0,0,-5)
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glRotate(1,1,-5,1)
        pyramid()
        pygame.display.flip()
        pygame.time.wait(10)
main()
