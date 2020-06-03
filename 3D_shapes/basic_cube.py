import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

verteces=(
    (1,-1,-1),
    (1,1,-1),
    (-1,1,-1),
    (-1,-1,-1),
    (1,-1,1),
    (1,1,1),
    (-1,-1,1),
    (-1,1,1)

    )

edges=((0,1),(0,3),(0,4),(2,1),(2,3),(2,7),(6,3),(6,4),(6,7),(5,1),(5,4),(5,7)

    )

surfaces=((0,1,2,3),(3,2,7,6),(6,7,5,4),(4,5,1,0),(1,5,7,2),(4,0,3,6))

def cube():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verteces[vertex])
    
    glEnd()
    glBegin(GL_QUADS)
    for surface in surfaces:
        glColor3fv((1,0,0))
        for vertex in surface:
            glVertex3fv(verteces[vertex])
    glEnd()

def main():
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    gluPerspective(45,(display[0]/display[1]),0.1,50.0)
    glTranslatef(2,2,-20)
    glRotatef(0,0,0,0)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glRotatef(1,3,1,1)
        cube()
        pygame.display.flip()
        pygame.time.wait(10)
main()
    
