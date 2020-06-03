#Moder opengl
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL import shaders
import numpy as np

#1)
vertex_src="""
#version 330 

in vec3 a_position;
in vec3 a_color;
out vec3 color;
void main()
{ gl_Position = vec4(a_position,1.0);
  color=a_color;
}

"""

fragment_src="""
#version 330
in vec3 color;
out vec4 FragColor;
void main()
{FragColor=vec4(color,1.0f);
}
"""

shader=None


def initialize():
    global vertex_src
    global fragment_src
    global shader

    tri=[-0.5,-0.5,0.0,
         0.5,-0.5,0.0,
         0.0,0.5,0.0,
         1,0,0,
         0,1,0,
         0,0,1]

    triangle=np.array(tri,dtype=np.float32)
    #2)
    vertexshader= shaders.compileShader(vertex_src,GL_VERTEX_SHADER)
    fragmentshader=shaders.compileShader(fragment_src,GL_FRAGMENT_SHADER)
    shader=shaders.compileProgram(vertexshader,fragmentshader)

    

    #3)
    #allocate memory for our object
    vbo=glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER,vbo)
    #4)
    glBufferData(GL_ARRAY_BUFFER,triangle.nbytes,triangle,GL_STATIC_DRAW)

    position= glGetAttribLocation(shader,"a_position")
    glEnableVertexAttribArray(position)
    glVertexAttribPointer(position,3,GL_FLOAT,GL_FALSE,0,ctypes.c_void_p(0))

    position= glGetAttribLocation(shader,"a_color")
    glEnableVertexAttribArray(position)
    glVertexAttribPointer(position,3,GL_FLOAT,GL_FALSE,0,ctypes.c_void_p(36))
    
    #5)
    glUseProgram(shader)
    glClearColor(0,0.1,0.1,1)
  
    



if not glfw.init():
    raise Exception("HOGE")

window=glfw.create_window(1280,720,"BOX",None,None)
if not window:
    glfw.terminate()
    raise Exception("glfw window cannot be crated")

glfw.set_window_pos(window,200,200)
glfw.make_context_current(window)
initialize()
while not glfw.window_should_close(window):
    
    glfw.poll_events()
    glClear(GL_COLOR_BUFFER_BIT)
    glDrawArrays(GL_TRIANGLE_STRIP,0,3)
    glfw.swap_buffers(window)


##steps:
##    1) create a vertex and fragment source
##    2) compile it to a shader program
##    3) create vertex buffer object vbo
##    4) send the vertex data to this vbo
##    5) Use this program with opengl

    
