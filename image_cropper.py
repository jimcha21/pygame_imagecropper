import pygame
import time
import numpy as np
import cv2
import sys
import os


if not len(sys.argv)==2:
    sys.exit("Give image input..")

filename = sys.argv[1]
label="pos"
os.system("mkdir "+label)
#todo pygame window will have input for window size.. also it will check for ascpect ratio ...
win_size=(64,128)

def getVarType(var):
    return type(var)

def isinImage(area,point):
    if (point[0]>=area[0] and point[0]<=area[0]+area[2])and(point[1]>=area[1] and point[1]<=area[1]+area[3]):
        return True

img = cv2.imread(filename,0)
pygame.init()
myfont = pygame.font.SysFont('Comic Sans MS', 25)
size=(img.shape[1]*2+20, img.shape[0]+20)
print "Image size "+str(img.shape)

if size[0]<win_size[0] or size[1]<win_size[1]:
    sys.exit("Too big window size..")
#else

canvas = pygame.Surface(size)
p1_camera = pygame.Rect(10,10,img.shape[1]+10, img.shape[0]+10)
p2_camera = pygame.Rect(img.shape[1]+(size[0]-img.shape[1])/2-win_size[0]/2,size[1]-win_size[1]-10,win_size[0],win_size[1])
popup= pygame.Rect(img.shape[1]+20,size[1]-win_size[1]-10,win_size[0],win_size[1])
save_btn = pygame.Rect(img.shape[1]+(size[0]-img.shape[1])/2-size[0]/8, 10, size[0]/4, 20)
quit_btn = pygame.Rect(img.shape[1]+(size[0]-img.shape[1])/2-size[0]/8, 40, size[0]/4, 20)
# p3_camera = pygame.Rect(0,img.shape[0],img.shape[1],img.shape[0])
# p4_camera = pygame.Rect(img.shape[1],img.shape[0],img.shape[1],img.shape[0])

screen = pygame.display.set_mode(size) 
c = pygame.time.Clock() # create a clock object for timing

while True:
    img_surf=pygame.image.load(filename)
    crop_surf=pygame.image.load(filename)

    forsave=pygame.Surface(win_size)
    for event in pygame.event.get():
        pressed=False #for saving on the mouse release
        if pygame.mouse.get_pressed()[0] or pygame.mouse.get_pressed()[2]:
            pressed=True
            mouse_pos=pygame.mouse.get_pos()
            if isinImage(p1_camera,mouse_pos):
                rect_topcorner=((mouse_pos[0]-10) - win_size[0]/2, (mouse_pos[1]-10) - win_size[1]/2)
                rect_=pygame.Rect(rect_topcorner[0],rect_topcorner[1],win_size[0],win_size[1])
                
                if isinImage(p1_camera,(rect_.left+10,rect_.top+10)) and isinImage(p1_camera,(rect_.left+10,rect_.bottom+10)) and isinImage(p1_camera,(rect_.right+10,rect_.top+10)) and isinImage(p1_camera,(rect_.right+10,rect_.bottom+10)):
                    pygame.draw.rect(img_surf, (0, 0, 255), rect_, 2)
                    screen.blit(crop_surf,p2_camera,rect_)

            elif isinImage(save_btn,mouse_pos):
                forsave.blit(crop_surf,(0,0),rect_)
                pygame.image.save(forsave,label+"/cropped_"+str(mouse_pos[0])+"_"+str(mouse_pos[1])+"_"+str(win_size[0])+"x"+str(win_size[1])+".jpg")
                #print "image saved at \'cropped_"+str(mouse_pos[0])+"_"+str(mouse_pos[1])+"_"+str(win_size[0])+"x"+str(win_size[1])+".jpg"
                textsurface = myfont.render('saved..!', False, (0, 255, 0))
                screen.blit(textsurface,p2_camera)
            elif isinImage(quit_btn,mouse_pos):
                sys.exit("Exiting now..")

    screen.blit(img_surf,p1_camera)
    pygame.draw.rect(screen, [255, 0, 0], save_btn) # draw objects down here
    textsurface = myfont.render('Save Image', False, (255, 255, 255))
    screen.blit(textsurface,save_btn)
    pygame.draw.rect(screen, [255, 0, 0], quit_btn)
    textsurface = myfont.render('Quit', False, (255, 255, 255))
    screen.blit(textsurface,quit_btn)
    pygame.display.flip() # update the display
    c.tick(10) # only three images per second

