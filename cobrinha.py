#########################################
###                                   ###
###           GAME COBRINHA           ###
###       AUTOR: MAYKOW MENEZES       ###
###                                   ###
###                                   ###
#########################################


import curses 
from curses import wrapper
import time
import random
import copy


###################################################################

# Representacao dos espacos vazios, cobrinha e comida
vazio = 'v'
cobrinha = '*'
comida = 'O'


# Par de cores (texto, fundo)
cor_vazio = (curses.COLOR_RED,curses.COLOR_GREEN)
cor_cobrinha = (curses.COLOR_BLACK, curses.COLOR_BLUE)
cor_comida = (curses.COLOR_CYAN, curses.COLOR_RED)
cor_mensagem = (curses.COLOR_BLACK, curses.COLOR_WHITE)


###################################################################



# Desenha o mapa na tela
def desenhaMapa(stdscr, comprimento, altura):
	for i in range(altura+1):
		for j in range(comprimento+1):
			stdscr.addstr(i, j, ' ', curses.color_pair(1))

#Desenha a comida na tela
def desenhaComida(stdscr, pos_comida):
	stdscr.addstr(pos_comida[0], pos_comida[1], comida, curses.color_pair(3))

# Desenha acobrinha na tela
def desenhaCobrinha(stdscr, pos_cobrinha):
	for i in pos_cobrinha:
		stdscr.addstr(i[0], i[1], cobrinha, curses.color_pair(2))


# Desenhaos pontos na tela
def desenhaPontos(stdsrc, num_pontos):
	stdsrc.addstr(0,1, 'Pontos: '+ str(num_pontos), curses.color_pair(1))


def msgEnd(stdsrc, comprimento, altura, pontos):
	stdsrc.addstr(int(altura/2),int(comprimento/2-6), 'FIM DO JOGO!', curses.color_pair(4))
	stdsrc.addstr(int(altura/2)+1,int(comprimento/2-5), 'PONTOS: ' + str(pontos), curses.color_pair(4))

def proximaPosicao(pos_cobrinha, direcao):
	pos = [0,0]
	if direcao == 'baixo':
		pos[0] = pos_cobrinha[-1][0] + 1 
		pos[1] = pos_cobrinha[-1][1]
	
	if direcao == 'cima':
		pos[0] = pos_cobrinha[-1][0] - 1 
		pos[1] = pos_cobrinha[-1][1]
	
	if direcao == 'direita':
		pos[0] = pos_cobrinha[-1][0]  
		pos[1] = pos_cobrinha[-1][1] + 1

	if direcao == 'esquerda':
		pos[0] = pos_cobrinha[-1][0] 
		pos[1] = pos_cobrinha[-1][1] - 1
	
	return pos


def moveCobrinha(pos_cobrinha, direcao):
	for i in range(len(pos_cobrinha)-1):
		pos_cobrinha[i] = copy.deepcopy(pos_cobrinha[i+1])

	pos_cobrinha[-1] =  proximaPosicao(pos_cobrinha, direcao)

	return pos_cobrinha


def colisaoBordas(pos_cobrinha, altura, comprimento):
	if pos_cobrinha[-1][0] < 0 or pos_cobrinha[-1][0] > altura or pos_cobrinha[-1][1] < 0 or pos_cobrinha[-1][1] > comprimento:
		return True
	else:
		return False

def autoColisao(pos_cobrinha, direcao):
	for i in pos_cobrinha:
		cont = 0
		for j in pos_cobrinha:
			if i == j: cont += 1

		if cont > 1:
			return True
	
	return False
	

def comeu(pos_cobrinha, pos_comida, direcao):
	if  proximaPosicao(pos_cobrinha, direcao) == pos_comida:
		return True
	else:
		return False
		

# Loop do game
def main(stdscr):
	stdscr.clear()
	stdscr.nodelay(True) # desabilita a espera do teclado
	
	# Defini os esquemas de cores
	curses.init_pair(1, cor_vazio[0], cor_vazio[1])
	curses.init_pair(2, cor_cobrinha[0], cor_cobrinha[1])
	curses.init_pair(3, cor_comida[0], cor_comida[1])
	curses.init_pair(4, cor_mensagem[0], cor_mensagem[1])

	# Pontuação do game
	pontos = 0

	#Tamanho do mapa
	comprimento = 50
	altura = 20
	
	# definindo a cobrinha como um vetor e sua posicao inicial
	x = int(comprimento/2)
	y = int(altura/2)
	pos_cobrinha = [[y,x],[y+1, x], [y+2, x]]

	#Posição inicial da comida
	pos_comida = [random.randint(0, altura), random.randint(0, comprimento)]

	# Define a direção inicial da cobrinha
	direcao = 'baixo'

	#define o estado do game
	play= True


	while play:
		time.sleep(.2)

		if comeu(pos_cobrinha, pos_comida, direcao):
			pontos += 1
			pos_cobrinha.append(pos_comida)
			pos_comida = [random.randint(0, altura), random.randint(0, comprimento)]		
		else:
			pos_cobrinha = moveCobrinha(pos_cobrinha, direcao)		

		

		
		desenhaMapa(stdscr, comprimento, altura)
		if colisaoBordas(pos_cobrinha, altura, comprimento) or autoColisao(pos_cobrinha, direcao):
			msgEnd(stdscr, comprimento, altura, pontos)
			stdscr.refresh()
			play = False
			time.sleep(5)

		desenhaPontos(stdscr, pontos)
		desenhaComida(stdscr, pos_comida)
		desenhaCobrinha(stdscr, pos_cobrinha)
		

		# Faz a verificação das teclas precionadas e muda a direção
		ch = stdscr.getch(curses.LINES-1, curses.COLS-1)		
		if ch == ord('q'): break
		if ch == curses.KEY_LEFT and direcao != 'direita': direcao = 'esquerda'
		if ch == curses.KEY_RIGHT and direcao != 'esquerda': direcao = 'direita'
		if ch == curses.KEY_UP and direcao != 'baixo': direcao = 'cima'
		if ch == curses.KEY_DOWN and direcao != 'cima': direcao = 'baixo'
			

# Chamadas das funcoes principais
wrapper(main)

