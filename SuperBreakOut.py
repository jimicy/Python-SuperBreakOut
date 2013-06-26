'''
Author: Jimmy Wang
Date: May 1, 2012
 
Description: This program is a Super Brick Breaker clone game. There are 6 rows
and 18 bricks each row. You have 3 lives. The extra features I decided to include
are 2 players capabilities and when half of the bricks are destroyed the paddle's
size is halved.
'''

#I-Import and Initalize
import pygame,SuperBreakOutSprites
pygame.init()
pygame.mixer.init()
pygame.key.set_repeat(17,17)
screen = pygame.display.set_mode((640, 480)) 

def main():
    # D-Display configuration
    pygame.display.set_caption('SuperBreakOut')
    
    #E-Entities
    background = pygame.Surface(screen.get_size())
    background.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    
    #Set the background music
    pygame.mixer.music.load('bgm.ogg')
    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.play(-1)  
    #Set sound effect for when ball hits the brick
    hit_brick = pygame.mixer.Sound('hit_brick.ogg')
    hit_brick.set_volume(1)
    #Set sound effect for when ball hits the paddle
    hit_paddle = pygame.mixer.Sound('hit_paddle.ogg')
    hit_paddle.set_volume(1)
    #Set sound effect for gameover
    gameover = pygame.mixer.Sound('gameover.ogg')
    gameover.set_volume(0.7)
    
    # "Game Over" Image to Display After Game Loop Terminates
    gameover_img = pygame.image.load('gameover.png')
    gameover_img = gameover_img.convert_alpha()
    
    #Create the endzone
    endzone=SuperBreakOutSprites.EndZone(screen)
    
    #Create the score keeper
    score_keeper = SuperBreakOutSprites.ScoreKeeper()
    
    #Create the lives
    lives = SuperBreakOutSprites.Lives()
   
    #Create player 1 and 2
    player1 = SuperBreakOutSprites.Player(screen, 1)
    player2 = SuperBreakOutSprites.Player(screen, 2)
    playerGroup=pygame.sprite.Group(player1,player2)    
    
    #Create the ball
    ball = SuperBreakOutSprites.Ball(screen)

    # Create the bricks
    #list of colors (blue, green, orange, yellow, red, and violet)
    color=[(0,0,255),(0,255,0),(255,140,0),(255,215,0),(255,0,0),(127,0,255)]
    bricks = []
    
    brick_x=0
    brick_y=screen.get_height()/3
    width=screen.get_width()/18
    
    for row in range(6):
        brick_x=0
        for brick in range(18):
            #Fills the remaining gap at the end
            if brick==17:
                #passes the variables brick x, brick y, width, color and value
                bricks.append(SuperBreakOutSprites.Brick\
                     (brick_x,brick_y-((row+1)*20),width+10,color[row])) 
            else:        
                #passes the variables brick x, brick y, width, color and value
                bricks.append(SuperBreakOutSprites.Brick\
                              (brick_x,brick_y-((row+1)*20),width,color[row]))
            brick_x+=width 
    brickGroup = pygame.sprite.Group(bricks)

    
    allSprites = pygame.sprite.Group\
               (endzone,score_keeper,lives,player1,player2,ball,bricks)
    
    # A - Action (broken into ALTER steps)
    # A - Assign values to key variables
    clock = pygame.time.Clock()
    keepGoing = True
    # Hide the mouse pointer
    pygame.mouse.set_visible(False)
     
    # L - Loop
    while keepGoing:
     
        # T - Timer to set frame rate
        time=clock.tick(30)
     
        # E - Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            if event.type==pygame.KEYDOWN:
                #Depending on the key pressed certain valves are passed 
                #into player2's change direction
                if event.key==pygame.K_a:
                    player2.change_direction(-10)
                elif event.key==pygame.K_d:
                    player2.change_direction(10)
        
        #Passes the mouse position into player1's change direction
        player1.change_direction(pygame.mouse.get_pos())
        
        #Check if the ball hits the bricks
        #Keeps track of the number of bricks hit
        x=pygame.sprite.spritecollide(ball,brickGroup, False)
        if pygame.sprite.spritecollide(ball,brickGroup, True):
            hit_brick.play()
            #Passes the number of bricks hit as the value to be added to score
            score_keeper.scored(len(x))
            ball.change_direction()
            
        #Check if the balls hits the player
        if pygame.sprite.spritecollide(ball,playerGroup,False):
            hit_paddle.play()
            ball.change_direction()
        
        #Check if the balls hits the Endzone
        if ball.rect.colliderect(endzone.rect):
            ball.reset()
            lives.lose_life()
        
        #Check for when half the bricks are elimated
        if score_keeper.get_score()==54:
            player1.change_size()
            player2.change_size()
        
        #Check for if all bricks are gone or if all lives are gone   
        if score_keeper.get_score==108 or lives.loser():
            keepGoing=False
        
        # R - Refresh display
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)      
        pygame.display.flip()
    
    #Unhide the mouse pointer
    pygame.mouse.set_visible(True)
    
    #Blit gameover on screen
    screen.blit(gameover_img, (100, 100))
    pygame.display.flip()
    
    #Play gameover sound effect
    pygame.mixer.music.set_volume(0)
    gameover.play()
    
    #Delay by 4500 miliseconds
    pygame.time.delay(4500)
    
    # Close the game window
    pygame.quit()
        
main()