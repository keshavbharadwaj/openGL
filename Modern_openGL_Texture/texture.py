import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL import shaders
import numpy as np
import pyrr
from PIL import Image

vertex_src="""
#version 330 

layout(location=0)in vec3 a_position;
layout(location=1)in vec3 a_color;
layout(location=2)in vec2 a_texture;

out vec3 v_color;
out vec2 v_texture;

uniform mat4 rotation;

void main()
{ gl_Position = rotation*vec4(a_position,1.0);
  v_color=a_color;
  v_texture=a_texture;
}

"""

fragment_src="""
#version 330

in vec3 v_color;
in vec2 v_texture;

out vec4 FragColor;

uniform sampler2D s_texture;

void main()
{  FragColor=texture(s_texture,v_texture);
}
"""



if not glfw.init():
    raise Exception("HOGE")

window=glfw.create_window(1280,720,"BOX",None,None)
if not window:
    glfw.terminate()
    raise Exception("glfw window cannot be crated")


glfw.set_window_pos(window,200,200)
glfw.make_context_current(window)


cube     = [-0.5, -0.5,  0.5,  1.0, 0.0, 0.0,  0.0, 0.0,
             0.5, -0.5,  0.5,  0.0, 1.0, 0.0,  1.0, 0.0,
             0.5,  0.5,  0.5,  0.0, 0.0, 1.0,  1.0, 1.0,
            -0.5,  0.5,  0.5,  1.0, 1.0, 1.0,  0.0, 1.0,

            -0.5, -0.5, -0.5,  1.0, 0.0, 0.0,  0.0, 0.0,
             0.5, -0.5, -0.5,  0.0, 1.0, 0.0,  1.0, 0.0,
             0.5,  0.5, -0.5,  0.0, 0.0, 1.0,  1.0, 1.0,
            -0.5,  0.5, -0.5,  1.0, 1.0, 1.0,  0.0, 1.0,

             0.5, -0.5, -0.5,  1.0, 0.0, 0.0,  0.0, 0.0,
             0.5,  0.5, -0.5,  0.0, 1.0, 0.0,  1.0, 0.0,
             0.5,  0.5,  0.5,  0.0, 0.0, 1.0,  1.0, 1.0,
             0.5, -0.5,  0.5,  1.0, 1.0, 1.0,  0.0, 1.0,

            -0.5,  0.5, -0.5,  1.0, 0.0, 0.0,  0.0, 0.0,
            -0.5, -0.5, -0.5,  0.0, 1.0, 0.0,  1.0, 0.0,
            -0.5, -0.5,  0.5,  0.0, 0.0, 1.0,  1.0, 1.0,
            -0.5,  0.5,  0.5,  1.0, 1.0, 1.0,  0.0, 1.0,

            -0.5, -0.5, -0.5,  1.0, 0.0, 0.0,  0.0, 0.0,
             0.5, -0.5, -0.5,  0.0, 1.0, 0.0,  1.0, 0.0,
             0.5, -0.5,  0.5,  0.0, 0.0, 1.0,  1.0, 1.0,
            -0.5, -0.5,  0.5,  1.0, 1.0, 1.0,  0.0, 1.0,

             0.5,  0.5, -0.5,  1.0, 0.0, 0.0,  0.0, 0.0,
            -0.5,  0.5, -0.5,  0.0, 1.0, 0.0,  1.0, 0.0,
            -0.5,  0.5,  0.5,  0.0, 0.0, 1.0,  1.0, 1.0,
             0.5,  0.5,  0.5,  1.0, 1.0, 1.0,  0.0, 1.0]

indices = [0,  1,  2,  2,  3,  0,
           4,  5,  6,  6,  7,  4,
           8,  9, 10, 10, 11,  8,
          12, 13, 14, 14, 15, 12,
          16, 17, 18, 18, 19, 16,
          20, 21, 22, 22, 23, 20]

v=np.array(cube,dtype=np.float32)
i=np.array(indices,dtype=np.uint32)

shader=shaders.compileProgram(shaders.compileShader(vertex_src,GL_VERTEX_SHADER),shaders.compileShader(fragment_src,GL_FRAGMENT_SHADER))

vbo=glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER,vbo)
glBufferData(GL_ARRAY_BUFFER,v.nbytes,v,GL_STATIC_DRAW)

ebo=glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,ebo)
glBufferData(GL_ELEMENT_ARRAY_BUFFER,i.nbytes,i,GL_STATIC_DRAW)

glEnableVertexAttribArray(0)
glVertexAttribPointer(0,3,GL_FLOAT,GL_FALSE,v.itemsize*8,ctypes.c_void_p(0))

glEnableVertexAttribArray(1)
glVertexAttribPointer(1,3,GL_FLOAT,GL_FALSE,v.itemsize*8,ctypes.c_void_p(12))

glEnableVertexAttribArray(2)
glVertexAttribPointer(2,2,GL_FLOAT,GL_FALSE,v.itemsize*8,ctypes.c_void_p(24))

texture=glGenTextures(1)
glBindTexture(GL_TEXTURE_2D,texture)

glTexParameteri(GL_TEXTURE_2D , GL_TEXTURE_WRAP_S , GL_REPEAT)
glTexParameteri(GL_TEXTURE_2D , GL_TEXTURE_WRAP_T , GL_REPEAT)

glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

img=Image.open("dog.png")
img=img.transpose(Image.FLIP_TOP_BOTTOM)
w,h=img.width,img.height
img_data = img.convert("RGBA").tobytes()
glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA,w,h,0,GL_RGBA,GL_UNSIGNED_BYTE,img_data)


glUseProgram(shader)
glClearColor(0, 0.1, 0.1, 1)
glEnable(GL_DEPTH_TEST)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

rotation_loc = glGetUniformLocation(shader, "rotation")



while not glfw.window_should_close(window):
    
    glfw.poll_events()
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    rot_x = pyrr.Matrix44.from_x_rotation(0.5 * glfw.get_time())
    rot_y = pyrr.Matrix44.from_y_rotation(0.8 * glfw.get_time())

    glUniformMatrix4fv(rotation_loc, 1, GL_FALSE, pyrr.matrix44.multiply(rot_x, rot_y))
    #glDrawArrays(GL_TRIANGLE_STRIP,0,4)
    glDrawElements(GL_TRIANGLES,len(indices),GL_UNSIGNED_INT,None)
    glfw.swap_buffers(window)

glfw.terminate()
