'''HEY ALL...
The following is a simple python project which is an AIM TRAINER ..The project ensures a walk through of the pygame module and also provides demonstration of the concepts like Class, Object, functions , etc.. in python.
The project can be more of a kind of intermediate type and will definitely helps to strengthen your base regarding the concepts 
mentioned above and happy coding experience...
Feel free to try this out .. and also try to include your creative contributions...

Author: VJ 13 SS
Last modified: 12 march 2024 5:03 pm
'''
import pygame
import math
import time
import random
pygame.init()


WIDTH,HEIGHT = 2500,2200 #Adjust the size for your screen
win = pygame.display.set_mode((WIDTH,HEIGHT))#Window object

pygame.display.set_caption('Aim Trainer')#Set caption for the window

TARGET_INCREMENT = 400#adds new target every 400ms
TARGET_EVENT = pygame.USEREVENT #this gets triggered off every 400ms and adds new target to the screen

TARGET_PADDING = 30 #30 pixels up from the edge of the screen

BG_COLOR = (0,25,40)#rgb values
TOP_BAR_HEIGHT = 80  #Height of the top bar
LIVES = 30

LABEL_FONT = pygame.font.SysFont('comicsans',45)#Comicsans font of size 24

class Target:
	MAX_SIZE = 50 #max size of target is 30
	GROWTH_RATE = 0.2 #grows 0.2 times every time
	COLOR = 'red'
	SECOND_COLOR = 'white'
	
	def __init__(self,x,y):
		self.x = x #random x coordinate
		self.y = y #random y coordinate
		self.size = 0 #initial size 
		self.grow = True
		
	def update_size(self):
		if self.size + self.GROWTH_RATE > self.MAX_SIZE:#If reached the max size while growing
			self.grow = False #started shrinking
			
		if self.grow:#If grow == True..grow the target
			self.size += self.GROWTH_RATE
		else: #shrink the target
			self.size -= self.GROWTH_RATE
		
	def draw_aim(self,win):
		#Drawing 4 circles similar to an aim
		#Draws 1st circle
		pygame.draw.circle(win, self.COLOR, (self.x,self.y), self.size)
		#Draws 2nd circle
		pygame.draw.circle(win, self.SECOND_COLOR, (self.x,self.y), self.size * 0.8)
		#Draws 3rd circle
		pygame.draw.circle(win, self.COLOR, (self.x,self.y), self.size * 0.6)
		#Draws 4th circle
		pygame.draw.circle(win, self.SECOND_COLOR, (self.x,self.y), self.size * 0.4)
		
	def collide(self, x, y):
		# (x,y) represents the ppsition where we keep the mouse pointer
		#if the distance from that point to the circle is less than the radius then we had touched the circle
		dist = math.sqrt(((self.x - x)**2) + ((self.y-y)**2))
			
			#Returns True or False
		return dist<self.size

def draw_top_bar(win,elapsed_time,targets_pressed, misses):
	pygame.draw.rect(win,'grey', (0,0,WIDTH, TOP_BAR_HEIGHT))#to draw rectangel on (0,0) --> Top left
	
	time_label = LABEL_FONT.render(f' Time: {round(elapsed_time,2)} sec', 1, 'red')#rendering font to display time
	life_label = LABEL_FONT.render(f'Lives {LIVES - misses}', 1, 'red')
	misses_label = LABEL_FONT.render(f'Misses {misses}', 1, 'red')
	hits_label = LABEL_FONT.render(f'Hits: {targets_pressed}', 1, 'red')
	speed = round((targets_pressed /elapsed_time),1)
	speed_label = LABEL_FONT.render(f'Speed {speed} t/s', 1, 'red')
	
	win.blit(time_label, (10,20))#To display a surface at a position
	win.blit(life_label, (950,20))
	win.blit(misses_label, (750,20))
	win.blit(hits_label, (550,20))
	win.blit(speed_label, (270,20))

#To display the final status
def end_screen(win, elapsed_time, clicks,targets_pressed,misses):
	win.fill(BG_COLOR)#To clear the screen
	
	time_label = LABEL_FONT.render(f' Time: {round(elapsed_time,2)} sec', 1, 'white')
	hits_label = LABEL_FONT.render(f'Hits: {targets_pressed}', 1, 'white')
	accuracy = round((targets_pressed / (targets_pressed + misses ) )*100, 1)
	accuracy_label = LABEL_FONT.render(f'Accuracy {accuracy}', 1, 'white')
	
	win.blit(time_label, (500,500))#To display a surface at a position
	win.blit(hits_label, (500,600))
	win.blit(accuracy_label, (500,700))
	
	pygame.display.update()
	
	run = True
	#The loop gets executed till the uses presses a key or exits from the code
	while run:
		for event in pygame.event.get():
			if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
				quit()
	
#To draw the targets	
def draw(win, targets):
	win.fill(BG_COLOR)
	
	for target in targets:
		target.draw_aim(win)#to draw the aim
	
def main():
	run = True
	targets = []#To store the targets
	
	pygame.time.set_timer(TARGET_EVENT, TARGET_INCREMENT)#The event gets triggered off every 400ms
	
	clock = pygame.time.Clock()#To set the frames per second
	
	targets_pressed = 0
	clicks = 0
	misses = 0 #To indicate how many targets we missed
	start_time = time.time()
	
	while run:#Infinite loop ..Runs till we quit the game
		clock.tick(60)#Runs at 60 frames per second
		elapsed_time = time.time() - start_time
		click = False
		mouse_pos = pygame.mouse.get_pos()#Gives the position of mouse pointer
		
		for event in pygame.event.get():#Gets the various events in pygame
			if event == pygame.QUIT:
				run = False
				break
				
			if event.type == TARGET_EVENT:
				#New target gets created at random position
				x = random.randint(TARGET_PADDING,WIDTH - TARGET_PADDING)
				y = random.randint(TARGET_PADDING + TOP_BAR_HEIGHT ,HEIGHT - TARGET_PADDING)#The target will appear below the Top bar/The rectangular box on top
				
				target = Target(x,y)
				targets.append(target)
				
			if event.type == pygame.MOUSEBUTTONDOWN:
				clicks =+1 #we clicked on the target
				click = True
		
		for target in targets:
			target.update_size()
			
			if target.size <= 0:
				targets.remove(target)
				misses +=1 #We didnt press on the target and missed it
				
			if click and target.collide(*mouse_pos):
				# in (*mouse_pos) ,the *(splat operator/Asterisk) breaks the tuple into mouse_pos[0] and mouse_pos[1]
				targets.remove(target)
				targets_pressed+=1
			
			if misses >= LIVES:
				end_screen(win, elapsed_time, clicks,targets_pressed,misses) #To display the end screen
				
		draw(win,targets)	
		draw_top_bar(win,elapsed_time,targets_pressed, misses)		
		
		pygame.display.update()#draws the aim to the display or updates it to the screen
		
	pygame.quit()
	
if __name__ =='__main__':
	main()