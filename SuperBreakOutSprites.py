import pygame
            
class Brick(pygame.sprite.Sprite):
    '''This class defines our brick sprite'''
    def __init__(self,brick_x,brick_y,width,color):
        '''This initializer takes brick x, brick y, width and color as parameters.
        It then sets up the surface for bricks, fills it and sets up the rect'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        # Set the image and rect attributes for the bricks
        self.image = pygame.Surface((width, 20))
        self.image=self.image.convert()
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.left = brick_x
        self.rect.top = brick_y
        
class Player(pygame.sprite.Sprite):
    '''This class defines our player sprite'''
    def __init__(self,screen,player_num):
        '''This initializer takes the screen and player number as parameters.
        It then loads the paddle image, saves the player num for later use 
        and sets up the rect based on the player num'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        # Define the image attributes for the paddle
        self.image = pygame.image.load('paddle1.png')
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        
        #Assign the player number
        self.__player_num=player_num
        
        # If we are initializing a sprite for player 1,
        # position it 50 pixels from the bottom of the screen
        if player_num == 1:
            self.rect.bottom = screen.get_height()-50
        #Otherwise, position it 20 pixels from the bottom of the screen.
        else:
            self.rect.bottom = screen.get_height()-20
 
        # Center the player horizontally in the window.
        self.rect.left = screen.get_width()/2
      
    def change_direction(self, displacement):
        '''This method takes the displacement and based on the player num, 
        different events occur'''
        
        #If the player num is 1, the x value is taken from the mouse position tuple
        if self.__player_num==1:
            self.rect.left = displacement[0]
        #if the player num is 2, the change in direction is added to the rect
        else:
            if self.rect.left==0:
                if displacement>0:
                    self.rect.left += displacement
            elif self.rect.left==550:
                if displacement<0:
                    self.rect.left += displacement
            else:
                self.rect.left += displacement
    
    def change_size(self):
        '''This method halves the size of the paddle'''
        self.image=pygame.image.load('paddle2.png')
        self.image=self.image.convert_alpha()
        
        
class Ball(pygame.sprite.Sprite):
    '''This class defines our ball sprite'''
    def __init__(self,screen):
        '''This initializer takes a screen as a parameter. It then loads the 
        ball image, sets up the rect, saves the screen and creates an x 
        and y direction value'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self) 
        # Set the image and rect attributes for the Ball
        self.image = pygame.image.load('ball.png')
        self.image= self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (screen.get_width()/2,screen.get_height()/2)
 
        # Instance variables to keep track of the screen surface
        # and set the initial x and y vector for the ball.
        self.__screen = screen
        self.__dx = 6
        self.__dy = -6
        
    def reset(self):
        '''This method resets the ball's position to the center'''
        self.rect.center = (self.__screen.get_width()/2,self.__screen.get_height()/2)
 
    def change_direction(self):
        '''This method causes the y direction of the ball to reverse.'''
        self.__dy = -self.__dy
             
    def update(self):
        '''This method will be called automatically to reposition the
        ball sprite on the screen.'''
        # Check if we have reached the left or right end of the screen.
        # If not, then keep moving the ball in the same x direction.
        if ((self.rect.left > 0) and (self.__dx < 0)) or\
           ((self.rect.right < self.__screen.get_width()) and (self.__dx > 0)):
            self.rect.left += self.__dx
        # If yes, then reverse the x direction. 
        else:
            self.__dx = -self.__dx
             
        # Check if we have reached the top or bottom of the court.
        # If not, then keep moving the ball in the same y direction.
        if ((self.rect.top > 0) and (self.__dy > 0)) or\
           ((self.rect.bottom < self.__screen.get_height()) and (self.__dy < 0)):
            self.rect.top -= self.__dy
        # If yes, then reverse the y direction. 
        else:
            self.__dy = -self.__dy
            
class EndZone(pygame.sprite.Sprite):
    '''This class defines the sprite for our left and right end zones'''
    def __init__(self, screen):
        '''This initializer takes a screen surface as parameters. The endzone 
        is set at the bottom of the screen'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
         
        # Our endzone sprite will be a 1 pixel tall black line.
        self.image = pygame.Surface((screen.get_width(),1))
        self.image = self.image.convert()
        self.image.fill((0, 0, 0))
         
        # Set the rect attributes for the endzone
        self.rect = self.image.get_rect()
        self.rect.left=0
        self.rect.bottom=screen.get_height()
        
class ScoreKeeper(pygame.sprite.Sprite):
    '''This class defines a label sprite to display the score.'''
    def __init__(self):
        '''This initializer loads the custom font "vermin_vibes.ttf", and
        sets the starting score to 0'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
 
        # Load our custom font, and initialize the starting score.
        self.__font = pygame.font.Font("vermin_vibes.ttf", 40)
        self.__score = 0
         
    def scored(self,value):
        '''This method takes a value as a parameter and adds to the score'''
        self.__score += value
     
    def get_score(self):
        '''Returns the score'''
        return self.__score
 
    def update(self):
        '''This method will be called automatically to display
        the current score at the top of the game window.'''
        message = "Score: %d" %\
                (self.__score)
        self.image = self.__font.render(message, 1, (193,205,193))
        self.rect = self.image.get_rect()
        self.rect.center = (320, 30)
        
class Lives(pygame.sprite.Sprite):
    '''This class defines a lives sprite to display the # of lives.'''
    def __init__(self):
        '''This initializer loads the lives image, sets up the rect and
        starting value of 3 for lives'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        # Set the image and rect attributes for the lives
        self.image=pygame.image.load('lives.png')
        self.image = self.image.convert_alpha()
         
        # Set the rect attributes for the lives
        self.rect = self.image.get_rect()
        self.rect.left= 20
        self.rect.top=10
        
        #Set the number of lives
        self.__lives=3
        
    def lose_life(self):
        '''crops out a heart and subtract a life everytime the ball 
        hits the endzone'''
        self.image=pygame.transform.chop(self.image,(0,20,28,20))
        self.__lives-=1
        
    def loser(self):
        '''returns 1 if there are no lives left or else returns a 0'''
        if self.__lives<=0:
            return 1
        else:
            return 0