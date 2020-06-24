import pygame

img = pygame.image.load("rip.png")
w, h = img.get_rect().size
img=pygame.transform.flip(img,False,True)
pygame.image.save(img,"rip.png")