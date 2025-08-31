# -*- coding: utf-8 -*-
"""
Created on Mon Jul 21 19:33:30 2025

@author: sasha
"""

import math
import pygame

pygame.init()
WIDTH,HEIGHT = 800,600

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Planet Simulation')
clock =pygame.time.Clock()

G=  6.67430e-11
Echelle = 6e-11
Echelle_zoomee= 1e-9
DT = 86400
zoome = False

class Body:
    def __init__(self,x,y,vx,vy,mass,radius,color):
        self.x=x
        self.y=y
        self.vx=vx
        self.vy=vy
        self.mass = mass
        self.radius = radius
        self.color = color
        self.trail=[]
        
    def update_position(self,bodies):
        fx = fy = 0
        for other in bodies :
            if other != self :
                dx = other.x - self.x
                dy= other.y -self.y
                r = math.sqrt(dx**2 + dy**2)
                if r>0 :
                    f= G*self.mass * other.mass/(r**2)
                    fx += f*dx / r
                    fy += f*dy/r
        ax = fx / self.mass
        ay = fy / self.mass
        self.vx += ax * DT
        self.vy += ay * DT
        self.x += self.vx*DT
        self.y += self.vy*DT
        
        current_scale = Echelle_zoomee if zoome else Echelle
        self.trail.append((int(self.x * current_scale + WIDTH//2 ), int(self.y*current_scale +HEIGHT//2)))
        if len(self.trail)>200 :
            self.trail.pop(0)
            
    def draw(self,screen):
        if len(self.trail)>1 :
            pygame.draw.lines(screen, (50,50,50),False,self.trail,1)
            
        current_scale = Echelle_zoomee if zoome else Echelle
        
        screen_x = int(self.x* current_scale + WIDTH//2)
        screen_y = int(self.y* current_scale + HEIGHT//2)
        
        pygame.draw.circle(screen, self.color, (screen_x,screen_y), self.radius)
        
        
bodies = [
    Body(0,0,0,0,1.989e30,8,(255,255,0)),
    Body(5.79e10, 0, 0, 47360, 3.301e23, 2, (169, 169, 169)), #Mercure

    
    
    
    
    
    ]
