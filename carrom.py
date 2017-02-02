import pygame
import math

#Board Constants
BACKGROUND_COLOUR = (238,197,145)
(WIDTH, HEIGHT) = (560,560)
BORDER_LENGTH=20;
#Physics Constants
DRAG = 0.99
ELASTICITY = 0.75
#Colours RGB
BLACK = (  0,  0,  0)
PINK= (139,  0,  0)
RED = (255,  0,  0)
GREEN = (  0,255,  0)
BLUE = (  0,  0,255)
DARKGREY = (50,10,25)
GREY = (128,128,128)
BROWN = (139,69,19)
WHITE = (215,143,73)

class Particle():
	def __init__(self,screen,colour, (x, y), size,mass):
		self.x = x
		self.y = y
		self.screen = screen
		self.size = size
		self.colour = colour
		self.mass=mass
		self.speed = 0
		self.angle = 0

	def display(self):
		pygame.draw.circle(self.screen, self.colour, (int(self.x), int(self.y)), self.size)

	def move(self):
		self.x += math.sin(self.angle) * self.speed
		self.y -= math.cos(self.angle) * self.speed
		self.speed *= DRAG

	def strikers(self,flip):
		if flip%2==0:
			self.y=470
		elif flip%2!=0:
			self.y=90
		(mX,mY) = pygame.mouse.get_pos()
		if mX>440:
			self.x=440
		elif mX<120:
			self.x=120
		else:
			self.x= mX 

	def bounce(self):
		if self.x >(WIDTH-BORDER_LENGTH) - self.size:
			self.x = 2*((WIDTH-BORDER_LENGTH) - self.size) - self.x
			self.angle = - self.angle
			self.speed *= ELASTICITY

		elif self.x < (self.size+BORDER_LENGTH):
			self.x = 2*(self.size+BORDER_LENGTH) - self.x
			self.angle = - self.angle
			self.speed *= ELASTICITY

		if self.y > (HEIGHT-BORDER_LENGTH) - self.size:
			self.y = 2*((HEIGHT-BORDER_LENGTH) - self.size) - self.y
			self.angle = math.pi - self.angle
			self.speed *= ELASTICITY

		elif self.y < (self.size+BORDER_LENGTH):
			self.y = 2*(self.size+BORDER_LENGTH) - self.y
			self.angle = math.pi - self.angle
			self.speed *= ELASTICITY

	def addVectors(self, (angle1, speed1), (angle2, speed2)):
		x = math.sin(angle1) * speed1 + math.sin(angle2) * speed2
		y = math.cos(angle1) * speed1 + math.cos(angle2) * speed2

		angle = 0.5 * math.pi -math.atan2(y, x) #subtract from pi/2 to calculate the angle of the vector.
		speed = math.hypot(x, y)

		return (angle, speed)

	def collide(self,particle1,particle2):

		dist_x = particle1.x - particle2.x
		dist_y = particle1.y - particle2.y

		dist = math.hypot(dist_x, dist_y)
		if dist < particle1.size + particle2.size:
			total_mass = particle1.mass + particle2.mass

			collision_angle =  math.atan2(dist_y, dist_x) + 0.5 * math.pi # + 0.5 * math.pi to avoid sticky problem

			angle_to_pass = collision_angle - math.pi * 0.5

			''' Collision_angle - particle1.angle changes reference from standard x, y axis
			Tangential speed remains same ever after collision.  Therefore,
			tangential_speed_1 = tangential_speed_after_collision_1, same for particle 2 '''

			normal_speed_1 = math.cos(collision_angle - particle1.angle) * particle1.speed
			tangential_speed_1 = math.sin(collision_angle - particle1.angle) * particle1.speed

			normal_speed_2 = math.cos(collision_angle - particle2.angle) * particle2.speed
			tangential_speed_2 = math.sin(collision_angle - particle2.angle) * particle2.speed

			normal_speed_after_collision_1 = (normal_speed_1 * (particle1.mass - particle2.mass) + 2 * particle2.mass * normal_speed_2) / total_mass
			normal_speed_after_collision_2 = (normal_speed_2 * (particle2.mass - particle1.mass) + 2 * particle1.mass * normal_speed_1) / total_mass

			(particle1.angle, particle1.speed) = self.addVectors((collision_angle,normal_speed_after_collision_1), (angle_to_pass, tangential_speed_1))
			(particle2.angle, particle2.speed) = self.addVectors((collision_angle,normal_speed_after_collision_2), (angle_to_pass, tangential_speed_2))
			particle1.speed *= ELASTICITY
			particle2.speed *= ELASTICITY

			# prevents particles from overlapping
			overlap = 0.9*(particle1.size + particle2.size - dist+1)
			particle1.x += math.sin(collision_angle)*overlap
			particle1.y -= math.cos(collision_angle)*overlap
			particle2.x -= math.sin(collision_angle)*overlap
			particle2.y += math.cos(collision_angle)*overlap

	def decideScore(self,particle,points,game):
			if(particle.colour==(0,0,0)):
					if(game.cover==2):
						points=50
						game.cover=0
					else :
						points=10
			elif(particle.colour==(205,133,63)):
					if(game.cover==2):
						points=50
						game.cover=0
					else :
						points=20
			elif(particle.colour==(139,0,0)):
					game.cover=1

			return points

	def dues(self,particle,game):
			numberofblackmen=0
			if game.flip%2==0:
				game.score[0]-=10
			elif game.flip%2!=0:
				game.score[1]-=10
			game.flip+=1
			for man in game.my_particles[1:]:
				if man.colour==(0,0,0):
					numberofblackmen += 1
			if (numberofblackmen<9): 
				if game.qweendues==1:
					man = Particle(self.screen,BLACK,(280,280), 10,5)
					game.my_particles.append(man)
					man = Particle(self.screen,PINK,(280,280), 10,5)
					game.my_particles.append(man)
					game.qweendues=0
				else:
					man = Particle(self.screen,BLACK,(280,280), 10,5)
					game.my_particles.append(man)
			game.striker.speed=0
			game.state=0
			if (game.doubledues==1):
				game.doubledues=2
			else:
				game.doubledues=0

	def inPocketCalculation(self,particle,game):
			points=0
			if(particle.colour==(0,255,0)):
				self.dues(particle,game)
			else:
				game.my_particles.remove(particle)
				point=self.decideScore(particle,points,game)
				if (particle.colour==(139,0,0)):
					if game.qweendues==0:
						game.qweendues=1
					else:
						game.qweendues=0
				if game.flip%2==0:
					game.score[0]+=point
				elif game.flip%2!=0:
					game.score[1]+=point
				if game.doubledues==0:
					game.doubledues=1
				else:
					game.doubledues=0

	def inPocket(self,particle,game):

			if particle.x<55 and particle.speed>0 and particle.y<55 and particle.speed<5:    # Lower Left Pocket
				particle.inPocketCalculation(particle,game)

			if particle.x<55 and particle.speed>0 and particle.y>515 and particle.speed<5 :    # Upper Left Pocket
				particle.inPocketCalculation(particle,game)

			if particle.x>515 and particle.speed>0 and particle.y<55 and particle.speed<5 :    # Upper Right Pocket
				particle.inPocketCalculation(particle,game)

			if particle.x>515 and particle.speed>0 and particle.y>515 and particle.speed<5:    # Lower Right Pocket
				particle.inPocketCalculation(particle,game)

class CarromBoard():
	def __init__(self, width=900, height=560, caption="Carrom Board"):
		self.width, self.height, self.caption = width, height, caption
		self.screen = pygame.display.set_mode((self.width, self.height))
		pygame.display.set_caption(self.caption)
		self.score = [0,0]
		self.cover=0
		self.my_particles = []

		self.striker = Particle(self.screen,GREEN,(160,470), 15,50)

		man = Particle(self.screen,PINK,(280,280), 10,5)      #Queen 
		self.my_particles.append(man)

		man = Particle(self.screen,BLACK,(280,260), 10,5)      # lower 1st
		self.my_particles.append(man)

		man = Particle(self.screen,WHITE,(297,268),10,5)       # lower 2nd
		self.my_particles.append(man)

		man = Particle(self.screen,BLACK,(298,287), 10,5)     # lower 3rd
		self.my_particles.append(man)

		man = Particle(self.screen,WHITE,(280,300),10,5)       # lower 4th
		self.my_particles.append(man)

		man = Particle(self.screen,BLACK,(262,289), 10,5)     # lower 5th
		self.my_particles.append(man)

		man = Particle(self.screen,WHITE,(262,270),10,5)       # lower 6th
		self.my_particles.append(man)

		man = Particle(self.screen,BLACK,(279,238), 10,5)      # Upper 1st
		self.my_particles.append(man)

		man = Particle(self.screen,WHITE,(297,247), 10,5)     # Upper 2nd
		self.my_particles.append(man)

		man = Particle(self.screen,BLACK,(315,258), 10,5)      # Upper 3rd
		self.my_particles.append(man)

		man = Particle(self.screen,WHITE,(315,278), 10,5)     # Upper 4th
		self.my_particles.append(man)

		man = Particle(self.screen,BLACK,(315,298), 10,5)      # Upper 5th
		self.my_particles.append(man)

		man = Particle(self.screen,WHITE,(298,309), 10,5)     # Upper 6th
		self.my_particles.append(man)

		man = Particle(self.screen,BLACK,(280,320), 10,5)      # Upper 7th
		self.my_particles.append(man)

		man = Particle(self.screen,WHITE,(261,309), 10,5)     # Upper 8th
		self.my_particles.append(man)

		man = Particle(self.screen,BLACK,(244,298), 10,5)      # Upper 9th
		self.my_particles.append(man)

		man = Particle(self.screen,WHITE,(242,278), 10,5)     # Upper 10th
		self.my_particles.append(man)

		man = Particle(self.screen,BLACK,(243,258), 10,5)      # Upper 11th
		self.my_particles.append(man)

		man = Particle(self.screen,WHITE,(262,246), 10,5)     # Upper 12th
		self.my_particles.append(man)

	def draw(self):
		self.screen.fill(BACKGROUND_COLOUR)

		""" Draw inner circles"""
		pygame.draw.circle(self.screen,BLACK,(280,280),59,1)
		pygame.draw.circle(self.screen,RED,(280,280),57,3)
		pygame.draw.circle(self.screen,BLACK,(280,280),54,1)

		""" Draw pocket circles"""
		pygame.draw.circle(self.screen,DARKGREY,(36,36),20,0)
		pygame.draw.circle(self.screen,BLACK,(36,36),21,2)
		pygame.draw.circle(self.screen,DARKGREY,(527,37),20,0)
		pygame.draw.circle(self.screen,BLACK,(527,37),21,2)
		pygame.draw.circle(self.screen,DARKGREY,(37,527),20,0)
		pygame.draw.circle(self.screen,BLACK,(37,527),21,2)
		pygame.draw.circle(self.screen,DARKGREY,(526,526),20,0)
		pygame.draw.circle(self.screen,BLACK,(526,526),21,2)

		""" Draw all lines"""
		pygame.draw.line(self.screen, BLACK, (120,80), (440,80), 3)
		pygame.draw.line(self.screen, BLACK, (120,100), (440,100), 2)

		pygame.draw.line(self.screen, BLACK, (80,120), (80,440), 3)
		pygame.draw.line(self.screen, BLACK, (100,120), (100,440), 2)

		pygame.draw.line(self.screen, BLACK, (120,460), (440,460), 2)
		pygame.draw.line(self.screen, BLACK, (120,480), (440,480), 3)

		pygame.draw.line(self.screen, BLACK, (460,120), (460,440), 2)
		pygame.draw.line(self.screen, BLACK, (480,120), (480,440), 3)

		""" Draw small red circles"""
		pygame.draw.circle(self.screen,RED,(120,90),12,0)
		pygame.draw.circle(self.screen,BLACK,(120,90),14,3)
		pygame.draw.circle(self.screen,RED,(440,90),12,0)
		pygame.draw.circle(self.screen,BLACK,(440,90),14,3)

		pygame.draw.circle(self.screen,RED,(90,120),12,0)
		pygame.draw.circle(self.screen,BLACK,(90,120),14,3)
		pygame.draw.circle(self.screen,RED,(90,440),12,0)
		pygame.draw.circle(self.screen,BLACK,(90,440),14,3)

		pygame.draw.circle(self.screen,RED,(120,470),12,0)
		pygame.draw.circle(self.screen,BLACK,(120,470),14,3)
		pygame.draw.circle(self.screen,RED,(440,470),12,0)
		pygame.draw.circle(self.screen,BLACK,(440,470),14,3)

		pygame.draw.circle(self.screen,RED,(470,120),12,0)
		pygame.draw.circle(self.screen,BLACK,(470,120),14,3)
		pygame.draw.circle(self.screen,RED,(470,440),12,0)
		pygame.draw.circle(self.screen,BLACK,(470,440),14,3)

		""" Draw Inbetween small circles"""
		pygame.draw.circle(self.screen,BLACK,(100,461),7,2)
		pygame.draw.circle(self.screen,BLACK,(461,461),7,2)
		pygame.draw.circle(self.screen,BLACK,(461,100),7,2)
		pygame.draw.circle(self.screen,BLACK,(100,100),7,2)

		""" Draw inclined lines"""
		pygame.draw.line(self.screen, BLACK, (60,500), (200,360), 2)
		pygame.draw.line(self.screen, BLACK, (360,360), (500,500), 2)
		pygame.draw.line(self.screen, BLACK, (60,60), (200,200), 2)
		pygame.draw.line(self.screen, BLACK, (360,200), (500,60), 2)

		""" Draw arcs"""
		pygame.draw.arc(self.screen,BLACK,(163,163,45,45),-180 * (math.pi / 180),90 * (math.pi / 180),2)  # Top left
		pygame.draw.arc(self.screen,BLACK,(353,164,45,45), 90 * (math.pi / 180),360 * (math.pi / 180),2)  # Top right
		pygame.draw.arc(self.screen,BLACK,(163,353,45,45), -90 * (math.pi / 180),180 * (math.pi / 180),2)  #bottom left
		pygame.draw.arc(self.screen,BLACK,(353,353,45,45),0,270 * (math.pi / 180),2) 	      #bottom right

		""" Draw arrow lines"""
		pygame.draw.line(self.screen, BLACK, (57,502), (67,498), 2)
		pygame.draw.line(self.screen, BLACK, (57,502), (61,493), 2)

		pygame.draw.line(self.screen, BLACK, (502,502), (492,497), 2)
		pygame.draw.line(self.screen, BLACK, (502,502), (497,492), 2)

		pygame.draw.line(self.screen, BLACK, (60,60), (70,65), 2)
		pygame.draw.line(self.screen, BLACK, (60,60), (65,70), 2)

		pygame.draw.line(self.screen, BLACK, (500,60), (490,65), 2)
		pygame.draw.line(self.screen, BLACK, (500,60), (495,70), 2)

		""" Draw Borders"""
		pygame.draw.line(self.screen, BROWN, (550,1), (550,560), 20)
		pygame.draw.line(self.screen, BROWN, (1,10), (550,10), 20)
		pygame.draw.line(self.screen, BROWN, (10,10), (10,560), 20)
		pygame.draw.line(self.screen, BROWN, (1,550), (550,550), 20)
		if self.state ==1:
					   (mouseX2, mouseY2) = pygame.mouse.get_pos()
					   dx = mouseX2 - self.striker.x
					   dy = mouseY2 - self.striker.y
					   speed1 = round((math.hypot(dx, dy) * .02),2)
					   angle1 = 0.5*math.pi + math.atan2(dy, dx)
					   angledeg = round((angle1*180/math.pi),2) if angle1 > 0 else (2*math.pi + angle1) * (360/(2*math.pi)) 
					   myfont1 = pygame.font.SysFont("Comic Sans MS", 20)
					   speed = myfont1.render("Speed: " + str(speed1), 1, BLACK)
					   angle = myfont1.render("Angle: " + str(angledeg), 1, BLACK)
					   self.screen.blit(speed, (650, 120))
					   self.screen.blit(angle, (650, 140))
					   pygame.draw.line(self.screen, GREY, (self.striker.x,self.striker.y), (mouseX2,mouseY2), 1)

		speed = round(self.striker.speed,2)
		angledeg = round((self.striker.angle*180/math.pi),2) if self.striker.angle > 0 else (2*math.pi + self.striker.angle) * (360/(2*math.pi))
		angle = round(angledeg,2)

		self.game_over = False

		myfont = pygame.font.SysFont("Comic Sans MS", 30)
		myfont1 = pygame.font.SysFont("Comic Sans MS", 20)
		myfont2 = pygame.font.SysFont("Comic Sans MS", 13)
		label = myfont.render("SCORE BOARD", 1, BLACK)
		player1 = myfont.render("Player 1: " + str(self.score[0]), 1, BLACK)
		player2 = myfont.render("Player 2: " + str(self.score[1]), 1, BLACK)
		stats = myfont1.render("Statistics", 1, BLACK)
		speed = myfont1.render("Speed: " + str(speed), 1, BLACK)
		angle = myfont1.render("Angle: " + str(angle), 1, BLACK)

		p1 = myfont2.render("Player 2", 1, WHITE)
		p2 = myfont2.render("Player 1", 1, WHITE)

		pygame.draw.rect(self.screen,RED,(600,5,250,50),0)
		pygame.draw.rect(self.screen,BROWN,(600,5,250,50),5)
		self.screen.blit(p1, (280, 2))
		self.screen.blit(p2, (280, 540))
		self.screen.blit(label, (620, 10))
		self.screen.blit(stats, (675, 80))
		if self.state ==2:
			self.screen.blit(speed, (650, 120))
			self.screen.blit(angle, (650, 140))
		self.screen.blit(player1, (640,240))
		self.screen.blit(player2, (640,280))

		#game_over
		if not self.my_particles:
			gameOver = myfont.render("Game Over", 1, BLACK)
			self.screen.blit(gameOver, (650, 400))
			if(self.score[0] > self.score[1]):
				winner = myfont.render("Player 1 wins", 1, BLACK)
				self.screen.blit(winner, (640, 450))
			elif(self.score[0] < self.score[1]):
				winner = myfont.render("Player 2 wins", 1, BLACK)
				self.screen.blit(winner, (640, 450))
			elif(self.score[0] == self.score[1]):
				winner = myfont.render("Match Draw", 1, BLACK)
				self.screen.blit(winner, (640, 450))

	def run(self):
		self.state =0
		self.flip=0
		self.doubledues=0
		self.qweendues=0

		while True:

			self.draw()
			self.striker.display()
			for self.event in pygame.event.get():
				if self.event.type == pygame.QUIT:
					pygame.quit()
					exit()

				if self.state == 0:
					if self.flip%2==0:
						ycor=470
					elif self.flip%2!=0:
						ycor=90
					self.striker.strikers(self.flip)                   # Initial Position 
					if self.event.type == pygame.MOUSEBUTTONDOWN:
						(mouseX, mouseY) = pygame.mouse.get_pos()
						if mouseX>440:
							self.striker.x=440
						elif mouseX<120:
							self.striker.x=120
						else:
							self.striker.x=mouseX
						self.state =1
						continue

				if self.state ==1:
					if self.event.type == pygame.MOUSEBUTTONDOWN and self.event.button ==3:
							self.state=0
					if self.event.type == pygame.MOUSEBUTTONDOWN and self.event.button ==1:
						(mouseX2, mouseY2) = pygame.mouse.get_pos()
						dx = mouseX2 - self.striker.x
						dy = mouseY2 - self.striker.y
						self.striker.angle = (0.5*math.pi)+math.atan2(dy, dx)  # (0.5*math.pi)+math.atan2(dy, dx)
						self.striker.speed = math.hypot(dx, dy) * .02  # math.hypot(dx, dy) * .029
						self.state=2

			self.striker.move()
			self.striker.bounce()

			if self.striker.speed>0 and self.striker.speed<0.05 and self.state!=0:
				self.striker.x=160
				if (self.doubledues==1):
					self.flip-=1
					self.doubledues=0
				elif(self.doubledues==2):
					self.doubledues=0
				self.flip+=1
				if(self.cover==2):
					self.cover=0
					man = Particle(self.screen,PINK,(280,280), 10,5)      #Queen
					self.my_particles.append(man)
				if(self.cover==1):
					self.cover=2

				if self.flip%2==0:
					self.striker.y=470
				elif self.flip%2!=0:
					self.striker.y=90

				self.striker.speed=0
				self.state=0
			
			for i, particle in enumerate(self.my_particles):
				particle.move()
				particle.bounce()
				particle.collide(self.striker,particle)
				particle.inPocket(self.striker,self)
				particle.inPocket(particle,self)
				for particle2 in self.my_particles[i+1:]:
					particle.collide(particle,particle2)
				particle.display()
				if particle.speed<0.08:
					particle.speed=0

			pygame.display.flip() # update the contents of the entire display

def main():
	game = CarromBoard()
	while game.run():
		pass

