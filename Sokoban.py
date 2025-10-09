import pygame as pg
import time

class Sokoban:
    def __init__(self, window_size, agent_choice):
        self.window_size = window_size
        self.image_size = window_size / 9
        self.level = 1
        self.show_level = True

        self.window = pg.display.set_mode((window_size, window_size))

        pg.font.init()
        self.font = pg.font.SysFont('Courier New', 50, bold=True)
        
        
        # Carregar as imagens
        try:
            
            agent1_img = pg.image.load('./assets/agente1.png')
            agent1_on_target_img = pg.image.load('./assets/a1_target.png')

            agent2_img = pg.image.load('./assets/agente2.png') 
            agent2_on_target_img = pg.image.load('./assets/a2_target.png')

           
            self.box_on_target = pg.image.load('./assets/box_target.png')
            self.box = pg.image.load('./assets/box.png')
            self.floor = pg.image.load('./assets/floor.png')
            self.target = pg.image.load('./assets/target.png')
            self.tree = pg.image.load('./assets/tree.png')
            self.wall = pg.image.load('./assets/wall.png')

        except pg.error as e:
            print("ERRO AO CARREGAR IMAGEM! Verifique o nome do arquivo.")
            print(f"Detalhe do erro: {e}")
            quit() # Encerra o jogo se não achar a imagem

        # decide qual ursinho vai ser usado
        if agent_choice == 1:
            self.agent = pg.transform.scale(agent1_img, (self.image_size, self.image_size))
            self.agent_on_target = pg.transform.scale(agent1_on_target_img, (self.image_size, self.image_size))
        elif agent_choice == 2:
            self.agent = pg.transform.scale(agent2_img, (self.image_size, self.image_size))
            self.agent_on_target = pg.transform.scale(agent2_on_target_img, (self.image_size, self.image_size))

        self.box_on_target = pg.transform.scale(self.box_on_target, (self.image_size, self.image_size))
        self.box = pg.transform.scale(self.box, (self.image_size, self.image_size))
        self.floor = pg.transform.scale(self.floor, (self.image_size, self.image_size))
        self.target = pg.transform.scale(self.target, (self.image_size, self.image_size))
        self.tree = pg.transform.scale(self.tree, (self.image_size, self.image_size))
        self.wall = pg.transform.scale(self.wall, (self.image_size, self.image_size))

        
        #desenha os niveis
        self.main_level = [['.', '.', '.', '.', '.', '.', '.', '.', '.'],
                          ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
                          ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
                          ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
                          ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
                          ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
                          ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
                          ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
                          ['.', '.', '.', '.', '.', '.', '.', '.', '.']]
       
        self.level_1 = [['t', 't', 'w', 'w', 'w', 't', 't', 't', 't'],
                        ['t', 't', 'w', 'o', 'w', 't', 't', 't', 't'],
                        ['t', 't', 'w', 'f', 'w', 'w', 'w', 'w', 't'],
                        ['w', 'w', 'w', 'b', 'f', 'b', 'o', 'w', 't'],
                        ['w', 'o', 'f', 'b', 'a', 'w', 'w', 'w', 't'],
                        ['w', 'w', 'w', 'w', 'b', 'w', 't', 't', 't'],
                        ['t', 't', 't', 'w', 'o', 'w', 't', 't', 't'],
                        ['t', 't', 't', 'w', 'w', 'w', 't', 't', 't'],
                        ['t', 't', 't', 't', 't', 't', 't', 't', 't']]
        
        self.level_2 = [['w', 'w', 'w', 'w', 'w', 't', 't', 't', 't'],
                        ['w', 'f', 'f', 'f', 'w', 't', 't', 't', 't'],
                        ['w', 'f', 'b', 'a', 'w', 't', 'w', 'w', 'w'],
                        ['w', 'f', 'b', 'b', 'w', 't', 'w', 'o', 'w'],
                        ['w', 'w', 'w', 'f', 'w', 'w', 'w', 'o', 'w'],
                        ['t', 'w', 'w', 'f', 'f', 'f', 'f', 'o', 'w'],
                        ['t', 'w', 'f', 'f', 'f', 'w', 'f', 'f', 'w'],
                        ['t', 'w', 'f', 'f', 'f', 'w', 'w', 'w', 'w'],
                        ['t', 'w', 'w', 'w', 'w', 'w', 't', 't', 't']]

        self.level_3 = [['t', 'w', 'w', 'w',   'w', 't', 't', 't', 't'],
                        ['w', 'w', 'f', 'f',   'w', 't', 't', 't', 't'],
                        ['w', 'f', 'a', 'b',   'w', 't', 't', 't', 't'],
                        ['w', 'w', 'b', 'f',   'w', 'w', 't', 't', 't'],
                        ['w', 'w', 'f', 'b',   'f', 'w', 't', 't', 't'],
                        ['w', 'o', 'b', 'f',   'f', 'w', 't', 't', 't'],
                        ['w', 'o', 'o', 'bot', 'o', 'w', 't', 't', 't'],
                        ['w', 'w', 'w', 'w',   'w', 'w', 't', 't', 't'],
                        ['t', 't', 't', 't',   't', 't', 't', 't', 't']]

        self.level_4 = [['t', 'w', 'w', 'w', 'w', 't', 't', 't', 't'],
                        ['t', 'w', 'a', 'f', 'w', 'w', 'w', 't', 't'],
                        ['t', 'w', 'f', 'b', 'f', 'f', 'w', 't', 't'],
                        ['w', 'w', 'w', 'f', 'w', 'f', 'w', 'w', 't'],
                        ['w', 'o', 'w', 'f', 'w', 'f', 'f', 'w', 't'],
                        ['w', 'o', 'b', 'f', 'f', 'w', 'f', 'w', 't'],
                        ['w', 'o', 'f', 'f', 'f', 'b', 'f', 'w', 't'],
                        ['w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 't'],
                        ['t', 't', 't', 't', 't', 't', 't', 't', 't']]

        self.level_5 = [['t', 't', 'w', 'w', 'w', 'w', 'w', 'w', 't'],
                        ['t', 't', 'w', 'f', 'f', 'f', 'f', 'w', 't'],
                        ['w', 'w', 'w', 'b', 'b', 'b', 'f', 'w', 't'],
                        ['w', 'a', 'f', 'b', 'o', 'o', 'f', 'w', 't'],
                        ['w', 'f', 'b', 'o', 'o', 'o', 'w', 'w', 't'],
                        ['w', 'w', 'w', 'w', 'f', 'f', 'w', 't', 't'],
                        ['t', 't', 't', 'w', 'w', 'w', 'w', 't', 't'],
                        ['t', 't', 't', 't', 't', 't', 't', 't', 't'],
                        ['t', 't', 't', 't', 't', 't', 't', 't', 't']]
        
        

        self.level_6 = [['t', 't', 'w', 'w', 'w',   'w', 'w', 't', 't'],
                        ['w', 'w', 'w', 'f', 'f',   'a', 'w', 't', 't'],
                        ['w', 'f', 'f', 'b', 'o',   'f', 'w', 'w', 't'],
                        ['w', 'f', 'f', 'o', 'b',   'o', 'f', 'w', 't'],
                        ['w', 'w', 'w', 'f', 'bot', 'b', 'f', 'w', 't'],
                        ['t', 't', 'w', 'f', 'f',   'f', 'w', 'w', 't'],
                        ['t', 't', 'w', 'w', 'w',   'w', 'w', 't', 't'],
                        ['t', 't', 't', 't', 't',   't', 't', 't', 't'],
                        ['t', 't', 't', 't', 't',   't', 't', 't', 't']]

        self.level_7 = [['t', 't', 'w', 'w', 'w', 'w', 't', 't', 't'],
                        ['t', 't', 'w', 'o', 'o', 'w', 't', 't', 't'],
                        ['t', 'w', 'w', 'f', 'o', 'w', 'w', 't', 't'],
                        ['t', 'w', 'f', 'f', 'b', 'o', 'w', 'w', 't'],
                        ['w', 'w', 'f', 'b', 'f', 'f', 'f', 'w', 't'],
                        ['w', 'f', 'f', 'w', 'b', 'b', 'f', 'w', 't'],
                        ['w', 'f', 'f', 'a', 'f', 'f', 'f', 'w', 't'],
                        ['w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 't'],
                        ['t', 't', 't', 't', 't', 't', 't', 't', 't']]

        self.level_8 = [['w', 'w', 'w', 'w', 'w',   'w', 'w', 'w', 't'],
                        ['w', 'f', 'f', 'f', 'f',   'f', 'f', 'w', 't'],
                        ['w', 'a', 'b', 'o', 'o',   'b', 'f', 'w', 't'],
                        ['w', 'f', 'b', 'o', 'bot', 'f', 'w', 'w', 't'],
                        ['w', 'f', 'b', 'o', 'o',   'b', 'f', 'w', 't'],
                        ['w', 'f', 'f', 'w', 'f',   'f', 'f', 'w', 't'],
                        ['w', 'w', 'w', 'w', 'w',   'w', 'w', 'w', 't'],
                        ['t', 't', 't', 't', 't',   't', 't', 't', 't'],
                        ['t', 't', 't', 't', 't',   't', 't', 't', 't']]

        self.level_9 = [['w', 'w', 'w', 'w', 'w', 'w', 't', 't', 't'],
                        ['w', 'f', 'f', 'f', 'f', 'w', 't', 't', 't'],
                        ['w', 'f', 'b', 'b', 'b', 'w', 'w', 't', 't'],
                        ['w', 'f', 'f', 'w', 'o', 'o', 'w', 'w', 'w'],
                        ['w', 'f', 'f', 'f', 'o', 'o', 'b', 'f', 'w'],
                        ['w', 'w', 'f', 'a', 'f', 'f', 'f', 'f', 'w'],
                        ['t', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w'],
                        ['t', 't', 't', 't', 't', 't', 't', 't', 't'],
                        ['t', 't', 't', 't', 't', 't', 't', 't', 't']]

        self.level_10 = [['w', 'w', 'w', 'w', 'w', 'w', 'w', 't', 't'],
                         ['w', 'o', 'o', 'b', 'o', 'o', 'w', 't', 't'],
                         ['w', 'o', 'o', 'w', 'o', 'o', 'w', 't', 't'],
                         ['w', 'f', 'b', 'b', 'b', 'f', 'w', 't', 't'],
                         ['w', 'f', 'f', 'b', 'f', 'f', 'w', 't', 't'],
                         ['w', 'f', 'b', 'b', 'b', 'f', 'w', 't', 't'],
                         ['w', 'f', 'f', 'w', 'a', 'f', 'w', 't', 't'],
                         ['w', 'w', 'w', 'w', 'w', 'w', 'w', 't', 't'],
                         ['t', 't', 't', 't', 't', 't', 't', 't', 't']]

        
        
    def clear_window(self):
        pg.draw.rect(self.window, (255, 255, 255), (0, 0, self.window.get_width(), self.window.get_height()))
        
    def copy_level(self, level):
        for y in range(9):
            for x in range(9):
                self.main_level[y][x] = level[y][x]

    def select_level(self):
        if self.level == 1:
            self.copy_level(self.level_1)
        elif self.level == 2:
            self.copy_level(self.level_2)
        elif self.level == 3:
            self.copy_level(self.level_3)
        elif self.level == 4:
            self.copy_level(self.level_4)
        elif self.level == 5:
            self.copy_level(self.level_5)
        elif self.level == 6:
            self.copy_level(self.level_6)
        elif self.level == 7:
            self.copy_level(self.level_7)
        elif self.level == 8:
            self.copy_level(self.level_8)
        elif self.level == 9:
            self.copy_level(self.level_9)
        elif self.level == 10:
            self.copy_level(self.level_10)
        
            
    def draw_map(self):
        for y in  range(9):
            for x in  range(9):
                string = self.main_level[y][x]
                if string == 'a':
                    self.window.blit(self.agent, (x * self.image_size, y * self.image_size))
                elif string == 'aot':
                    self.window.blit(self.agent_on_target, (x * self.image_size, y * self.image_size))
                elif string == 't':
                    self.window.blit(self.tree, (x * self.image_size, y * self.image_size))
                elif string == 'w':
                    self.window.blit(self.wall, (x * self.image_size, y * self.image_size))
                elif string == 'o':
                    self.window.blit(self.target, (x * self.image_size, y * self.image_size))
                elif string == 'f':
                    self.window.blit(self.floor, (x * self.image_size, y * self.image_size))
                elif string == 'b':
                    self.window.blit(self.box, (x * self.image_size, y * self.image_size))
                elif string == 'bot':
                    self.window.blit(self.box_on_target, (x * self.image_size, y * self.image_size))
                    
    def get_agent_position(self):
        agent_position = [0, 0]
        for y in range(9):
            for x in range(9):
                if self.main_level[y][x] == 'a' or self.main_level[y][x] == 'aot':
                    agent_position[0] = x
                    agent_position[1] = y
        return agent_position

    def move(self, key):
        agent_position = self.get_agent_position()

        agent_new_position = [agent_position[0], agent_position[1]]
        space_ahead = [agent_position[0], agent_position[1]]

        if key == 'w' or key == 'up':
            agent_new_position[1] -= 1
            space_ahead[1] -= 2
        elif key == 'a' or key == 'left':
            agent_new_position[0] -= 1
            space_ahead[0] -= 2
        elif key == 's' or key == 'down':
            agent_new_position[1] += 1
            space_ahead[1] += 2
        elif key == 'd' or key == 'right':
            agent_new_position[0] += 1
            space_ahead[0] += 2

        if space_ahead[0] <= -1 or space_ahead[0] >= 10 or space_ahead[1] <= -1 or space_ahead[1] >= 10:
            pass
        else:
            if self.main_level[agent_new_position[1]][agent_new_position[0]] == 'b' and self.main_level[space_ahead[1]][space_ahead[0]] == 'f':
                self.change_map(agent_position, agent_new_position, space_ahead)
            elif self.main_level[agent_new_position[1]][agent_new_position[0]] == 'bot' and self.main_level[space_ahead[1]][space_ahead[0]] == 'f':
                self.change_map(agent_position, agent_new_position, space_ahead)
            elif self.main_level[agent_new_position[1]][agent_new_position[0]] == 'b' and self.main_level[space_ahead[1]][space_ahead[0]] == 'o':
                self.change_map(agent_position, agent_new_position, space_ahead)
            elif self.main_level[agent_new_position[1]][agent_new_position[0]] == 'bot' and self.main_level[space_ahead[1]][space_ahead[0]] == 'o':
                self.change_map(agent_position, agent_new_position, space_ahead)
            elif self.main_level[agent_new_position[1]][agent_new_position[0]] == 'f':
                self.change_map(agent_position, agent_new_position, space_ahead)
            elif self.main_level[agent_new_position[1]][agent_new_position[0]] == 'o':
                self.change_map(agent_position, agent_new_position, space_ahead)

    def change_map(self, agent_position, agent_new_position, space_ahead):
        if self.main_level[agent_position[1]][agent_position[0]] == 'a':
            self.main_level[agent_position[1]][agent_position[0]] = 'f'
        elif self.main_level[agent_position[1]][agent_position[0]] == 'aot':
            self.main_level[agent_position[1]][agent_position[0]] = 'o'

        if self.main_level[agent_new_position[1]][agent_new_position[0]] == 'b' and self.main_level[space_ahead[1]][space_ahead[0]] == 'f':
            self.main_level[space_ahead[1]][space_ahead[0]] = 'b'
            self.main_level[agent_new_position[1]][agent_new_position[0]] = 'a'
        elif self.main_level[agent_new_position[1]][agent_new_position[0]] == 'bot' and self.main_level[space_ahead[1]][space_ahead[0]] == 'f':
            self.main_level[space_ahead[1]][space_ahead[0]] = 'b'
            self.main_level[agent_new_position[1]][agent_new_position[0]] = 'aot'
        elif self.main_level[agent_new_position[1]][agent_new_position[0]] == 'b' and self.main_level[space_ahead[1]][space_ahead[0]] == 'o':
            self.main_level[space_ahead[1]][space_ahead[0]] = 'bot'
            self.main_level[agent_new_position[1]][agent_new_position[0]] = 'a'
        elif self.main_level[agent_new_position[1]][agent_new_position[0]] == 'bot' and self.main_level[space_ahead[1]][space_ahead[0]] == 'o':
            self.main_level[space_ahead[1]][space_ahead[0]] = 'bot'
            self.main_level[agent_new_position[1]][agent_new_position[0]] = 'aot'
        elif self.main_level[agent_new_position[1]][agent_new_position[0]] == 'f':
            self.main_level[agent_new_position[1]][agent_new_position[0]] = 'a'
        elif self.main_level[agent_new_position[1]][agent_new_position[0]] == 'o':
            self.main_level[agent_new_position[1]][agent_new_position[0]] = 'aot'

    def new_level(self):
        if self.show_level:
            text = self.font.render(f'Level {self.level}', 1, (0, 0, 0))
            x = (self.window.get_width() / 2) - (text.get_width() / 2)
            y = (self.window.get_height() / 2) - (text.get_height() / 2)
            self.window.blit(text, (x, y))
            pg.display.update()
            time.sleep(2)
            self.show_level = False
            self.select_level()


    def is_level_completed(self):
        count = 0
        for y in range(9):
            for x in range(9):
                if self.main_level[y][x] == 'b':
                    count += 1
        
        if count == 0: 
            self.show_level = True
            self.level += 1
            
            # conta os niveis
            if self.level == 11:
                pg.display.update() 
                time.sleep(2)       
                return True        
            
            pg.display.update()
            time.sleep(1)
            
        return False


WINDOW_SIZE = 504
pg.init()
window = pg.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pg.display.set_caption("Sokoban - Seleção de Agente")

#coloca a musica
pg.mixer.init()
pg.mixer.music.load('./assets/som.mp3')
pg.mixer.music.set_volume(0.5)
pg.mixer.music.play(-1)

# Carrega as imagens para o menu
agent1_select_img = pg.transform.scale(pg.image.load('./assets/op11.png'), (200, 200))
agent2_select_img = pg.transform.scale(pg.image.load('./assets/op22.png'), (200, 200)) 

logo_img = pg.image.load('./assets/logo.png') 
logo_img = pg.transform.scale(logo_img, (200, 50)) 
logo_rect = logo_img.get_rect()
logo_rect.centerx = WINDOW_SIZE / 2 
logo_rect.top = 10 

#tela final
final_screen_img = pg.image.load('./assets/final.png') 
final_screen_img = pg.transform.scale(final_screen_img, (WINDOW_SIZE, WINDOW_SIZE)) 
final_screen_rect = final_screen_img.get_rect(topleft=(0, 0)) 


# cliques do mouse
agent1_rect = agent1_select_img.get_rect(center=(WINDOW_SIZE / 4, WINDOW_SIZE / 2))
agent2_rect = agent2_select_img.get_rect(center=(WINDOW_SIZE * 3 / 4, WINDOW_SIZE / 2))


menu_font = pg.font.SysFont('Courier New', 40, bold=True)
title_text = menu_font.render('Escolha seu ursinho', True, (0, 0, 0))
title_rect = title_text.get_rect(center=(WINDOW_SIZE / 2, WINDOW_SIZE / 4))


game_state = 'MENU' 
sokoban_game = None 
running = True

while running:
    if game_state == 'MENU':
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                # Verifica se o clique foi na marsha
                if agent1_rect.collidepoint(event.pos):
                    print("Agente 1 selecionado!")
                    sokoban_game = Sokoban(WINDOW_SIZE, 1) 
                    game_state = 'GAME' 
                # Verifica se o clique foi no Levy
                if agent2_rect.collidepoint(event.pos):
                    print("Agente 2 selecionado!")
                    sokoban_game = Sokoban(WINDOW_SIZE, 2) 
                    game_state = 'GAME' # Muda o estado para JOGO
        
        # Desenha a tela do menu
        window.fill((180, 210, 255))                  
        window.blit(logo_img, logo_rect)              
        window.blit(title_text, title_rect)          
        window.blit(agent1_select_img, agent1_rect)   
        window.blit(agent2_select_img, agent2_rect) 
        
        
    elif game_state == 'GAME':
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                key_name = pg.key.name(event.key)
                if key_name in ['w', 'a', 's', 'd', 'up', 'down', 'left', 'right']:
                    sokoban_game.move(key_name)
                elif key_name == 'r':
                    sokoban_game.select_level()
                elif key_name == 'escape':
                    running = False

        # Game Logic
        sokoban_game.clear_window()
        sokoban_game.new_level()
        sokoban_game.draw_map()
        if sokoban_game.is_level_completed():
            game_state = 'END_SCREEN'
        
        
    elif game_state == 'END_SCREEN':
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN: 
                game_state = 'MENU' # Volta para o menu
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE: # Sair com ESC
                    running = False

       
        window.blit(final_screen_img, final_screen_rect)
        
        
    pg.display.update()

pg.quit()
quit()


