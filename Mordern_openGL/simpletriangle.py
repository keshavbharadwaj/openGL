import glfw
import cv2
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
verteces=[-1,-1,-1,
          -1,-1,1,
          1,-1,1,
          1,-1,-1,
          0,1,0
    ]


v2=[-0.5,-0.5,0,
    0.5,0.5,0,
    0,0.5,0
    ]
vertices=np.array(v2,dtype=np.float32)


if not glfw.init():
    raise Exception("glfw cannot be initialised")

window=glfw.create_window(1280,720,"first",None,None)
if not window:
    glfw.terminate()
    raise Exception("glfw window cannot be crated")
glfw.set_window_pos(window,200,200)
glfw.make_context_current(window)

glClearColor(0,0.1,0.1,1)
glEnableClientState(GL_VERTEX_ARRAY)
glVertexPointer(3,GL_FLOAT,0,vertices)

while not glfw.window_should_close(window):
    glfw.poll_events()
    glClear(GL_COLOR_BUFFER_BIT)
    glDrawArrays(GL_TRIANGLES,0,3)
    glfw.swap_buffers(window)


glfw.terminate()
