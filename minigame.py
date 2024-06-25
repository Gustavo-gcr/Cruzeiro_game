import pygame
from pygame.locals import *
import random
import sys

# Definindo constantes
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
SPEED = 10
GRAVITY = 1
GAME_SPEED = 10
OBSTACLE_INTERVAL = 2000  # Intervalo de tempo entre obstáculos em milissegundos
INITIAL_OBSTACLE_SPEED = 16  # Velocidade inicial dos obstáculos
OBSTACLE_SPEED_INCREASE = 2.5  # Aumento de velocidade dos obstáculos por segundo

GROUND_HEIGHT = 20
OBSTACLE_WIDTH = 40  # Largura reduzida do obstáculo
OBSTACLE_HEIGHT = 60

class Cruzeiro(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('cruzeiro.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))  # Reduzindo o tamanho da imagem
        self.rect = self.image.get_rect()
        self.rect[0] = 50
        self.rect[1] = SCREEN_HEIGHT - GROUND_HEIGHT - self.rect.height
        self.speed = 0
        self.jump_speed = -20  # Velocidade de pulo aumentada
        self.jumping = False
        self.score = 0  # Iniciando a pontuação em zero
        self.alive = True

    def update(self):
        if self.alive:
            self.speed += GRAVITY
            self.rect[1] += self.speed

            if self.rect[1] > SCREEN_HEIGHT - GROUND_HEIGHT - self.rect.height:
                self.rect[1] = SCREEN_HEIGHT - GROUND_HEIGHT - self.rect.height
                self.jumping = False

    def jump(self):
        if not self.jumping and self.alive:
            self.jumping = True
            self.speed = self.jump_speed  # Aplicando a nova velocidade de pulo

    def increase_score(self):
        if self.alive:
            self.score += 1  # Incrementando a pontuação ao passar por um obstáculo

    def die(self):
        self.alive = False

class Obstaculo(pygame.sprite.Sprite):
    def __init__(self, xpos, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('copabr.jpg').convert_alpha()  # Corrigindo carregamento da imagem
        self.image = pygame.transform.scale(self.image, (OBSTACLE_WIDTH, OBSTACLE_HEIGHT))  # Ajuste de tamanho aqui
        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = SCREEN_HEIGHT - GROUND_HEIGHT - self.rect.height
        self.speed = speed
        self.passed = False  # Flag para indicar se o obstáculo foi passado pelo cruzeiro

    def update(self):
        self.rect[0] -= self.speed
        if self.rect[0] < -self.rect.width:
            self.kill()

class Chao(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('chao.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (SCREEN_WIDTH, GROUND_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect[0] = 0
        self.rect[1] = SCREEN_HEIGHT - GROUND_HEIGHT

    def update(self):
        pass

def mostrar_game_over(screen, score):
    # Tornar a tela mais escura
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(150)  # Transparência de 150 (0 = totalmente transparente, 255 = totalmente opaco)
    overlay.fill((0, 0, 0))  # Cor preta
    screen.blit(overlay, (0, 0))

    fonte_game_over = pygame.font.Font(None, 72)
    texto_game_over = fonte_game_over.render('Game Over', True, (255, 0, 0))
    rect_game_over = texto_game_over.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    screen.blit(texto_game_over, rect_game_over)

    fonte_score = pygame.font.Font(None, 48)
    texto_score = fonte_score.render(f'Score: {score}', True, (255, 255, 255))
    rect_score = texto_score.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
    screen.blit(texto_score, rect_score)

    pygame.display.update()

    pygame.time.wait(2000)  # Aguarda 2 segundos antes de sair

def mostrar_menu(screen):
    fonte = pygame.font.Font(None, 48)
    texto = fonte.render("Escolha a dificuldade:", True, (255, 255, 255))
    texto_rect = texto.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    screen.blit(texto, texto_rect)

    fonte = pygame.font.Font(None, 36)
    facil_texto = fonte.render("Fácil", True, (255, 255, 255))
    facil_rect = facil_texto.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10))
    screen.blit(facil_texto, facil_rect)

    medio_texto = fonte.render("Médio", True, (255, 255, 255))
    medio_rect = medio_texto.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
    screen.blit(medio_texto, medio_rect)

    dificil_texto = fonte.render("Difícil", True, (255, 0, 0))  # Cor vermelha para dificuldade difícil
    dificil_rect = dificil_texto.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 90))
    screen.blit(dificil_texto, dificil_rect)

    pygame.display.update()

    while True:
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if facil_rect.collidepoint(mouse):
                    return 0  # Fácil
                elif medio_rect.collidepoint(mouse):
                    return 1  # Médio
                elif dificil_rect.collidepoint(mouse):
                    return 2  # Difícil

def principal(dificuldade):
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Cruzeiro Game')

    clock = pygame.time.Clock()
    cruzeiro = Cruzeiro()
    chao = Chao()
    background = pygame.image.load('fundo.webp').convert()
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    cruzeiro_grupo = pygame.sprite.Group()
    cruzeiro_grupo.add(cruzeiro)

    chao_grupo = pygame.sprite.Group()
    chao_grupo.add(chao)

    obstaculo_grupo = pygame.sprite.Group()

    pygame.time.set_timer(USEREVENT + 1, OBSTACLE_INTERVAL)

    velocidade_aumento_obstaculo_timer = 0
    velocidade_obstaculo = INITIAL_OBSTACLE_SPEED

    game_over = False

    while not game_over:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    cruzeiro.jump()
            if event.type == USEREVENT + 1:
                if dificuldade == 2:  # Difícil: gerar mais obstáculos quase ao mesmo tempo
                    for _ in range(2):  # Sempre gerar 2 obstáculos no modo Difícil
                        obstaculo = Obstaculo(SCREEN_WIDTH, velocidade_obstaculo)
                        obstaculo_grupo.add(obstaculo)
                else:
                    obstaculo = Obstaculo(SCREEN_WIDTH, velocidade_obstaculo)
                    obstaculo_grupo.add(obstaculo)

        if not cruzeiro.alive:
            game_over = True

        screen.blit(background, (0, 0))

        cruzeiro_grupo.update()
        chao_grupo.update()
        obstaculo_grupo.update()

        # Aumentar a velocidade dos obstáculos gradualmente
        velocidade_aumento_obstaculo_timer += clock.get_rawtime() / 1000
        if velocidade_aumento_obstaculo_timer > 1:
            velocidade_obstaculo += OBSTACLE_SPEED_INCREASE
            velocidade_aumento_obstaculo_timer = 0

        cruzeiro_grupo.draw(screen)
        chao_grupo.draw(screen)
        obstaculo_grupo.draw(screen)

        # Verificar colisão do cruzeiro com os obstáculos
        for obstaculo in obstaculo_grupo:
            if pygame.sprite.collide_rect(cruzeiro, obstaculo):
                cruzeiro.die()
                game_over = True

        # Verificar se o cruzeiro passou por cima de um obstáculo
        for obstaculo in obstaculo_grupo:
            if obstaculo.rect.right < cruzeiro.rect.left and not obstaculo.passed:
                obstaculo.passed = True
                cruzeiro.increase_score()

        # Mostrar pontuação na tela
        fonte = pygame.font.Font(None, 36)
        texto = fonte.render(f'Pontuação: {cruzeiro.score}', True, (255, 255, 255))  # Cor do texto ajustada para branco
        screen.blit(texto, (10, 10))

        pygame.display.update()

    # Mostrar tela de Game Over
    mostrar_game_over(screen, cruzeiro.score)

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Cruzeiro Game')

    mostrar_menu(screen)
    dificuldade = mostrar_menu(screen)

    principal(dificuldade)
