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

#-------------------------------------------#
class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y, r, earth_r):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.r = r
        self.draw_width = 4
        self.earth_r = earth_r
    def draw(self):
        pygame.draw.circle(Surface, BLACK, ConvertCoord(self.x,self.y), self.r, self.draw_width)
    
class Planet(pygame.sprite.Sprite):
    def __init__(self, x, y, r, rotation, line_length):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.r = r
        self.rotangle = rotation
        self.line_length = line_length
        self.draw_width = 10
    def draw(self):
        pygame.draw.circle(Surface, BLACK, ConvertCoord(self.x,self.y), self.r, self.draw_width)
    def lines(self, num_lines):
        total_degrees = 360.0
        section_degrees = total_degrees/num_lines
        for n in range(num_lines):
            x = self.r * math.cos( DegtoRad(self.rotangle + n*section_degrees) )
            y = self.r * math.sin( DegtoRad(self.rotangle + n*section_degrees) )
            x2 = (self.r+self.line_length) * math.cos( DegtoRad(self.rotangle + n*section_degrees) )
            y2 = (self.r+self.line_length) * math.sin( DegtoRad(self.rotangle + n*section_degrees) )
            self.draw_lines(ConvertCoord(x,y),ConvertCoord(x2,y2))
            
    def draw_lines(self, p1, p2):
        pygame.draw.line(Surface, BLACK, p1, p2, self.draw_width)
        
    def incrementAngle(self, angle):
        self.rotangle+=angle
#---Initialize objects---#
planet_radius = 140
ball_radius = 20
earth = Planet(0,0, planet_radius,0, 55)
ball1 = Ball(planet_radius + ball_radius, 0, ball_radius)

while True:
    Surface.fill(BGCOLOR)
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()
#--drawings--#
    #earth.lines(5)
    earth.draw()
    ball1.draw()
#------------#


#----Calculations---#
    #earth.incrementAngle(0.05)
    
    pygame.display.update()
