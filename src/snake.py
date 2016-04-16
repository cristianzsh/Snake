import random, pygame, sys
from pygame.locals import *

FPS = 15
LARGURA_JANELA = 640
ALTURA_JANELA = 480
TAMANHO_CELULA = 20
LARGURA_CELULA = int(LARGURA_JANELA / TAMANHO_CELULA)
ALTURA_CELULA = int(ALTURA_JANELA / TAMANHO_CELULA)

BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
COR_FUNDO = (0, 0, 0)

CIMA = 'up'
BAIXO = 'down'
ESQUERDA = 'left'
DIREITA = 'right'
CABECA = 0

def main():
	global FPS_CLOCK, EXIBICAO, FONTE

	pygame.init()
	FPS_CLOCK = pygame.time.Clock()
	EXIBICAO = pygame.display.set_mode((LARGURA_JANELA, ALTURA_JANELA))
	FONTE = pygame.font.Font('dlxfont.ttf', 12)
	pygame.display.set_caption('Snake')

	mostrar_tela_inicial()
	while True:
		executar()
		mostrar_tela_fim_de_jogo()

def executar():
	x = 12
	y = 12
	coordenadas = [{'x': x, 'y': y}, {'x': x - 1, 'y': y}, {'x': x - 2, 'y': y}]
	direcao = DIREITA
	comida = gerar_posicao()

	while True:
		for ev in pygame.event.get():
			if ev.type == QUIT:
				sair()
			elif ev.type == KEYDOWN:
				if (ev.key == K_LEFT or ev.key == K_a) and direcao != DIREITA:
					direcao = ESQUERDA
				elif (ev.key == K_RIGHT or ev.key == K_d) and direcao != ESQUERDA:
					direcao = DIREITA
				elif (ev.key == K_UP or ev.key == K_w) and direcao != BAIXO:
					direcao = CIMA
				elif (ev.key == K_DOWN or ev.key == K_s) and direcao != CIMA:
					direcao = BAIXO
				elif ev.key == K_ESCAPE:
					sair()

		if coordenadas[CABECA]['x'] == -1 or coordenadas[CABECA]['x'] == LARGURA_CELULA or coordenadas[CABECA]['y'] == -1 or coordenadas[CABECA]['y'] == ALTURA_CELULA:
			return
		for corpo in coordenadas[1:]:
			if corpo['x'] == coordenadas[CABECA]['x'] and corpo['y'] == coordenadas[CABECA]['y']:
				return

		if coordenadas[CABECA]['x'] == comida['x'] and coordenadas[CABECA]['y'] == comida['y']:
			som_comida = pygame.mixer.Sound('som_comida.wav')
			som_comida.play()
			comida = gerar_posicao()
		else:
			del coordenadas[-1]

		if direcao == CIMA:
			nova_cabeca = {'x': coordenadas[CABECA]['x'], 'y': coordenadas[CABECA]['y'] - 1}
		elif direcao == BAIXO:
			nova_cabeca = {'x': coordenadas[CABECA]['x'], 'y': coordenadas[CABECA]['y'] + 1}
		elif direcao == ESQUERDA:
			nova_cabeca = {'x': coordenadas[CABECA]['x'] - 1, 'y': coordenadas[CABECA]['y']}
		elif direcao == DIREITA:
			nova_cabeca = {'x': coordenadas[CABECA]['x'] + 1, 'y': coordenadas[CABECA]['y']}

		coordenadas.insert(0, nova_cabeca)
		EXIBICAO.fill(COR_FUNDO)
		desenhar_snake(coordenadas)
		desenhar_comida(comida)
		desenhar_pontuacao(len(coordenadas) - 3)
		pygame.display.update()
		FPS_CLOCK.tick(FPS)

def desenhar_snake(coord):
	for c in coord:
		x = c['x'] * TAMANHO_CELULA
		y = c['y'] * TAMANHO_CELULA
		reta_snake = pygame.Rect(x, y, TAMANHO_CELULA, TAMANHO_CELULA)
		pygame.draw.rect(EXIBICAO, VERDE, reta_snake)


def desenhar_comida(c):
	x = c['x'] * TAMANHO_CELULA
	y = c['y'] * TAMANHO_CELULA
	com = pygame.Rect(x, y, TAMANHO_CELULA, TAMANHO_CELULA)
	pygame.draw.rect(EXIBICAO, VERMELHO, com)

def desenhar_pontuacao(p):
	pont = FONTE.render('Pontos: %s' %p, True, BRANCO)
	pont_rect = pont.get_rect()
	pont_rect.topleft = (LARGURA_JANELA - 625, 450)
	EXIBICAO.blit(pont, pont_rect)

def sair():
	pygame.quit()
	sys.exit()

def gerar_posicao():
	return {'x': random.randint(0, LARGURA_CELULA - 1), 'y': random.randint(0, ALTURA_CELULA - 1)}

def mostrar_tela_inicial():
	img = pygame.image.load('tela_inicial.png')
	imgx = 165
	imgy = 100

	while True:
		desenhar_informacoes()

		if tecla_pressionada():
			pygame.event.get()
			return
		pygame.display.update()
		EXIBICAO.blit(img, (imgx, imgy))
		FPS_CLOCK.tick(FPS)

def desenhar_informacoes():
	desenhar_texto('Pressione qualquer tecla para jogar', LARGURA_JANELA / 2, 275)
	desenhar_texto('Pressione Esc para sair', LARGURA_JANELA / 2, 300)
	desenhar_texto('2016 - Cristian Henrique', LARGURA_JANELA / 2, 430)

def desenhar_texto(texto, x, y):
	texto_obj = FONTE.render(texto, True, BRANCO)
	texto_rect = texto_obj.get_rect()
	texto_rect.center = (x, y)
	EXIBICAO.blit(texto_obj, texto_rect)


def tecla_pressionada():
	if len(pygame.event.get(QUIT)) > 0:
		sair()

	key_up_events = pygame.event.get(KEYUP)
	if len(key_up_events) == 0:
		return None
	if key_up_events[0].key == K_ESCAPE:
		sair()
	return key_up_events[0].key

def mostrar_tela_fim_de_jogo():
	fim_jogo_fonte = pygame.font.Font('dlxfont.ttf', 45)
	exib = fim_jogo_fonte.render('Fim de jogo!', True, BRANCO)
	exib_rect = exib.get_rect()
	exib_rect.midtop = (330, 50)

	EXIBICAO.blit(exib, exib_rect)
	desenhar_informacoes()
	pygame.display.update()
	pygame.time.wait(500)
	tecla_pressionada()

	while True:
		if tecla_pressionada():
			pygame.event.get()
			return
main()