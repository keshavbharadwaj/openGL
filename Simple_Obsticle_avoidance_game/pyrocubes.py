import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random

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






verteces2=((-1,-1,-1),
          (-1,-1,1),
          (1,-1,1),
          (1,-1,-1),
          (0,1,0)
    )
edges2=((0,1),(0,3),(0,4),(1,2),(1,4),(2,3),(2,4),(3,4)


    )

surfaces2=((0,1,2,3),(0,4,1),(0,4,3),(2,3,4),(4,1,2),)

colour=((1,0,0),(0,1,0),(0,0,1),(0,1,0),(1,1,1),(0,1,1),(1,0,0),(0,1,0),(0,0,1),(0,1,0),(1,1,1),(0,1,1))


##ground_ver=((-10,-1.1,20),(10,-1.1,20),(-10,-1.1,-300),(+10,-1.1,-300))
##
##def ground():
##    glBegin(GL_QUADS)
##    glColor3fv((1,0,1))
##    for v in ground_ver:
##        glVertex3fv(v)
##        
##    glEnd()
##    

def pyramid(y):
    glBegin(GL_LINES)
    for edge in edges2:
        for vertex in edge:
            glVertex3fv(y[vertex])
    glEnd()
    
    glBegin(GL_QUADS)
    for surface in surfaces2:
        x=0
        for vertex in surface:
            x+=1
            glColor3fv(colour[x])
            glVertex3fv(y[vertex])
    glEnd()

def cube(x):

    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(x[vertex])
    
    glEnd()
    glBegin(GL_QUADS)
    for surface in surfaces:
        c=0
        for vertex in surface:
            c+=1
            glColor3fv(colour[c])
            
            glVertex3fv(x[vertex])
    glEnd()

def make_vertex(max,choose,min_distance=-20,camera_x=0,camera_y=0):

    camera_x=-1*int(camera_x)
    camera_y=-1*int(camera_y)
    
    x_value=random.randrange(camera_x-20,camera_x+20)
    y_value=random.randrange(camera_y-20,camera_y+20)
    z_value=random.randrange(-max,min_distance)

    new_obj=[]
    if choose==0:
        for vert in verteces:
            new_vert=[]
            vertx=vert[0]+x_value
            verty=vert[1]+y_value
            vertz=vert[2]+z_value
            new_vert.append(vertx)
            new_vert.append(verty)
            new_vert.append(vertz)
            new_obj.append(new_vert)
    if choose==1:
        for vert in verteces2:
            new_vert=[]
            vertx=vert[0]+x_value
            verty=vert[1]+y_value
            vertz=vert[2]+z_value
            new_vert.append(vertx)
            new_vert.append(verty)
            new_vert.append(vertz)
            new_obj.append(new_vert)
    return new_obj


def main():
    pygame.init()
    score=0
    display = (800,600)
    max_distance=100
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    gluPerspective(45,(display[0]/display[1]),0.1,max_distance)
    glRotatef(0,0,0,0)
    glTranslatef(0,0,-40)
    #passed=False
    x_move=0
    y_move=0
    
    cur_x=0
    cur_y=0

    objs={}
    choices=[]
    game_speed=2

    gg=3
    
    dir_speed=2
    h=True
    for p in range(55):
        j=random.randrange(0,2)
        objs[p]=make_vertex(max_distance,j)
        choices.append(j)
    while h:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key==K_LEFT:
                    x_move=dir_speed
                if event.key==K_RIGHT:
                    x_move=-dir_speed
                if event.key==K_UP:
                    y_move=-dir_speed
                if event.key==K_DOWN:
                    y_move=dir_speed
            if event.type==pygame.KEYUP:
                if event.key==K_LEFT or event.key==K_RIGHT:
                    x_move=0
                if event.key==K_UP or event.key==K_DOWN:
                    y_move=0

                    
##            if event.type==pygame.MOUSEBUTTONDOWN:
##                if event.button==4:
##                    glTranslatef(0,0,1)
##                if event.button==5:
##                    glTranslatef(0,0,-1)
        x=glGetDoublev(GL_MODELVIEW_MATRIX)

        camera_z=x[3][2]
        camera_x=x[3][0]
        camera_y=x[3][1]

        cur_x+=x_move
        cur_y+=y_move

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        for obj in objs:
            choice=choices[obj]
            if choice==0:
                cube(objs[obj])
            if choice==1:
                pyramid(objs[obj])
            
        for obj in objs:
            if camera_z<=objs[obj][0][2]:
                #print("passed_cube")
                score+=1
                new_max = int(-1*(camera_z-(max_distance*2)))
                j=random.randrange(0,2)
                objs[obj]=make_vertex(new_max,j,int(camera_z-max_distance),cur_x,cur_y)
                choices[obj]=j
            if camera_z<objs[obj][0][2]+gg and camera_z>objs[obj][0][2]-gg and camera_x<objs[obj][0][0]+gg and camera_x>objs[obj][0][0]-gg  and camera_y<objs[obj][0][1]+gg and camera_y>objs[obj][0][1]-gg:
                print("gameover")
                print("SCORE : ",score)
                h=False
                break
        glTranslatef(x_move,y_move,game_speed)
        pygame.display.flip()
        #pygame.time.wait(10)

main()
pygame.quit()
quit()
