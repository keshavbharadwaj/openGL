import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL import shaders
import numpy as np
import pyrr

vertex_src="""
#version 330 

layout(location=0)in vec3 a_position;
uniform mat4 rotation;

void main()
{ gl_Position = rotation*vec4(a_position,1.0);
}

"""

fragment_src="""
#version 330
out vec4 FragColor;
void main()
{FragColor=vec4(1.0f,0.0f,1.0f,1.0f);
}
"""



cube=[-0.5,-0.5,0.5,
        0.5,-0.5,0.5,
        0.5,0.5,0.5,
        -0.5,0.5,0.5,
      
        -0.5,-0.5,-0.5,
        0.5,-0.5,-0.5,
        0.5,0.5,-0.5,
        -0.5,0.5,-0.5,
    

    ]

i=[ 0,1,2,2,3,0,
    4,5,6,6,7,4,
    4,5,1,1,0,4,
    6,7,3,3,2,6,
    5,6,2,2,1,5,
    7,4,0,0,3,7
    ]


if not glfw.init():
    raise Exception("NOOOOOOOOOOOOOOOO");

window=glfw.create_window(1280,720,"Cube",None,None)

if not window:
    glfw.terminate()
    raise Exception("glfw window cannot be crated")
glfw.set_window_pos(window,200,200)
glfw.make_context_current(window)


vertex=np.array(cube,dtype=np.float32)
indices=np.array(i,dtype=np.uint32)

shader=shaders.compileProgram(shaders.compileShader(vertex_src,GL_VERTEX_SHADER),shaders.compileShader(fragment_src,GL_FRAGMENT_SHADER))
print("here")
vbo=glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER,vbo)
glBufferData(GL_ARRAY_BUFFER,vertex.nbytes,vertex,GL_STATIC_DRAW)

ebo=glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,ebo)
glBufferData(GL_ELEMENT_ARRAY_BUFFER,indices.nbytes,indices,GL_STATIC_DRAW)

glEnableVertexAttribArray(0)
glVertexAttribPointer(0,4,GL_FLOAT,GL_FALSE,0,ctypes.c_void_p(0))



glUseProgram(shader)
rotation_loc=glGetUniformLocation(shader,"rotation")
glClearColor(0,0.1,0.1,1)

while not glfw.window_should_close(window):

    
    glfw.poll_events()
    glClear(GL_COLOR_BUFFER_BIT)
    rot_x=pyrr.Matrix44.from_x_rotation(glfw.get_time())

    glUniformMatrix4fv(rotation_loc,1,GL_FALSE,rot_x)
    #glDrawArrays(GL_TRIANGLE_STRIP,0,4)
    glDrawElements(GL_TRIANGLES,36,GL_UNSIGNED_INT,None)
    glfw.swap_buffers(window)
    
