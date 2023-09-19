import pygame
from pygame.sprite import Sprite
from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, FUNDO, RESET_ICON, FUNDO_MENU, DEFAULT_TYPE
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.components.power_ups.power_up_manager import PowerUpManager

FONT_STYLE = "freesansbold.ttf"

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = False
        self.playing = False
        self.game_speed = 10
        self.score = 0
        self.death_count = 0
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.power_up_manager = PowerUpManager()

    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
                self.show_menu()
        pygame.display.quit()
        pygame.quit()

    def run(self):
        self.playing = True
        self.obstacle_manager.reset_obstacles()
        self.power_up_manager.reset_power_ups()
        while self.playing:
            self.events()
            self.update()
            self.draw()
            
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self)
        self.update_score()
        self.power_up_manager.update(self)

    def update_score(self):
        self.score += 1
        if self.score % 100 == 0:
            self.game_speed += 1

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.screen.blit(FUNDO,(0,0))  
        self.draw_background()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.draw_score()
        self.draw_power_up_time()
        self.power_up_manager.draw(self.screen)
        pygame.display.flip()

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def draw_score(self):
        font = pygame.font.Font(FONT_STYLE, 22)
        text = font.render(f"Pontuação: {self.score}", True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (300, 70)
        self.screen.blit(text, text_rect)
    
    def draw_power_up_time(self):
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2
        if self.player.has_power_up:
            time_to_show = round((self.player.power_up_time - pygame.time.get_ticks()) / 1000, 1)
            if time_to_show >= 0:
                font = pygame.font.Font(FONT_STYLE, 30)
                text = font.render(f"{self.player.type.capitalize()} enabled for {time_to_show} seconds", True, (255, 0, 255))
                text_rect = text.get_rect()
                text_rect.center = (half_screen_width, half_screen_height)
                self.screen.blit(text, text_rect)
        else:
               self.player.has_power_up = False
               self.player.type = DEFAULT_TYPE

    def show_menu(self):
        self.screen.fill((255, 255, 255))
        self.screen.blit(FUNDO_MENU,(0,0))
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2

        if self.death_count == 0:
            font = pygame.font.Font(FONT_STYLE, 30)
            text = font.render("Hora de correr carinha", True, (255, 0, 255))
            text_rect = text.get_rect()
            text_rect.center = (half_screen_width, half_screen_height)
            self.screen.blit(text, text_rect)
        else:
            self.screen.blit(RESET_ICON, (half_screen_width - 30, half_screen_height - 120))

            
            font = pygame.font.Font(FONT_STYLE, 26)
            text = font.render("Aperte qualquer botão para reiniciar.", True, (0, 0, 0))
            text_rect = text.get_rect()
            text_rect.center = (half_screen_width, half_screen_height)
            self.screen.blit(text, text_rect)

            
            font = pygame.font.Font(FONT_STYLE, 25)
            text = font.render(f"Total de mortes: {self.death_count}", True, (0, 0, 0))
            text_rect = text.get_rect()
            text_rect.center = (half_screen_width, half_screen_height + 40)
            self.screen.blit(text, text_rect)

            
            text = font.render(f"Pontuação: {self.score}", True, (0, 0, 0))
            text_rect = text.get_rect()
            text_rect.center = (half_screen_width, half_screen_height + 80)
            self.screen.blit(text, text_rect)

        pygame.display.update()
        self.handle_events_on_menu()

    def handle_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.score = 0
                self.game_speed = 20
                self.run()