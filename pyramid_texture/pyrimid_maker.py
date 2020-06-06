from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL import shaders
import numpy as np
import pyrr
from PIL import Image
import pygame

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


x = 1377
y = 567
sx1 = 497 / x
sy1 = 118 / y
sx2 = 348 / x
sy2 = 324 / y
sx3 = 677 / x
sy3 = 315 / y
sx4 = 663 / x
sy4 = 108 / y

tx1 = 241 / x
ty1 = 124 / y
tx2 = 131 / x
ty2 = 315 / y
tx3 = 353 / x
ty3 = 313 / y

pyramid = [-1.0, 0.0, 1.0, sx1, sy1,
           1.0, 0.0, 1.0, sx2, sy2,
           1.0, 0.0, -1.0, sx3, sy3,
           -1.0, 0.0, -1.0, sx4, sy4,

           1.0, 0.0, 1.0, tx1, ty1,
           1.0, 0.0, -1.0, tx2, ty2,
           0.0, 1, 0.0, tx3, ty3,

           1.0, 0.0, -1.0, tx1, ty1,
           -1.0, 0.0, -1.0, tx2, ty2,
           0.0, 1, 0.0, tx3, ty3,

           -1.0, 0.0, -1.0, tx1, ty1,
           -1.0, 0.0, 1.0, tx2, ty2,
           0.0, 1, 0.0, tx3, ty3,

           -1.0, 0.0, 1.0, tx1, ty1,
           1.0, 0.0, 1.0, tx2, ty2,
           0.0, 1, 0.0, tx3, ty3

           ]

i = [0, 1, 2, 2, 3, 0,
     4, 5, 6,
     7, 8, 9,
     10, 11, 12,
     13, 14, 15
     ]

v = np.array(pyramid, dtype=np.float32)
i = np.array(i, dtype=np.uint32)

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

texture = glGenTextures(1)
glBindTexture(GL_TEXTURE_2D, texture)

glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

img = pygame.image.load("together.png")
w, h = img.get_rect().size
img_data = pygame.image.tostring(img, "RGBA")
glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)

glUseProgram(shader)
glClearColor(0, 0.1, 0.1, 1)
glEnable(GL_DEPTH_TEST)
##glEnable(GL_BLEND)
##glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)


model_loc = glGetUniformLocation(shader, "model")
proj_loc = glGetUniformLocation(shader, "projection")

projection = pyrr.matrix44.create_perspective_projection_matrix(45, 1280 / 720, 0.1,
                                                                50)  # field_of_view,aspect_ration,nearclippingplane,farclipping,plane

glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)
translation = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, -5]))

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.VIDEORESIZE:
            glViewport(0, 0, event.w, event.h)
    ct = pygame.time.get_ticks() / 1000
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    rot_x = pyrr.Matrix44.from_x_rotation(0.5 * ct)
    rot_y = pyrr.Matrix44.from_y_rotation(0.5 * ct)
    rotation = pyrr.matrix44.multiply(rot_x, rot_y)
    model = pyrr.matrix44.multiply(rotation, translation)

    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
    # glDrawArrays(GL_TRIANGLE_STRIP,0,4)
    glDrawElements(GL_TRIANGLES, len(i), GL_UNSIGNED_INT, None)

    pygame.display.flip()