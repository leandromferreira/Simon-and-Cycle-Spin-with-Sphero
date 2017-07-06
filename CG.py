import pygame
import random
import time
from kulka import Kulka

pygame.init()
gameDisplay = pygame.display.set_mode((800,600))
pygame.display.set_caption("simon")
crash_sound = pygame.mixer.music.load("Bleep.mp3")

white = (0,0,202)
#white = (255,255,255)
black = (8,8,8)
RED = (255,0,0)
new = (250,31,86)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
bright_yellow = (150,150,0)
bright_blue = (0,0,150)
bright_green = (0,150,0)
bright_red = (150,0,0)
#bgcolor = (0,128,255)
bgcolor= (37,72,153)
pause = False




ADDR = '68:86:E7:06:34:F9'
SPEED = 0x15
SLEEP_TIME = 0.3


def make_a_step(kulka, current_angle):
    kulka.roll(SPEED, current_angle)
    time.sleep(SLEEP_TIME)
    kulka.roll(0, current_angle)


def make_a_circle(kulka, steps, direction,color):#faz o Sphero andar fazendo um circulo
    rotate_by = 360 // steps
    current_angle = 5

    if direction < 0:    
	for _ in range(steps):#Esquerda
		kulka.set_rgb(color[0],color[1],color[2])	        
		make_a_step(kulka, current_angle % 360)
	        current_angle -= rotate_by
		
		
    else:
	for _ in range(steps):#Direita
		kulka.set_rgb(color[0],color[1],color[2])
	        make_a_step(kulka, current_angle % 360)
	        current_angle += rotate_by
    kulka.set_rgb(0,0,0)	
		
def quitgame():#sai do jogo
	pygame.quit()
	quit()
def drawbutton_Simon():#desenha os botoes pro simon
	pygame.draw.rect(gameDisplay,bright_yellow,(150,100,175,175))
	pygame.draw.rect(gameDisplay,bright_blue,(345,100,175,175))
	pygame.draw.rect(gameDisplay,bright_red,(150,295,175,175))
	pygame.draw.rect(gameDisplay,bright_green,(345,295,175,175))
def drawbutton_Circle():
	pygame.draw.rect(gameDisplay,bright_green,(150,100,175,175))
	pygame.draw.rect(gameDisplay,bright_blue,(345,100,175,175))
def drawsibutton_Simon(color):#Desenha os botoes para o jogo Simon
	#print(1)
	if color == YELLOW:
		pygame.draw.rect(gameDisplay,color,(150,100,175,175))
	elif color == BLUE:
		pygame.draw.rect(gameDisplay,color,(345,100,175,175))
	elif color == RED:
		pygame.draw.rect(gameDisplay,color,(150,295,175,175))
	elif color == GREEN:
		pygame.draw.rect(gameDisplay,color,(345,295,175,175))

def text_objects(text,font):
	textsurface = font.render(text,True,black)
	return textsurface,textsurface.get_rect()
def button(text,x,y,w,h,ic,ac,action=None):#Desenha botao na tela
	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()
	if x+w>mouse[0]>x-w and y+w>mouse[1]>y-w:
		pygame.draw.circle(gameDisplay,ic,(x+h,y),w,0)
		pygame.draw.circle(gameDisplay,black,(x+h,y),w+2,3)
		if click[0]==1 and action!=None:
			action()
	else:
		pygame.draw.circle(gameDisplay,ac,(x+h,y),w,0)
		pygame.draw.circle(gameDisplay,black,(x+h,y),w+2,3)
	smallText = pygame.font.SysFont("broadway",25)
	textSurf,textRect = text_objects(text,smallText)
	textRect.center  = (x+h,y)
	gameDisplay.blit(textSurf,textRect)
def controlSimon():#Mostra os controles do jogo Simon
	cont = True
	clock = pygame.time.Clock()
	while cont:
		for event in pygame.event.get():
			if(event.type == pygame.QUIT):
				quitgame()
		gameDisplay.fill(bgcolor)
		lt = pygame.font.SysFont('cooperblack',45)
		ttSurf,ttRect = text_objects("Controls: Q,W,A,S",lt)
		ttRect.center = (400,300)
		gameDisplay.blit(ttSurf,ttRect)
		pygame.display.update()
		pygame.time.wait(1000)
		cont = False
		game_loop_Simon()

def controlCircle():#Mostra os controles do jogo Circle
	cont = True
	clock = pygame.time.Clock()
	while cont:
		for event in pygame.event.get():
			if(event.type == pygame.QUIT):
				quitgame()
		gameDisplay.fill(bgcolor)
		lt = pygame.font.SysFont('cooperblack',45)
		ttSurf,ttRect = text_objects("Controles: Q-Sim,W-Nao",lt)
		ttRect.center = (400,300)
		gameDisplay.blit(ttSurf,ttRect)
		pygame.display.update()
		pygame.time.wait(1000)
		cont = False
		game_loop_Circle()
def game_intro():#Tela inicial
	intro = True
	clock = pygame.time.Clock()
	while intro:
		for event in pygame.event.get():
			if(event.type == pygame.QUIT):
				quitgame()
		gameDisplay.fill(bgcolor)
		largetext=pygame.font.SysFont('cooperblack',65)
		TextSurf,TextRect = text_objects("Sphygame",largetext)
		TextRect.center = (400,100)
		gameDisplay.blit(TextSurf,TextRect)
		
		
		button("Circle",150,450,50,20,GREEN,bright_green,controlCircle)
		button("Simon",350,450,50,20,BLUE,bright_blue,controlSimon)
		button("Quit",550,450,50,20,RED,bright_red,quitgame)
		
		
		pygame.display.update()
		clock.tick(15)
def unpause():#sai do pause
	global pause 
	pause = False
def yourscore(score): #Pontuacao final
	temp = pygame.font.SysFont("comicsansms",25)
	t1 = temp.render("Sua pontuacao: " + str(score),True,black)
	gameDisplay.blit(t1,(300,400))
def crash(score):#ERROU
	pygame.mixer.music.play()
	time.sleep(2)
	pygame.mixer.music.stop()
	#pygame.mixer.music.play(crash_sound)
	gameDisplay.fill(bgcolor)
	te = pygame.font.SysFont("comicsansms",75)
	teSurf,teRect = text_objects("ERROOOOU!",te)
	teRect.center = (400,300)
	gameDisplay.blit(teSurf,teRect)
	yourscore(score)
	pygame.display.update()
	time.sleep(2)
	game_intro()
def displayscore(score):#mostrar pontuacao
	font = pygame.font.SysFont("comicsansms",25)
	text = font.render("Pontucao : " + str(score),True,BLUE)
	gameDisplay.blit(text,(650,0))
def paused():#tela de pause
	clock = pygame.time.Clock()
	while pause:
		for event in pygame.event.get():
			if(event.type == pygame.QUIT):
				quitgame()
		
		gameDisplay.fill(bgcolor)
		largeText = pygame.font.SysFont("cooperblack",100)
		TextSurf,TextRect = text_objects("Pausa",25)
		TextRect.center = (400,100)
		gameDisplay.blit(TextSurf,TextRect)
		
		button("CONTINUE",150,450,100,30,GREEN,bright_green,unpause)
		button("QUIT",550,450,100,30,RED,bright_red,quitgame)
		
		pygame.display.update()
		clock.tick(15)
	
def game_loop_Simon():
	global pause,pattern,index,waitinginput,play
	clock = pygame.time.Clock()
	play = True
	index = 0
	pattern = []
	waitinginput = False
	score = 0
	clicked = None
	gameDisplay.fill(black)
	#drawbutton_Simon()
	displayscore(score)
	pygame.display.update()
		
	with Kulka(ADDR) as kulka: #Conecta		
		while play:
			#gameDisplay.fill(black)
			#drawbutton_Simon()
			#displayscore(score)
			#pygame.display.update()
			clock.tick(60)
			clicked = None
			for event in pygame.event.get():
				if(event.type == pygame.QUIT):
					quitgame()
				if(event.type == pygame.KEYDOWN):#Entrada do teclado
					if(event.key == pygame.K_q):
						clicked = YELLOW
					elif(event.key == pygame.K_w):
						clicked = BLUE
					elif(event.key == pygame.K_a):
						clicked = RED
					elif(event.key == pygame.K_s):
						clicked = GREEN
					if(event.key == pygame.K_p):
						pause = True	
						paused()

			if not waitinginput:
				gameDisplay.fill(black)
				#drawbutton_Simon()
				displayscore(score)
				pygame.display.update()
				#pygame.display.update()
				pygame.time.wait(1000)
				pattern.append(random.choice((YELLOW,BLUE,RED,GREEN)))
				#origsurf = gameDisplay.copy()
				for button in pattern:
					#print (button)
					kulka.set_rgb(button[0],button[1],button[2])#Sphero cor
					pygame.time.wait(300)
					kulka.set_rgb(0,0,0)					
					#drawbutton_Simon()
					#pygame.display.update()
					pygame.time.wait(500)
					#gameDisplay.blit(origsurf,(0,0))
			
				waitinginput = True
				drawbutton_Simon()
				pygame.display.update()
				
			else:
				if clicked and clicked == pattern[index]:
					drawsibutton_Simon(clicked)
					pygame.display.update()
					drawbutton_Simon()	
					pygame.display.update()				
					pygame.time.wait(200)
					index+=1
					if index == len(pattern):
						score+=1
						waitinginput = False
						index =0 
						gameDisplay.fill(black)
						drawbutton_Simon()
						displayscore(score)
						pygame.display.update()
				elif clicked and clicked!= pattern[index]:
					crash(score)
def game_loop_Circle():
	global pause,pattern,index,waitinginput,play
	clock = pygame.time.Clock()
	play = True
	steps = 5
	stepsANT = steps
	direction = 1
	directionANT = direction
	waitinginput = False
	color=None;
	colorANT = None
	score = 0
#	gameDisplay.fill(black)
#	displayscore(score)
#	pygame.display.update()
	clock.tick(60)
		
	with Kulka(ADDR) as kulka:	
		while play:
			clicked = None	
			displayscore(score)
			clock.tick(60)
	
			for event in pygame.event.get(): #leitura do teclado para colher a resposta
				if(event.type == pygame.QUIT):
					quitgame()
				if(event.type == pygame.KEYDOWN):
					if(event.key == pygame.K_q):
						clicked = "YES"
						resUser = "YES"
					elif(event.key == pygame.K_w):
						clicked = "NO"						
						resUser = "NO"
					if(event.key == pygame.K_p):
						pause = True	
						paused()
			if not waitinginput:#chamar funcao do circle
				pygame.time.wait(1000)
				Color= random.choice((YELLOW,BLUE,RED,GREEN))
				direction = random.choice((1,-1))
				steps=random.choice((5,10,15,20))
				make_a_circle(kulka, steps, direction,Color)
				question = random.choice(("A cor e a mesma que a anterior?",
							 "A cor era amarelo?",
							 "A cor era verde?",
							 "A cor era vermelho?",
							 "A cor era azul?",
							 "A direcao foi a mesma?",
							 "A bola foi para a esquerda?",
							 "A bola foi para a direita?",
							 "O tamanho era maior que o anterior?",
							 "O tamanho era o mesmo anterior?",
							 "O tamanho era menor que o anterior?"))#Perguntas possiveis

				if question == "A cor e a mesma que a anterior?":
					if color==colorANT:
						res="YES"
					else:
					  	res="NO"
				if question == "A cor era amarelo?": 
					if color==YELLOW:
						res="YES"
					else:
					  	res="NO"
				if question == "A cor era verde?": 
					if color==GREEN:
						res="YES"
					else:
					  	res="NO"
				if question == "A cor era vermelho?": 
					if color==RED:
						res="YES"
					else:
					  	res="NO"
				if question == "A cor era azul?": 
					if color==BLUE:
						res="YES"
					else:
					  	res="NO"
				if question == "A direcao foi a mesma?": 
					if direction==directionANT:
						res="YES"
					else:
					  	res="NO"
							 
				if question == "A bola foi para a direita?":
					if direction == 1:
						res = "YES"
					else:
						res = "NO"
				if question == "A bola foi para a esquerda?":
					if direction == -1:
						res = "YES"
					else:
						res = "NO"
				if question == "O tamanho era o mesmo anterior?":
					if steps == stepsANT :
						res = "YES"
					else:
						res = "NO"
				if question == "O tamanho era menor que o anterior?":
					if steps < stepsANT :
						res = "YES"
					else:
						res = "NO"
				if question == "O tamanho era maior que o anterior?":
					if steps > stepsANT :
						res = "YES"
					else:
						res = "NO"
				#Faz a tela de resposta			
				gameDisplay.fill(bgcolor)
				fontText = pygame.font.SysFont("cooperblack",25)
				TextSurf,TextRect = text_objects(question,fontText)
				TextRect.center = (400,100)
				gameDisplay.blit(TextSurf,TextRect)
				button("SIM",150,450,100,30,GREEN,bright_green,None)
				button("NAO",550,450,100,30,RED,bright_red,None)
				pygame.display.update()					 
				waitinginput = True
			else:
				if clicked and res == resUser:#Certa a resposta
					#drawsibutton_Simon(clicked)
					#pygame.display.update()
					pygame.time.wait(200)
					score+=1
					waitinginput = False
					clicked = None
					displayscore(score)
					button("ACERTOU",150,450,100,30,GREEN,bright_green,None)
					pygame.display.update()
					colorANT=color
					directionANT=direction
					stepsANT=steps
					pygame.time.wait(500)
					displayscore(score)				
					gameDisplay.fill(black)
					pygame.display.update()
				elif clicked and res != resUser:
					crash(score)#errou
				
game_intro()
game_loop();
quitgame()
