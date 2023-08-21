'''
Created on May 1, 2023
Created with the help of the official PyGame Documentation
@author: johnbotonakis
'''
import pygame
from Settings import ACC,WIDTH,FRIC,HEIGHT,FPS
import random
vec = pygame.math.Vector2        # This makes the game 2 Dimensional

class Player(pygame.sprite.Sprite):     # The Main Player Class
    def __init__(self):

        super().__init__()                                            # Initialize from the parent class Sprite
        self.image = pygame.image.load(f"./img/P1.png")                # The size of the player model
        self.surf = pygame.transform.scale(self.image,(40,50))
        self.jumping = False
        self.rect = self.surf.get_rect(center = (10, 420))  # Make the player a rectangle, and place at the provided coords
        self.score = 0
        self.pos = vec((10, 700))   # Position on screen
        self.vel = vec(0,0)         # Velocity or how fast Player ramps up while moving
        self.acc = vec(0,0)         # Acceleration or how fast the Player moves (Horizontal acceleration,Vertical Acceleration)
    
    #MOVEMENT
    def move(self):
        self.acc = vec(0,1)                         # Reset the acceleration 
        pressed_keys = pygame.key.get_pressed()     # If any keys are pressed, store them as a variable
        if pressed_keys[pygame.K_a]:                # If the key pressed is an "A"
            self.acc.x = -ACC                       # Set the Player acceleration negative
            self.image = pygame.image.load("./img/P1.png")                # The size of the player model
            self.surf = pygame.transform.flip(self.image, True, False)
            self.surf = pygame.transform.scale(self.surf,(40,50))
        if pressed_keys[pygame.K_d]:                # If the key pressed is a "D"
            self.image = pygame.image.load("./img/P1.png")                # The size of the player model
            self.surf = pygame.transform.scale(self.image,(40,50))
            self.acc.x = ACC                        # Set the Player acceleration positive
        
        self.acc.x += self.vel.x * FRIC             # Formula to find the speed (Acceleration + (Velocity times Friction))
        self.vel += self.acc                        # Formula to ramp up velocity
        self.pos += self.vel + 0.5 * self.acc       # Formula to move the Player position
        if self.pos.x > WIDTH:                      # If the player X position is higher than the width of the screen, 
            self.pos.x = 0                          # Set it back to the 0 coordinate at the other end of the screen
        if self.pos.x < 0:                          # If the player X position is lower than the width of the screen,
            self.pos.x = WIDTH                      # Set it forward to the final coordinate at the other end of the screen
        self.rect.midbottom = self.pos
    
    #RESET
    def reset(self):
        self.rect = self.surf.get_rect(center = (10,420))   # Make the player, and place at the provided coords
        self.score = 0                                      # Set the player score 
        self.pos = vec((500, 200))                          # Position on screen
        self.vel = vec(0,0)                                 # Velocity or how fast Player ramps up while moving
        self.acc = vec(0,0)                                 # Acceleration or how fast the Player moves (Horizontal acceleration,Vertical Acceleration)
    
    #UPDATE FUNCTION
    def update(self):                                                   
        hits = pygame.sprite.spritecollide(P1 , platforms, False)       # This will recognize if two sprites collide
        if self.vel.y >0:                                               # If the Player's Y velocity is greater than 0
            if hits:                                                    # And if two sprites register a hit,
                if self.pos.y < hits[0].rect.bottom:                    # AND if the Player's Y position is bigger than where the hit occurred
                    if hits[0].point == True:                           # If the object that was hit has it's points set to True
                        hits[0].point = False                           # Set the object to False, so it can't be re hit for extra points
                        self.score += 1                                 # Increase the player score
                    if hits[0].sand == True:
                        self.vel.x =-.3
                    self.pos.y = hits[0].rect.top +1                    # Set the Y position to where the hit occurred plus 1 (for a buffer)
                    self.vel.y = 0                                      # Set the Y Velocity to 0
                    self.jumping = False                                # Allow the Player to Jump again
    # JUMPING    
    def jump(self):
        hits = pygame.sprite.spritecollide(self, platforms, False)      # Checks to see if the Player is on a sprite (Can't jump without a platform!)
        if hits and not self.jumping:                                   # If standing on something, and not jumping,
            self.jumping=True                                           # Set Jumping to true
            self.image = pygame.image.load("./img/jump.png")            # Change the sprite to the jumping sprite
            self.surf = pygame.transform.scale(self.image,(40,50))      # Transform the image to the appropriate size
            self.vel.y = -25                                            # Ascend
    # CANCEL JUMP / MID AIR
    def canceljump(self):                                               
        if self.jumping:                                                # If actively in the air,
            self.vel.y=-5                                               # Set the Y velocity to negative 5 (bring back down to earth)
            self.jumping = False                                        # Allow to jump again
            self.image = pygame.image.load("./img/P1.png")              # Change the sprite back to the normal sprite
            self.surf = pygame.transform.scale(self.image,(40,50))      # Transform to the image to the appropriate size
 
 #MAIN PLATFORM CLASS
class platform(pygame.sprite.Sprite):                                       
    def __init__(self):
        super().__init__()                                          # Initialize this class from the parent class Sprite
        self.image = pygame.image.load("./img/PT1.png")             # Load the platform image
        self.surf = pygame.transform.scale(self.image,(100,20))     # Transform the image to the appropriate size
        self.rect = self.surf.get_rect(center = (random.randint(100,WIDTH-600),random.randint(200, 700)))     
        #^^Generate a random point and, from that, generate a width and height outwards^^#
        self.point= True                                            # Set the condition for points to be True  
        self.sand = False

class sand_platform(platform):
    def __init__(self):
        super().__init__()                                                  # Initialize this class from the parent class Sprite
        self.image = pygame.image.load("./img/PT2.png")                     # Load the Sand Platform image
        self.surf = pygame.transform.scale(self.image,(100,20))             # Transform the image to the appropriate size
        self.rect = self.surf.get_rect(center = (WIDTH/2, HEIGHT - 10))     # The platform model, placed at the provided coords
        self.point= True                                                    # Set the condition for points to be True 
        self.sand = True                                                    # Set the Sand condition to True

        
PT1 = platform()                    # Instantiate a platform
PT1.point = False                   # Set the starting platform's points to be false
P1 = Player()                       # Instantiate a Player
platforms = pygame.sprite.Group()   # Create a group for all available sprites
platforms.add(PT1)                  # Add Platform