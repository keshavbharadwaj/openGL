import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL import shaders
import numpy as np
import pyrr
from textureloader import load_texture
import glfw
vertex_src="""
#version 330
layout(location=0)in vec3 a_pos;
layout(location=1)in vec2 a_texture;

out vec2 v_texture;

uniform mat4 model;
void main()
{gl_Position=model*vec4(a_pos,1.0);
v_texture=a_texture;
}
"""

fragment_src="""
#version 330
out vec4 fragcolour;
in vec2 v_texture;
out vec4 colour;
uniform sampler2D s_texture;

void main()
{  colour=vec4(1.8f,0.0f,1.8f,1.8f);
   fragcolour=texture(s_texture,v_texture)*colour;
}
"""

# def window_resize(window, width, height):
#     glViewport(0, 0, width, height)
#
# if not glfw.init():
#     raise Exception("HOGE")
#
# window=glfw.create_window(1280,720,"BOX",None,None)
# if not window:
#     glfw.terminate()
#     raise Exception("glfw window cannot be crated")

# glfw.set_window_pos(window,200,200)
# glfw.set_window_size_callback(window, window_resize)
# glfw.make_context_current(window)



pygame.init()
pygame.display.set_mode((1280, 720), pygame.OPENGL | pygame.DOUBLEBUF | pygame.RESIZABLE)

sizex=2000
sizey=1080

frontside1x=1641/sizex
frontside1y=582/sizey
frontside2x=1517/sizex
frontside2y=13/sizey
frontside3x=1307/sizex
frontside3y=15/sizey
frontside4x=1184/sizex
frontside4y=585/sizey
frontside5x=1283/sizex
frontside5y=855/sizey
frontside6x=1539/sizex
frontside6y=855/sizey

back1x=259/sizex
back1y=513/sizey
back2x=189/sizex
back2y=181/sizey
back3x=97/sizex
back3y=182/sizey
back4x=30/sizex
back4y=511/sizey
back5x=103/sizex
back5y=621/sizey
back6x=185/sizex
back6y=624/sizey

side1x=465/sizex
side1y=718/sizey
side2x=722/sizex
side2y=719/sizey
side3x=720/sizex
side3y=528/sizey
side4x=466/sizex
side4y=529/sizey

big1x=297/sizex
big1y=468/sizey
big2x=299/sizex
big2y=61/sizey
big3x=1041/sizex
big3y=64/sizey
big4x=1040/sizex
big4y=468/sizey


scale=0.45

# coffin=[ -0.75*scale,1.5*scale,1*scale,   frontside1x,frontside1y,  #done
#          -0.5*scale,-1*scale,1*scale,     frontside2x,frontside2y,
#          0*scale,-1*scale,1*scale,        frontside3x,frontside3y,
#          0.25*scale,1.5*scale,1*scale,    frontside4x,frontside4y,
#          0*scale,2*scale,1*scale,         frontside5x,frontside5y,
#          -0.5*scale,2*scale,1*scale,      frontside6x,frontside6y,
#
#         -0.75*scale,1.5*scale,0.5*scale,  back1x,back1y,    #done
#         -0.5*scale,-1*scale,0.5*scale,    back2x,back2y,
#          0*scale,-1*scale,0.5*scale,      back3x,back3y,
#          0.25*scale,1.5*scale,0.5*scale,  back4x,back4y,
#          0*scale,2*scale,0.5*scale,       back5x,back5y,
#         -0.5*scale,2*scale,0.5*scale,     back6x,back6y,
#
#         -0.5*scale,-1*scale,1*scale,      side1x,side1y,    #done
#          0*scale,-1*scale,1*scale,        side2x,side2y,
#          0*scale,-1*scale,0.5*scale,      side3x,side3y,
#          -0.5*scale,-1*scale,0.5*scale,   side4x,side4y,
#
#          0*scale,-1*scale,1*scale,        big4x,big4y,
#          0.25*scale,1.5*scale,1*scale,    big1x,big1y,
#         0*scale,-1*scale,0.5*scale,      big3x,big3y,
#          0.25*scale,1.5*scale,0.5*scale,  big2x,big2y,
#
#         0.25*scale,1.5*scale,1*scale,    side2x,side2y,    #20,21,22,22,21,23 done
#          0*scale,2*scale,1*scale,         side1x,side1y,
#          0.25*scale,1.5*scale,0.5*scale,  side3x,side3y,
#          0*scale,2*scale,0.5*scale,       side4x,side4y,
#
#           0*scale,2*scale,1*scale,        side2x,side2y,    #24,25,26,26,25,27,curr done
#          -0.5*scale,2*scale,1*scale,      side1x,side1y,
#           0*scale,2*scale,0.5*scale,      side3x,side3y,
#          -0.5*scale,2*scale,0.5*scale,    side4x,side4y,
#
#          -0.5*scale,2*scale,1*scale,      side2x,side2y,    #28,29,30,30,29,31 done
#          -0.75*scale,1.5*scale,1*scale,   side1x,side1y,
#          -0.5*scale, 2*scale, 0.5*scale,  side3x,side3y,
#          -0.75*scale, 1.5*scale, 0.5*scale,side4x,side4y,
#
#          -0.75*scale,1.5*scale,1*scale,   big4x,big4y,    #32,33,34,34,33,35 done
#          -0.5*scale,-1*scale,1*scale,     big1x,big1y,
#          -0.75*scale,1.5*scale, 0.5*scale,big3x,big3y,
#         -0.5*scale, -1*scale, 0.5*scale, big2x,big2y
#
#          ]



coffin=[ -0.75*scale,1.5*scale,1*scale,   frontside1x,frontside1y,  #done
         -0.5*scale,-1*scale,1*scale,     frontside2x,frontside2y,
         0*scale,-1*scale,1*scale,        frontside3x,frontside3y,
         0.25*scale,1.5*scale,1*scale,    frontside4x,frontside4y,
         0*scale,2*scale,1*scale,         frontside5x,frontside5y,
         -0.5*scale,2*scale,1*scale,      frontside6x,frontside6y,

        -0.75*scale,1.5*scale,0.75*scale,  back1x,back1y,    #done
        -0.5*scale,-1*scale,0.75*scale,    back2x,back2y,
         0*scale,-1*scale,0.75*scale,      back3x,back3y,
         0.25*scale,1.5*scale,0.75*scale,  back4x,back4y,
         0*scale,2*scale,0.75*scale,       back5x,back5y,
        -0.5*scale,2*scale,0.75*scale,     back6x,back6y,

        -0.5*scale,-1*scale,1*scale,      side1x,side1y,    #done
         0*scale,-1*scale,1*scale,        side2x,side2y,
         0*scale,-1*scale,0.75*scale,      side3x,side3y,
         -0.5*scale,-1*scale,0.75*scale,   side4x,side4y,

         0*scale,-1*scale,1*scale,        big4x,big4y,
         0.25*scale,1.5*scale,1*scale,    big1x,big1y,
        0*scale,-1*scale,0.75*scale,      big3x,big3y,
         0.25*scale,1.5*scale,0.75*scale,  big2x,big2y,

        0.25*scale,1.5*scale,1*scale,    side2x,side2y,    #20,21,22,22,21,23 done
         0*scale,2*scale,1*scale,         side1x,side1y,
         0.25*scale,1.5*scale,0.75*scale,  side3x,side3y,
         0*scale,2*scale,0.75*scale,       side4x,side4y,

          0*scale,2*scale,1*scale,        side2x,side2y,    #24,25,26,26,25,27,curr done
         -0.5*scale,2*scale,1*scale,      side1x,side1y,
          0*scale,2*scale,0.75*scale,      side3x,side3y,
         -0.5*scale,2*scale,0.75*scale,    side4x,side4y,

         -0.5*scale,2*scale,1*scale,      side2x,side2y,    #28,29,30,30,29,31 done
         -0.75*scale,1.5*scale,1*scale,   side1x,side1y,
         -0.5*scale, 2*scale, 0.75*scale,  side3x,side3y,
         -0.75*scale, 1.5*scale, 0.75*scale,side4x,side4y,

         -0.75*scale,1.5*scale,1*scale,   big4x,big4y,    #32,33,34,34,33,35 done
         -0.5*scale,-1*scale,1*scale,     big1x,big1y,
         -0.75*scale,1.5*scale, 0.75*scale,big3x,big3y,
        -0.5*scale, -1*scale, 0.75*scale, big2x,big2y

         ]

# scale=0.5
# for i in range(len(coffin)):
#     coffin[i]=coffin[i]*scale

indices=[0,1,5,4,3,2,1,5,2,2,5,4,
         6,11,10,7,8,9,10,6,7,7,10,9,
         12,13,14,14,15,12,#working
         16,17,18,18,17,19,#working
         20,21,22,22,21,23,
         24,25,26,26,25,27,
         28,29,30,30,29,31,
         32,33,34,34,33,35,
]
v=np.array(coffin,dtype=np.float32)
print(v)
i = np.array(indices, dtype=np.uint32)

shader=shaders.compileProgram(shaders.compileShader(vertex_src,GL_VERTEX_SHADER),shaders.compileShader(fragment_src,GL_FRAGMENT_SHADER))

vbo=glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER,vbo)
glBufferData(GL_ARRAY_BUFFER,v.nbytes,v,GL_STATIC_DRAW)

ebo=glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,ebo)
glBufferData(GL_ELEMENT_ARRAY_BUFFER,i.nbytes,i,GL_STATIC_DRAW)

glEnableVertexAttribArray(0)
glVertexAttribPointer(0,3,GL_FLOAT,GL_FALSE,v.itemsize*5,ctypes.c_void_p(0))

glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, v.itemsize * 5, ctypes.c_void_p(12))

texture=glGenTextures(1)

t=load_texture(texture,"all7.png")
glBindTexture(GL_TEXTURE_2D, texture)
glUseProgram(shader)
glClearColor(0.0, 0.1, 0.1, 1)
glEnable(GL_DEPTH_TEST)
model_loc = glGetUniformLocation(shader, "model")
model = pyrr.Matrix44.from_x_rotation(1)
curr_rotation=pyrr.matrix44.create_from_x_rotation(0.1)


translation = pyrr.matrix44.create_from_translation(pyrr.Vector3([0,-0.0,-0.0]))

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    ct = pygame.time.get_ticks() / 1000
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    rot_x = pyrr.Matrix44.from_x_rotation(0.2*ct)
    rot_y = pyrr.Matrix44.from_y_rotation(0.5*ct)
    rotation = pyrr.matrix44.multiply(rot_x, rot_y)
    model = pyrr.matrix44.multiply(rotation, translation)
   # model=translation
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
    # glDrawArrays(GL_TRIANGLE_STRIP,0,4)
    glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)

    pygame.display.flip()