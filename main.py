'''
Created on May 1, 2023
Created with the help of the ****Official PyGame Documentation****
@author: johnbotonakis
'''

import pygame
from pygame.locals import *
from Classes import *
import sys
import Settings
import random
import time

class MAIN():
    def __init__(self):
        pygame.init()                                                    # Initialize PyGame
        self.vec = pygame.math.Vector2                                   # Store the PyGame Vector (2 for two dimensional) as a variable "vec"
        self.FramePerSec = pygame.time.Clock()                           # Keeping track of clock time, as a variable
        self.game_state = "start"                                        # Set the Game State as Start
        self.displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))   # Display the window using the given height
        pygame.display.set_caption("Jump!")                              # Set the title of the window
        self.all_sprites = pygame.sprite.Group()                         # Collect each grouped Sprite class instance as a single variable

    #INITIALIZATION
    def InI(self):
        #ADDING THE SPRITES INTO SPRITE GROUPS
        self.all_sprites.add(PT1)                                        # Add the Starting Platform
        self.all_sprites.add(P1)                                         # Add Player 1
        PT1.surf = pygame.Surface((WIDTH, 20))                           # This draws the flat platform that was the first instance of PT1
        PT1.surf.fill("black")                                           # Color the surface BLACK
        PT1.rect = PT1.surf.get_rect(center = (WIDTH/2, HEIGHT - 10))    # Set it to the bottom of the screen
        self.bg = pygame.image.load("./img/bg.png")                      # Create a variable for the background image
       
        
        #BUILDING THE LEVEL
        for x in range(random.randint(4,11)):        # For a number between 4 and 11,
            self.pl = platform()                     # Create an instance of a platform
            platforms.add(self.pl)                   # Add those platforms to the platform variable
            self.all_sprites.add(self.pl)            # Add in those platforms to the sprite variable
            self.spl=sand_platform()                 # Create an instance of a sand platform
            platforms.add(self.spl)                  # Add the sand platforms to the platform variable
            self.all_sprites.add(self.spl)           # Add in the sand platforms to the sprite variable
        
    #PLATFORM CHECK
    def check(self,platform,group):                                                  
        if pygame.sprite.spritecollideany(platform, group):                # If PyGame registers the platform colliding with anything,
            return True                                                    # Return True
        else:                                                              # Otherwise,
            for E in group:                                                # For an entity in the provided group
                if E in platforms:                                         # If that entity is in the platform group
                    continue                                               # Continue to the next instruction
                if (abs(platform.rect.top - E.rect.bottom) < 105):         # If the absolute position of the top of the platform minus the bottom of the new entity is less than 30,
                    if (abs(platform.rect.bottom - E.rect.top) < 105):     # And if the absolute position of the bottom of the platform and top of the entity is less than 30,
                        return True                                        # Return True
                return False                                               # Otherwise, if no other condition is met, return False
    
    #GENERATING A LEVEL
    def plat_gen(self): 
            while len(platforms) < 10:                                                                      # While the amount of platforms is <10
                J = random.randint(0,100)
                if J <=90:
                    width = random.randrange(5,25)                                                          # Choose a random number and save it as a width
                    p  = platform()                                                                         # Instantiate a base platform, which serves as the first entry into the platform group
                    C = True                                                                                # This is the check, and it returns True to start the While loop
                    while C:                                                                                # While the Check is running,
                        p  = platform()                                                                     # Instantiate a platform, and save it as p
                        p.rect.center = (random.randrange(0, WIDTH - width*2),random.randrange(100,350))    # Set the platform to the specified coordinates
                        C = self.check(p, platforms)                                                        # Use the check function to see if it can be placed on the screen
                    platforms.add(p)                                                                        # Add the new platform to the platform group
                    self.all_sprites.add(p)                                                                 # Add the new platform to the sprite group
                if J >=91:                                                                    # While the amount of platforms is less than 11,
                    width = random.randrange(5,25)                                            # Choose a random number and save it as a width
                    p  = platform()                                                           # Instantiate a base platform, which serves as the first entry into the platform group
                    C = True                                                                  # This is the check, and it returns True to start the While loop
                    while C:                                                                                # While the Check is running,
                        p  = sand_platform()                                                                # Instantiate a platform, and save it as p
                        p.rect.center = (random.randrange(-5, WIDTH - width*2),random.randrange(100,150))   # Set the platform to the specified coordinates
                        C = self.check(p, platforms)                                                        # Use the check function to see if it can be placed on the screen
                    platforms.add(p)                                                                        # Add the new platform to the platform group
                    self.all_sprites.add(p)                                                                 # Add the new platform to the sprite group
    
    #START SCREEN
    def start_screen(self):
        while self.game_state == "start":                                   # While the Game State is start
            self.bg = pygame.image.load("./img/Start.png")                  # Create a variable for the background image
            self.surf = pygame.transform.scale(self.bg,(WIDTH,HEIGHT))      # Fit the background to the correct dimensions
            self.displaysurface.blit(self.surf,(0,0))                       # Display the transformed background
            for event in pygame.event.get():                # If PyGame Recognizes an event happening,
                if event.type == QUIT:                      # And if PyGame recognizes a "QUIT" Event, (wanting to close the window)
                        pygame.quit()                       # Close the PyGame window
                        sys.exit()                          # Terminate the program
                if event.type==pygame.KEYDOWN:     # But if that event is a keypress,
                    if event.key== pygame.K_q:     # And that key is Q,
                        pygame.quit()              # Close the PyGame window
                        sys.exit()                 # Terminate the program
                    elif event.key == pygame.K_r:  # If that key is R,
                        self.game_state = "game"   # Change the game state to game                                     
            pygame.display.update()                                         # Regardless of choice, Update the display

       
   
    #GAME OVER SCREEN
    def game_over(self):
            self.displaysurface.fill("black")
            time.sleep(0.25)                                                     # Wait for a quarter of a second
            self.bg = pygame.image.load("./img/END.png")                         # Create a variable for the background image
            self.surf = pygame.transform.scale(self.bg,(WIDTH,HEIGHT))           # Fit the background to the correct dimensions
            self.displaysurface.blit(self.surf,(0,0))                            # Display the transformed background
            self.font = pygame.font.SysFont("arial", 60,True)                    # Create a new variable called font
            self.Score = self.font.render(str(f"{P1.score}"),True,"green")       # Create a Score variable
            self.displaysurface.blit(self.Score,(WIDTH-315, HEIGHT - 363))       # Display the title at the correct position
            for event in pygame.event.get():        # Get every event that happens
                if event.type == QUIT:              # If PyGame recognizes a "QUIT" Event, (wanting to close the window)
                    pygame.quit()                   # Close the PyGame window
                    sys.exit()                      # Terminate the program
                    
                if event.type == pygame.KEYDOWN:        # If PyGame recognizes a KEYDOWN event (pressing a key)
                    if event.key== pygame.K_q:              # And if the key pressed is a Q,
                        pygame.quit()                       # Close the PyGame window
                        sys.exit()                          # Terminate the program
                        
                if event.type == pygame.KEYDOWN:        # If PyGame recognizes a KEYDOWN event (pressing a key)
                    if event.key== pygame.K_r:             # And if the key released is an "R",
                        self.game_state = "game"           # Change the Game State to Start
                        P1.reset()                           # Reset Player 1
                        PT1 = platform()
                        PT1.surf = pygame.Surface((WIDTH, 20))                           # This draws the flat platform that was the first instance of PT1
                        PT1.surf.fill("black")                                           # Color the surface BLACK
                        PT1.rect = PT1.surf.get_rect(center = (WIDTH/2, HEIGHT - 10))    # Set it to the bottom of the screen
                        self.InI()
                        
            pygame.display.update()                                               # Regardless of choice, Update the display
    
    #MAIN RUNNING    
    def run(self,state):
        self.game_state = state                                                 # Start the game with the specified state
        while True:                                                             # While running,
            if self.game_state == "start":              # If the game instance is start,
                while self.game_state == "start":       # While the game instance is start,
                    self.start_screen()                 # Load the start screen
            
            elif self.game_state == "game":                                         # If the game state is game,
                self.InI()                                                          # Reset the level
                self.plat_gen()                                                     # Run the platform generation function
                while self.game_state == "game":                                    # While the game state is game,
                    self.plat_gen()                                                 # Run the platform generation function
                    P1.update()                                                     # Update Player 1 (Tied to collision and gravity)
                    self.bg = pygame.image.load("./img/bg.png")                     # Create a variable for the background image
                    self.surf = pygame.transform.scale(self.bg,(WIDTH,HEIGHT))      # Adjust the image to fit the screen width
                    self.displaysurface.blit(self.surf,(0,0))                       # Display the image
                    self.f = pygame.font.SysFont("Verdana", 20)                     # Score variable with it's params
                    self.g  = self.f.render(str(P1.score), True, (123,255,0))       # Rendered variable with IT's params
                    self.displaysurface.blit(self.g, (WIDTH/2, 10))                 # Render the rendered variable
                    
                    for event in pygame.event.get():        # Get every event that happens
                        if event.type == QUIT:              # If PyGame recognizes a "QUIT" Event, (wanting to close the window)
                            pygame.quit()                   # Close the PyGame window
                            sys.exit()                      # Terminate the program
                        
                        # Jumping 
                        if event.type == pygame.KEYDOWN:                    # If PyGame recognizes a KEYDOWN event (pressing a key)
                            if event.key== pygame.K_SPACE:                  # And if the key pressed is the Spacebar,
                                P1.jump()                                   # Ascend
                        if event.type == pygame.KEYUP:                      # If PyGame recognizes a KEYUP event (releasing a key)
                            if event.key== pygame.K_SPACE:                  # And if the key released is the Spacebar,
                                P1.canceljump()                             # Descend
                    
                    #Despawn platforms once beyond the screen            
                    if P1.rect.top <= 600:                                # If the top of the player is less than 1000 units,
                        P1.pos.y += abs(P1.vel.y+4)                       # Add the absolute value of the Y velocity to the Player's Y Position
                        for plat in platforms:                            # And for each platform,
                            plat.rect.y += abs(P1.vel.y)                  # Add the absolute value of P1 Y velocity to the platform + 2 (Buffer)
                            if plat.rect.top >= HEIGHT:                   # And if the platform is off screen, (greater value than the height)
                                plat.kill()                               # Unload the platform
                    
                    #Lose condition (Player position greater than screen)            
                    if P1.rect.top > HEIGHT:            # If the top of Player 1's sprite position is larger than the height,
                        for entity in self.all_sprites:
                            entity.kill()
                        time.sleep(0.25)
                        self.game_state = "over"        # Change the game state to over
                    
                    for entity in self.all_sprites:                              # For a sprite in the group of available sprites,
                        self.displaysurface.blit(entity.surf, entity.rect)       # Display them
                    pygame.display.update()          # Update the screen
                    self.FramePerSec.tick(FPS)       # Advance each tick
                    P1.move()                        # Allows Player 1 to move
                    
            elif self.game_state == "over":             # If the game state is over,
                while self.game_state == "over":        # WHILE the game state is over,
                    self.game_over()                    # Call the game over function
            else:                           # Otherwise,
                pygame.quit()               # Quit the game

if __name__=="__main__":
    MAIN().run("start")