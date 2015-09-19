import pygame
from pygame.locals import *
import sys
import time
import math
import pyganim

pygame.init()


#--------Variable Declarations--------------#

MAX_X = 800
MAX_Y = 640
  
# set up the colors
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)
mainClock = pygame.time.Clock()
BGCOLOR = (100, 50, 50)

Surface = pygame.display.set_mode((MAX_X, MAX_Y))
pygame.display.set_caption('Planet Vortex')
line_coords = [ [[0,0],[0,0]] , [[0,0],[0,0]] , [[0,0],[0,0]] , [[0,0],[0,0]] , [[0,0],[0,0]] ]
#-------------------------------------------#


#---------Helper Functions -----------------#
def DegtoRad(angle):
    return angle/180.0*math.pi
def ConvertCoord(x,y):
    return [x+400, -1*y +320]
def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image
def mag(x,y):
    return math.sqrt(x*x+y*y)
#-------------------------------------------#
class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y, r, angle):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.r = r
        self.angle = angle
        self.draw_width = 4
    def draw(self):
        pygame.draw.circle(Surface, BLACK, ConvertCoord((int)(self.x),(int)(self.y)), self.r, self.draw_width)
    def boundary(self, earth_radius):
        cur_r = mag(self.x,self.y)
        if( cur_r< earth_radius+self.r):
            self.x = self.x/cur_r *(self.r+earth_radius)
            self.y = self.y/cur_r *(self.r+earth_radius)

        
class Planet(pygame.sprite.Sprite):
    def __init__(self, x, y, r, rotation, line_length, speed, accel):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.r = r
        self.rotangle = rotation
        self.line_length = line_length
        self.draw_width = 10
        self.speed = speed
        self.accel = accel
    def draw(self):
        pygame.draw.circle(Surface, BLACK, ConvertCoord(self.x,self.y), self.r, self.draw_width)
    def lines(self, num_lines):
        total_degrees = 360.0
        section_degrees = total_degrees/num_lines
        for n in range(num_lines):
            line_coords[n][0][0]= self.r * math.cos( DegtoRad(self.rotangle + n*section_degrees) )
            line_coords[n][0][1] = self.r * math.sin( DegtoRad(self.rotangle + n*section_degrees) )
            line_coords[n][1][0] = (self.r+self.line_length) * math.cos( DegtoRad(self.rotangle + n*section_degrees) )
            line_coords[n][1][1] = (self.r+self.line_length) * math.sin( DegtoRad(self.rotangle + n*section_degrees) )
            self.draw_lines(ConvertCoord(line_coords[n][0][0],line_coords[n][0][1]),ConvertCoord(line_coords[n][1][0],line_coords[n][1][1]))
            
    def draw_lines(self, p1, p2):
        pygame.draw.line(Surface, BLACK, p1, p2, self.draw_width)
    def rotation(self, slow_constant):
        key=pygame.key.get_pressed()
        print self.speed
        if(abs(self.accel)<0.05):
            if(key[K_RIGHT]):
                self.accel-=0.005
            elif(key[K_LEFT]):
                self.accel+=0.005
        self.speed = self.speed/slow_constant
        self.accel = self.accel/slow_constant
        if((self.speed>-0.5 and self.accel<0) or (self.speed<0.5 and self.accel>0)):
            self.speed+=self.accel
        self.incrementAngle(self.speed)

    def incrementAngle(self, angle):
        self.rotangle+=angle
#---Initialize objects---#
planet_radius = 140
ball_radius = 20
earth = Planet(0,0, planet_radius,0, 55, 0,0)
ball1 = Ball(planet_radius + ball_radius, 0, ball_radius, 0)

while True:
    Surface.fill(BGCOLOR)
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()
#--drawings--#
    earth.lines(5)
    earth.draw()
    ball1.draw()
#------------#
    

#----Calculations---#
    earth.rotation(1.012)
    ball1.x = pygame.mouse.get_pos()[0]-400
    ball1.y = -1*(pygame.mouse.get_pos()[1]-320)
    ball1.boundary(earth.r)
    pygame.display.update()
