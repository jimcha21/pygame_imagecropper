import pygame
import time
import numpy as np
import cv2
import sys
import os


if not len(sys.argv)==2:
    sys.exit("Give image input..")

filename = sys.argv[1]
print "creating /pos and /neg directories.."
os.system("mkdir pos")
os.system("mkdir neg")

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
save_btn = pygame.Rect(size[0]/2+size[0]/8, 10, size[0]/4, 20)
quit_btn = pygame.Rect(size[0]/2+size[0]/8, 40, size[0]/4, 20)
pos_btn = pygame.Rect(size[0]/2+size[0]/8, 70, size[0]/9, 20)
neg_btn = pygame.Rect(size[0]/2+size[0]/4, 70, size[0]/9, 20)
# p3_camera = pygame.Rect(0,img.shape[0],img.shape[1],img.shape[0])
# p4_camera = pygame.Rect(img.shape[1],img.shape[0],img.shape[1],img.shape[0])

screen = pygame.display.set_mode(size) 
c = pygame.time.Clock() # create a clock object for timing
saving_as='pos'

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
                    if saving_as=='pos':
                        pygame.draw.rect(img_surf, (0, 255, 0), rect_, 2)
                    else:
                        pygame.draw.rect(img_surf, (255, 0, 0), rect_, 2)
                    screen.blit(crop_surf,p2_camera,rect_)

            elif isinImage(save_btn,mouse_pos):
                forsave.blit(crop_surf,(0,0),rect_)
                pygame.image.save(forsave,saving_as+"/cropped_"+str(mouse_pos[0])+"_"+str(mouse_pos[1])+"_"+str(win_size[0])+"x"+str(win_size[1])+".jpg")
                #print "image saved at \'cropped_"+str(mouse_pos[0])+"_"+str(mouse_pos[1])+"_"+str(win_size[0])+"x"+str(win_size[1])+".jpg"
                textsurface = myfont.render('saved as'+saving_as+'..!', False, (0, 255, 0))
                screen.blit(textsurface,p2_camera)
            elif isinImage(pos_btn,mouse_pos):
                saving_as='pos'
            elif isinImage(neg_btn,mouse_pos):
                saving_as='neg'
            elif isinImage(quit_btn,mouse_pos):
                sys.exit("Exiting now..")

    screen.blit(img_surf,p1_camera)
    pygame.draw.rect(screen, [255, 0, 0], save_btn) # draw objects down here
    textsurface = myfont.render(' Save Image', False, (255, 255, 255))
    screen.blit(textsurface,save_btn)
    pygame.draw.rect(screen, [255, 0, 0], quit_btn)
    textsurface = myfont.render(' Quit', False, (255, 255, 255))
    screen.blit(textsurface,quit_btn)

    if saving_as=='pos':
        pygame.draw.rect(screen, [0, 125, 0], pos_btn)
    else:
        pygame.draw.rect(screen, [0, 0, 125], pos_btn)
    textsurface = myfont.render(' saving in \\pos', False, (255, 255, 255))
    screen.blit(textsurface,pos_btn)
    
    if saving_as=='neg':
        pygame.draw.rect(screen, [0, 125, 0], neg_btn)
    else:
        pygame.draw.rect(screen, [0, 0, 125], neg_btn)
    
    textsurface = myfont.render(' saving in \\neg', False, (255, 255, 255))
    screen.blit(textsurface,neg_btn)
    pygame.display.flip() # update the display
    c.tick(10) # only three images per second

# import pygame, pygame.font, pygame.event, pygame.draw, string
# from pygame.locals import *

# def get_key():
#   while 1:
#     event = pygame.event.poll()
#     if event.type == KEYDOWN:
#       return event.key
#     else:
#       pass

# def display_box(screen, message):
#   "Print a message in a box in the middle of the screen"
#   fontobject = pygame.font.Font(None,18)
#   pygame.draw.rect(screen, (0,0,0),
#                    ((screen.get_width() / 2) - 100,
#                     (screen.get_height() / 2) - 10,
#                     200,20), 0)
#   pygame.draw.rect(screen, (255,255,255),
#                    ((screen.get_width() / 2) - 102,
#                     (screen.get_height() / 2) - 12,
#                     204,24), 1)
#   if len(message) != 0:
#     screen.blit(fontobject.render(message, 1, (255,255,255)),
#                 ((screen.get_width() / 2) - 100, (screen.get_height() / 2) - 10))
#   pygame.display.flip()

# def ask(screen, question):
#   "ask(screen, question) -> answer"
#   pygame.font.init()
#   current_string = []
#   display_box(screen, question + ": " + string.join(current_string,""))
#   while 1:
#     inkey = get_key()
#     if inkey == K_BACKSPACE:
#       current_string = current_string[0:-1]
#     elif inkey == K_RETURN:
#       break
#     elif inkey == K_MINUS:
#       current_string.append("_")
#     elif inkey <= 127:
#       current_string.append(chr(inkey))
#     display_box(screen, question + ": " + string.join(current_string,""))
#   return string.join(current_string,"")

# def main():
#   screen = pygame.display.set_mode((320,240))
#   print ask(screen, "Name") + " was entered"

# if __name__ == '__main__': main()