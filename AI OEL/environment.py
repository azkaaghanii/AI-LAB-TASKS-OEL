# Space Discover: Genetic Algorithms - Environment File 

import numpy as np
import pygame as pg

# Represents a city in the environment.
class City():
    def __init__(self, pos, color):
        self.pos = pos
        self.color = color

class Environment():
    # Represents the entire environment (screen, cities, connections, rocket).
    def __init__(self):
        
        self.width = 600
        self.height = 600
        self.cityRadius = 10
        
        self.cities = list()

        # Tracks paths (connections) between cities
        self.connections = list()
        
        # Creates a pygame screen object with specified dimensions.
        self.screen = pg.display.set_mode((self.width, self.height))
        
        self.origSpriteRocket = pg.image.load('rocket.png')

        # The rocket image (may be rotated later).
        self.spriteRocket = self.origSpriteRocket

        # Dimensions of the rocket.
        self.rocketWidth = self.spriteRocket.get_rect().size[0]
        self.rocketHeight = self.spriteRocket.get_rect().size[1]
        self.rotation = 0
        
        self.spriteBackground = pg.image.load('space.jpg')
        self.spriteBackground = pg.transform.smoothscale(self.spriteBackground, (self.width, self.height))
        
        # Speed of movement
        self.rocketSpeed = 10

        # Starting position (off-screen at [-50, -50])
        self.rocketPos = [-50] * 2
        
        # Tracks the current city the rocket is on
        self.currentPos = 0
        
        self.drawScreen('none')
        self.edit()
        
        # This function updates the visual display
    def drawScreen(self, view):

        # Clears the screen (black) and redraws the background
        self.screen.fill((0, 0, 0)) 
        self.screen.blit(self.spriteBackground, (0,0))
        
        # In "normal" mode, it draws all connections between cities in yellow
        if view == 'normal':
            for i in range(0, len(self.connections)):
                pg.draw.line(self.screen, (255, 255, 0), self.connections[i][0], self.connections[i][1], 3)

        # In "beautiful" mode, only shows partial connections for animation.
        elif view == 'beautiful':
            for i in range(0, len(self.connections) - 1):
                pg.draw.line(self.screen, (255, 255, 0), self.connections[i][0], self.connections[i][1], 3)
        
        if len(self.cities) > 0 and self.rocketPos[0] > 0 and view == 'beautiful':
           pg.draw.line(self.screen, (255, 255, 0), (self.cities[self.currentPos].pos[0], self.cities[self.currentPos].pos[1]), (self.rocketPos[0], self.rocketPos[1]), 3)
        
        # Draws each city as a colored circle.
        for city in self.cities:
            pg.draw.circle(self.screen, city.color, city.pos, self.cityRadius)
    
        # Places the rocket at its current position and updates the screen.
        self.screen.blit(self.spriteRocket, (self.rocketPos[0] - self.rocketWidth/2, self.rocketPos[1] - self.rocketHeight/2))
        pg.display.flip()
        
    # Allows users to add cities interactively.   
    def edit(self):
        while True:
            # Gets mouse position and listens for user actions.
            position = pg.mouse.get_pos()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()

            # Adds a new city where the mouse is clicked, with a random color
                elif event.type == pg.MOUSEBUTTONDOWN:
                    color = (np.random.randint(0, 256), np.random.randint(0, 256), np.random.randint(0, 256))
                    city = City(position, color)
                    self.cities.append(city)

            # Ends the editing mode if the user presses Enter
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        return
                    
            self.drawScreen('none')
    
    # Rotates the rocket image around its center to match its direction.
    def rotateCenter(self, sprite, angle):
        spriteRect = sprite.get_rect() 
        rotSprite = pg.transform.rotate(sprite, angle) 
        spriteRect.center = rotSprite.get_rect().center 
        rotSprite = rotSprite.subsurface(spriteRect)
        return rotSprite
    
    # Simulates moving the rocket from one city to another.
    def step(self, action, view):
        
        # Gets coordinates of the current and target cities and calculates the Euclidean distance between them.
        c1X = self.cities[self.currentPos].pos[0]
        c1Y = self.cities[self.currentPos].pos[1]
        c2X = self.cities[action].pos[0]
        c2Y = self.cities[action].pos[1]
        distance = pow(pow(c1X - c2X, 2) + pow(c1Y - c2Y, 2), 0.5)
        
        if view == 'normal' or view == 'beautiful':
            self.connections.append([(c1X, c1Y), (c2X, c2Y)])
            self.drawScreen(view)
            
            
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
        
        
        if view == 'beautiful':
            reached = False
            self.rocketPos[0] = c1X
            self.rocketPos[1] = c1Y
            diffX = c1X - c2X
            diffY = c1Y - c2Y
            t = diffY/(diffX + 1e-12)
            x = pow(pow(self.rocketSpeed, 2) / (pow(t, 2) + 1), 0.5)
            y = x * abs(t) 
            if diffY > 0:
                y = -y
            if diffX > 0:
                x = -x
            
            if (x <= 0 and y <= 0) or (x <= 0 and y >= 0):
                angle = np.rad2deg(np.arctan(-t) + np.pi/2)
            else:
                angle = np.rad2deg(np.arctan(-t) - np.pi/2)
            
            if diffX == 0:
                angle += 180
                
            
            self.spriteRocket = self.origSpriteRocket
            self.spriteRocket = self.rotateCenter(self.spriteRocket, angle)
            
            
            while not reached:
                self.rocketPos[0] += x
                self.rocketPos[1] += y
                distance = pow(pow(self.rocketPos[0] - c2X, 2) + pow(self.rocketPos[1] - c2Y, 2), 0.5)
                if distance < self.cityRadius or (diffX == 0 and diffY == 0):
                    self.rocketPos[0] = c2X
                    self.rocketPos[1] = c2Y
                    reached = True
                pg.time.wait(50)
                self.drawScreen(view)
        
        self.currentPos = action
        
        return distance
    
    def reset(self):
        self.connections.clear()
        self.currentPos = 0
        self.rocketPos = [-50] * 2
        
        
if __name__ == '__main__': 
    env = Environment()
