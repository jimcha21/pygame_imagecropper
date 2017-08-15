import pygame, pygame.font, pygame.event, pygame.draw, string
from pygame.locals import *
import time
import numpy as np
import cv2
import sys
import os


def get_key():
  while 1:
    event = pygame.event.poll()
    if event.type == KEYDOWN:
      return event.key
    else:
      pass

def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def getVarType(var):
    return type(var)

def isinArea(area,point):
    if (point[0]>=area[0] and point[0]<=area[0]+area[2])and(point[1]>=area[1] and point[1]<=area[1]+area[3]):
        return True

def main():

    if not len(sys.argv)==2:
        sys.exit("Give image input..")

    filename = sys.argv[1]
    print "creating /pos and /neg directories.."
    os.system("mkdir pos")
    os.system("mkdir neg")

    #init.
    win_size=(64,128)

    img = cv2.imread(filename,0)
    pygame.init()
    myfont = pygame.font.SysFont('Comic Sans MS', 25)
    size=(img.shape[1]*2+20, img.shape[0]+20)
    print "Given image size "+str(img.shape)

    if size[0]<win_size[0] or size[1]<win_size[1]:
        sys.exit("Too big window size..")
    #else

    canvas = pygame.Surface(size)
    img_area = pygame.Rect(10,10,img.shape[1]+10, img.shape[0]+10)
    #cropped_area = pygame.Rect(img.shape[1]+(size[0]-img.shape[1])/2-win_size[0]/2,size[1]-win_size[1]-10,win_size[0],win_size[1])
    cropped_area = pygame.Rect(size[0]/2+size[0]/4-win_size[0]/2,size[1]-win_size[1]-10,win_size[0],win_size[1])

    save_btn    = pygame.Rect(size[0]/2+size[0]/8, size[1]/50, size[0]/4, size[1]/20)
    quit_btn    = pygame.Rect(size[0]/2+size[0]/8, save_btn[1]+size[1]/17, size[0]/4, size[1]/20)
    pos_btn     = pygame.Rect(size[0]/2+size[0]/8, quit_btn[1]+size[1]/17, size[0]/9, size[1]/20)
    neg_btn     = pygame.Rect(size[0]/2+size[0]/4, quit_btn[1]+size[1]/17, size[0]/9, size[1]/20)
    width_fld   = pygame.Rect(size[0]/2+size[0]/8, pos_btn[1]+size[1]/17, size[0]/9, size[1]/20)
    height_fld  = pygame.Rect(size[0]/2+size[0]/4, pos_btn[1]+size[1]/17, size[0]/9, size[1]/20)

    screen = pygame.display.set_mode(size) 

    c = pygame.time.Clock() # create a clock object for timing
    saving_as='pos'

    while True:
        img_surf=pygame.image.load(filename)
        crop_surf=pygame.image.load(filename)    
        #print ask(screen, "Name") + " was entered"
        forsave=pygame.Surface(win_size)
        for event in pygame.event.get():
            pressed=False #for saving on the mouse release
            if pygame.mouse.get_pressed()[0] or pygame.mouse.get_pressed()[2]:
                pressed=True
                mouse_pos=pygame.mouse.get_pos()
                if isinArea(img_area,mouse_pos):
                    rect_topcorner=((mouse_pos[0]-10) - win_size[0]/2, (mouse_pos[1]-10) - win_size[1]/2)
                    rect_=pygame.Rect(rect_topcorner[0],rect_topcorner[1],win_size[0],win_size[1])
                    
                    if isinArea(img_area,(rect_.left+10,rect_.top+10)) and isinArea(img_area,(rect_.left+10,rect_.bottom+10)) and isinArea(img_area,(rect_.right+10,rect_.top+10)) and isinArea(img_area,(rect_.right+10,rect_.bottom+10)):
                        if saving_as=='pos':
                            pygame.draw.rect(img_surf, (0, 255, 0), rect_, 2)
                        else:
                            pygame.draw.rect(img_surf, (255, 0, 0), rect_, 2)
                        screen.blit(crop_surf,cropped_area,rect_)

                elif isinArea(save_btn,mouse_pos):
                    forsave.blit(crop_surf,(0,0),rect_)
                    pygame.image.save(forsave,saving_as+"/cropped_"+str(mouse_pos[0])+"_"+str(mouse_pos[1])+"_"+str(win_size[0])+"x"+str(win_size[1])+".jpg")
                    #print "image saved at \'cropped_"+str(mouse_pos[0])+"_"+str(mouse_pos[1])+"_"+str(win_size[0])+"x"+str(win_size[1])+".jpg"
                    if saving_as=='pos':
                        textsurface = myfont.render('saved..!', False, (0, 255, 0))
                    else:
                        textsurface = myfont.render('saved..!', False, (255, 0, 0))
                    screen.blit(textsurface,cropped_area)
                elif isinArea(pos_btn,mouse_pos):
                    saving_as='pos'
                elif isinArea(neg_btn,mouse_pos):
                    saving_as='neg'
                elif isinArea(width_fld,mouse_pos):
                    pygame.draw.rect(screen, [0, 0, 150], width_fld)
                    pygame.display.flip()
                    current_string = []
                    while 1:
                        inkey = get_key()
                        if inkey == K_BACKSPACE:
                            current_string = current_string[0:-1]
                            pygame.draw.rect(screen, [0, 0, 150], width_fld)
                        elif inkey == K_RETURN:
                            break
                        elif inkey == K_MINUS:
                            current_string.append("_")
                        elif inkey <= 127:
                            current_string.append(chr(inkey))             

                        textsurface = myfont.render(string.join(current_string,""), False, (255, 255, 255))
                        screen.blit(textsurface,width_fld)
                        pygame.display.flip()

                    if RepresentsInt(string.join(current_string,"")):                    
                        width=int(string.join(current_string,""))
                        if(width>size[0]/2):
                            print "Too big width value!.."
                        else:
                            win_size=(width,win_size[1])
                            #clear the cropped area, before resizing
                            pygame.draw.rect(screen, [0, 0, 0], cropped_area)
                            cropped_area = pygame.Rect(size[0]/2+size[0]/4-win_size[0]/2,size[1]-win_size[1]-10,win_size[0],win_size[1])
                    else:
                        print 'Please enter an integer value...'

                elif isinArea(height_fld,mouse_pos):
                    pygame.draw.rect(screen, [0, 0, 150], height_fld)
                    pygame.display.flip()
                    current_string = []
                    while 1:
                        inkey = get_key()
                        if inkey == K_BACKSPACE:
                            current_string = current_string[0:-1]
                            pygame.draw.rect(screen, [0, 0, 150], height_fld)
                        elif inkey == K_RETURN:
                            break
                        elif inkey == K_MINUS:
                            current_string.append("_")
                        elif inkey <= 127:
                            current_string.append(chr(inkey))             

                        textsurface = myfont.render(string.join(current_string,""), False, (255, 255, 255))
                        screen.blit(textsurface,height_fld)
                        pygame.display.flip()

                    if RepresentsInt(string.join(current_string,"")):                    
                        height=int(string.join(current_string,""))
                        if(height>2*size[1]/3):
                            print "Too big height value!.."
                        else:
                            win_size=(win_size[0],height)
                            #clear the cropped area, before resizing
                            pygame.draw.rect(screen, [0, 0, 0], cropped_area)
                            cropped_area = pygame.Rect(size[0]/2+size[0]/4-win_size[0]/2,size[1]-win_size[1]-10,win_size[0],win_size[1])
                    else:
                        print 'Please enter an integer value...'

                elif isinArea(quit_btn,mouse_pos):
                    sys.exit("Exiting now..")
        
        pygame.draw.rect(screen, [0, 0, 150], width_fld)
        textsurface = myfont.render(' Change width ['+str(win_size[0])+'px]', False, (255, 255, 255))
        screen.blit(textsurface,width_fld)

        pygame.draw.rect(screen, [0, 0, 150], height_fld)
        textsurface = myfont.render(' Change height ['+str(win_size[1])+'px]', False, (255, 255, 255))
        screen.blit(textsurface,height_fld)

        pygame.draw.rect(screen, [255, 0, 0], save_btn) # draw objects down here
        textsurface = myfont.render(' Save Image ['+str(win_size[0])+'x'+str(win_size[1])+'px]', False, (255, 255, 255))
        screen.blit(textsurface,save_btn)

        pygame.draw.rect(screen, [255, 0, 0], quit_btn)
        textsurface = myfont.render(' Quit', False, (255, 255, 255))
        screen.blit(textsurface,quit_btn)

        if saving_as=='pos':
            pygame.draw.rect(screen, [0, 200, 0], pos_btn)
        else:
            pygame.draw.rect(screen, [125, 125, 125], pos_btn)
        textsurface = myfont.render(' saving in /pos', False, (255, 255, 255))
        screen.blit(textsurface,pos_btn)
        
        if saving_as=='neg':
            pygame.draw.rect(screen, [0, 200, 0], neg_btn)
        else:
            pygame.draw.rect(screen, [125, 125, 125], neg_btn)
        
        textsurface = myfont.render(' saving in /neg', False, (255, 255, 255))
        screen.blit(textsurface,neg_btn)

        screen.blit(img_surf,img_area)
        pygame.display.flip() # update the display
        c.tick(10) # only three images per second


if __name__ == "__main__":
    main()