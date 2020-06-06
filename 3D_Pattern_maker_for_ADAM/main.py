import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL import shaders
import numpy as np
import pyrr
from textureloader import load_texture
from inputs import ini
from pygame.locals import *
def list_rotation(l):
    k=l[0]
    for i in range(len(l)-1):
        l[i]==l[i+1]
    l[-1]=k
    return l
l=ini()
tex={0:"all2.png",1:"all3.png",2:"all4.png",3:"all5.png",4:"all6.png",5:"all7.png"}

vertex_src = """
#version 330 

layout(location=0)in vec3 a_position;

layout(location=1)in vec2 a_texture;


out vec2 v_texture;

uniform mat4 model;
uniform mat4 projection;

void main()
{ gl_Position = projection*model*vec4(a_position,1.0);

  v_texture=a_texture;

}

"""

fragment_src = """
#version 330


in vec2 v_texture;

out vec4 FragColor;

uniform sampler2D s_texture;

void main()
{  FragColor=texture(s_texture,v_texture);
}
"""

pygame.init()
pygame.display.set_mode((1280, 720), pygame.OPENGL | pygame.DOUBLEBUF | pygame.RESIZABLE)

x = 0.20
y = 0.30
z = 0.1

frontpicx1 = 895 / 1377
frontpicy1 = 87 / 567
frontpicx2 = 1145 / 1377
frontpicy2 = 87 / 567
frontpicx3 = 893 / 1377
frontpicy3 = 446 / 567
frontpicx4 = 1145 / 1377
frontpicy4 = 445 / 567

sidex1 = 0
sidey1 = 170 / 567

sidex2 = 0
sidey2 = 0

sidex3 = 554 / 1377
sidey3 = 0

sidex4 = 555 / 1377
sidey4 = 171 / 567

topx1 = 0
topy1 = 183 / 567
topx2 = 556 / 1377
topy2 = 186 / 567
topx3 = 553 / 1377
topy3 = 376 / 567
topx4 = 0
topy4 = 374 / 567


cube = [-x, -y, z, frontpicx3, frontpicy3,
        x, -y, z, frontpicx4, frontpicy4,
        x, y, z, frontpicx2, frontpicy2,
        -x, y, z, frontpicx1, frontpicy1,

        -x, -y, -z, frontpicx3, frontpicy3,
        x, -y, -z, frontpicx4, frontpicy4,
        x, y, -z, frontpicx2, frontpicy2,
        -x, y, -z, frontpicx1, frontpicy1,

        x, -y, -z, sidex4, sidey4,
        x, y, -z, sidex2, sidey2,
        x, y, z, sidex1, sidey1,
        x, -y, z, sidex3, sidey3,

        -x, y, -z, sidex4, sidey4,
        -x, -y, -z, sidex2, sidey2,
        -x, -y, z, sidex1, sidey1,
        -x, y, z, sidex3, sidey3,

        -x, -y, -z, topx3, topy3,
        x, -y, -z, topx4, topy4,
        x, -y, z, topx1, topy1,
        -x, -y, z, topx2, topy2,

        x, y, -z, topx3, topy3,
        -x, y, -z, topx4, topy4,
        -x, y, z, topx1, topy1,
        x, y, z, topx2, topy2]

indices = [0, 1, 2, 2, 3, 0,
           4, 5, 6, 6, 7, 4,
           8, 9, 10, 10, 11, 8,
           12, 13, 14, 14, 15, 12,
           16, 17, 18, 18, 19, 16,
           20, 21, 22, 22, 23, 20]

v = np.array(cube, dtype=np.float32)
i = np.array(indices, dtype=np.uint32)

shader = shaders.compileProgram(shaders.compileShader(vertex_src, GL_VERTEX_SHADER),
                                shaders.compileShader(fragment_src, GL_FRAGMENT_SHADER))

vbo = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vbo)
glBufferData(GL_ARRAY_BUFFER, v.nbytes, v, GL_STATIC_DRAW)

ebo = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, i.nbytes, i, GL_STATIC_DRAW)

glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, v.itemsize * 5, ctypes.c_void_p(0))

glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, v.itemsize * 5, ctypes.c_void_p(12))

cubetextures=[]
texture = glGenTextures(6)

for i in range(len(l)):
    cubetextures=load_texture(texture[i],tex[i])
needed=[]
j=0
for i in range(len(l)):
    k=l[i]
    while k!=0:
        needed.append(j)
        k-=1
    j+=1
print(l)
glUseProgram(shader)
glClearColor(0, 0.1, 0.1, 1)
glEnable(GL_DEPTH_TEST)
##glEnable(GL_BLEND)
##glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

model_loc = glGetUniformLocation(shader, "model")
proj_loc = glGetUniformLocation(shader, "projection")

projection = pyrr.matrix44.create_perspective_projection_matrix(45, 1280 / 720, 0.1,100)  # field_of_view,aspect_ration,nearclippingplane,farclipping,plane

glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)

translations=[]
rotations=[]
a=1
b=1
c=-3
for i in range(sum(l)):
    cube = pyrr.matrix44.create_from_translation(pyrr.Vector3([a, b, c]))
    translations.append(cube)
    c-=0.2
    a-=0
    b-=0
    rot_x = pyrr.Matrix44.from_x_rotation(0.0)
    rot_y = pyrr.Matrix44.from_y_rotation(0.0)
    rotation = pyrr.matrix44.multiply(rot_x, rot_y)
    rotations.append(rotation)
current_box=None
curr_z_move=0
z_move=0
curr_rotation=1
print(translations)
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.VIDEORESIZE:
            glViewport(0, 0, event.w, event.h)
        if event.type == pygame.KEYDOWN:
            if event.key == K_0:
                current_box=0
            if event.key == K_1:
                print("triggered")
                current_box=1
            if event.key == K_2:
                current_box=2
            if event.key == K_3:
                current_box=3
            if event.key == K_4:
                current_box=4
            if event.key == K_5:
                current_box=5
            if event.key == K_6:
                current_box=6
            if event.key == K_7:
                current_box=7
            if event.key == K_8:
                current_box=8
            if event.key == K_9:
                current_box=9
            if event.key ==K_UP:
                z_move=pyrr.matrix44.create_from_translation(pyrr.Vector3([0,+0.01, 0]))
                #print(z_move)
                curr_z_move = curr_z_move + z_move-pyrr.matrix44.create_from_translation(pyrr.Vector3([0,0, 0]))
               # print(translations[1])
            if event.key ==K_DOWN:
                z_move=pyrr.matrix44.create_from_translation(pyrr.Vector3([0,-0.01,0]))-pyrr.matrix44.create_from_translation(pyrr.Vector3([0,0, 0]))
                #print(z_move)
                curr_z_move = curr_z_move + z_move
                #print(translations[1])
            if event.key==K_x:
                z_move = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, +0.01])) - pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))
                curr_z_move=curr_z_move+z_move
            if event.key==K_z:
                z_move = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, -0.01])) - pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))
                curr_z_move = curr_z_move + z_move
            if event.key ==K_LEFT:
                z_move = pyrr.matrix44.create_from_translation(pyrr.Vector3([-0.01, 0, 0]))
                #print(z_move)
                curr_z_move = curr_z_move + z_move - pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))
                #print(translations[1])
            if event.key ==K_RIGHT:
                z_move = pyrr.matrix44.create_from_translation(pyrr.Vector3([0.01, 0, 0]))
                #print(z_move)
                curr_z_move = curr_z_move + z_move - pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))
                #print(translations[1])

        if event.type == pygame.KEYUP:
            if event.key == K_LEFT or event.key == K_RIGHT or event.key==K_UP or event.key==K_DOWN or event.key==K_x or event.key==K_z:
                curr_z_move = 0
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button==1:
                curr_rotation=pyrr.matrix44.create_from_x_rotation(0.1)
            if event.button==3:
                curr_rotation=pyrr.matrix44.create_from_y_rotation(0.1)
            if event.button==2:
                curr_rotation = pyrr.matrix44.create_from_z_rotation(0.1)
        if event.type==pygame.MOUSEBUTTONUP:
            if event.button==1:
                curr_rotation=1
            if event.button==3 or event.button==2:
                curr_rotation=1
    ct = pygame.time.get_ticks() / 1000
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    if current_box==None:
        for j in range(len(translations)):
            rot_x = pyrr.Matrix44.from_x_rotation(0.0 )
            rot_y = pyrr.Matrix44.from_y_rotation(0.0 )
            rotation = pyrr.matrix44.multiply(rot_x, rot_y)
            model = pyrr.matrix44.multiply(rotations[j],translations[j])
            glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
            glBindTexture(GL_TEXTURE_2D, texture[needed[j]])
            glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)

    else:
        for j in range(len(translations)):
            if j==current_box:
                translations[j] = translations[j]+curr_z_move
                rotations[j]=pyrr.matrix44.multiply(curr_rotation,rotations[j])
                print(rotation)
            model = pyrr.matrix44.multiply(rotations[j], translations[j])
            glUniformMatrix4fv(model_loc, 1, GL_FALSE,model)
            glBindTexture(GL_TEXTURE_2D, texture[needed[j]])
            glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)
            z_move=0


    pygame.display.flip()
