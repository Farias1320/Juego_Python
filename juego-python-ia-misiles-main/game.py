import pygame
from constants import *
from player import Player
from pygame.locals import *
from webcam import Webcam
from enemy import Enemy
from events import *
from levels import get_level_config
from background import Background
from laser import Laser
import globals
import random

import cv2
import mediapipe as mp
import math

class Game:
    def __init__(self, level=1):
        self.level = level
        self.config = get_level_config(level)

        self.screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        self.clock = pygame.time.Clock()
        self.running = True
        self.started = True  # Inicia directamente

        #Facemesh
        self.mp_face_mesh = mp.solutions.face_mesh
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles

        pygame.init()
        pygame.display.set_caption("Misiles")

        # Imagen de explosión
        self.explosion_img = pygame.image.load("sprites/0009.png").convert_alpha()
        # Sonido de explosión
        self.explosion_sound = pygame.mixer.Sound("sprites/golpe10.mp3")
        self.explosion_sound.set_volume(0.10)
        # Imagen del láser
        self.laser_img = pygame.image.load("sprites/laser1.png").convert_alpha()
        # Sonido del laser
        self.laser_sound = pygame.mixer.Sound("sprites/laser01.mp3")
        self.laser_sound.set_volume(0.5)


        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.smaller_font = pygame.font.Font('freesansbold.ttf', 22)
        self.background = Background()

        self.initialize()

    def initialize(self):
        self.start_time = pygame.time.get_ticks()
        self.last_frame_time = self.start_time
        self.lives = 3  # Número de vidas
        self.invulnerable = False
        self.invulnerable_time = 0
        self.player = Player()
        self.movement = 0

        #Timers
        self.enemy_timer = 1000 - (self.config["missile_speed"] * 30)
        if self.enemy_timer < 50:
            self.enemy_timer = 50
        pygame.time.set_timer(ADD_ENEMY, int(self.enemy_timer))

        self.enemies = pygame.sprite.Group()
        self.lasers = pygame.sprite.Group()
        self.last_shot_time = 0  # Para evitar disparos múltiples por frame

        # Genera enemigos iniciales según el nivel
        for _ in range(self.config["enemy_count"]):
            enemy = Enemy()
            self.enemies.add(enemy)

        self.lost = False
        self.score = 0

        self.webcam = Webcam().start()
        
        self.max_face_surf_height=0
        self.face_left_x = 0
        self.face_right_x = 0
        self.face_top_y = 0
        self.face_bottom_y = 0

    def update(self, delta_time):
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False

        if not self.lost and self.started:
            # Aumentar la velocidad segun el tiempo que hemos durado
            globals.game_speed = 1 + ((pygame.time.get_ticks() - self.start_time) / 1000) * .1
            self.score = self.score + (delta_time * globals.game_speed)

            for event in events:
                if event.type == ADD_ENEMY:
                    #Agregar 3 o 6 enemigos
                    num = random.randint(3, 6)
                    for _ in range(num):
                        enemy = Enemy()
                        self.enemies.add(enemy)

                    #Actualizar el timer que define cuando aparecera un nuevo enemigo
                    self.enemy_timer = 600 - ((globals.game_speed - 1) * 80) - (self.config["missile_speed"] * 20)
                    if self.enemy_timer < 50:
                        self.enemy_timer = 50
                    pygame.time.set_timer(ADD_ENEMY, int(self.enemy_timer))

            self.player.update(self.movement, delta_time)
            self.enemies.update(delta_time)
            self.lasers.update(delta_time)
            self.process_collisions()
            self.background.update(delta_time)

            # Invulnerabilidad temporal tras perder una vida
            if self.invulnerable:
                if pygame.time.get_ticks() - self.invulnerable_time > 1000:  # 1 segundo
                    self.invulnerable = False

            # Condición de victoria: alcanzar los puntos requeridos por el nivel
            if self.score / 1000 >= self.config["points_to_win"]:
                self.running = False
                self.lost = False  # Ganaste

    def play_explosion(self, position):
        self.screen.fill((0,0,0))
        self.background.render(self.screen)
        self.screen.blit(self.explosion_img, self.explosion_img.get_rect(center=position))
        pygame.display.flip()
        pygame.time.delay(700)  # Muestra la explosión por 0.7 segundos

    def process_collisions(self):
        if self.invulnerable:
            return
        collide = pygame.sprite.spritecollide(self.player, self.enemies, False, pygame.sprite.collide_mask)
        if collide:
            self.lives -= 1
            if self.lives <= 0:
                self.explosion_sound.play()
                self.play_explosion(self.player.rect.center)
                self.lost = True
                self.running = False
            else:
                self.player.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60)
                self.invulnerable = True
                self.invulnerable_time = pygame.time.get_ticks()

        # Colisión láser-meteorito
        for laser in self.lasers:
            hit_enemies = pygame.sprite.spritecollide(laser, self.enemies, True, pygame.sprite.collide_mask)
            if hit_enemies:
                laser.kill()  # El láser desaparece al impactar

    def render(self):
        self.screen.fill((0,0,0))

        self.background.render(self.screen)
        
        if self.webcam.lastFrame is not None:
            self.render_camera()

        # Parpadeo del jugador cuando es invulnerable
        if not self.invulnerable or (pygame.time.get_ticks() // 100) % 2 == 0:
            self.screen.blit(self.player.surf, self.player.rect)

        # Dibuja lasers
        for laser in self.lasers:
            self.screen.blit(laser.image, laser.rect)

        # Dibuja vidas
        for i in range(self.lives):
            pygame.draw.circle(self.screen, (255,0,0), (SCREEN_WIDTH - 30 - (i * 30), 30), 10)

        for e in self.enemies:
            self.screen.blit(e.surf, e.rect)

        display_score = round(self.score/1000)
        text_score = self.font.render('Score: ' + str(display_score), True, (255,255,255))
        scoreTextRect = text_score.get_rect()
        scoreTextRect.bottom = SCREEN_HEIGHT-5
        scoreTextRect.left = 5
        self.screen.blit(text_score, scoreTextRect)

        if self.lost:
            game_over_text = self.font.render('GAME OVER :(', True, (255,255,255), (0,0,0))
            game_over_text_rect = game_over_text.get_rect()
            game_over_text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            self.screen.blit(game_over_text, game_over_text_rect)

            retry_text = self.smaller_font.render('Presiona Enter para volver al menú', True, (200,200,200), (0,0,0))
            retry_text_rect = retry_text.get_rect()
            retry_text_rect.center = (SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2) + 40)
            self.screen.blit(retry_text, retry_text_rect)

        pygame.display.flip()

    def show_win_screen(self):
        win_text = self.font.render('¡Nivel superado!', True, (0,255,0), (0,0,0))
        win_text_rect = win_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        continue_text = self.smaller_font.render('Presiona Enter para volver al menú', True, (200,200,200), (0,0,0))
        continue_text_rect = continue_text.get_rect(center=(SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2) + 40))
        self.screen.fill((0,0,0))
        self.screen.blit(win_text, win_text_rect)
        self.screen.blit(continue_text, continue_text_rect)
        pygame.display.flip()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    waiting = False

    def show_game_over_screen(self):
        game_over_text = self.font.render('GAME OVER :(', True, (255,255,255), (0,0,0))
        game_over_text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        retry_text = self.smaller_font.render('Presiona Enter para volver al menú', True, (200,200,200), (0,0,0))
        retry_text_rect = retry_text.get_rect(center=(SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2) + 40))
        self.screen.fill((0,0,0))
        self.screen.blit(game_over_text, game_over_text_rect)
        self.screen.blit(retry_text, retry_text_rect)
        pygame.display.flip()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    waiting = False

    def loop(self):
        with self.mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            min_detection_confidence=0.5,
            refine_landmarks=True
        ) as self.face_mesh, self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.5
        ) as self.hands:
            while self.running:
                if not self.lost:
                    if not self.webcam.ready():
                        continue
                    self.process_camera(self.hands)

                time = pygame.time.get_ticks()
                delta_time = time - self.last_frame_time
                self.last_frame_time = time
                self.update(delta_time)
                self.render()
                self.clock.tick(60)
            if not self.lost:
                self.show_win_screen()
                return "win"
            else:
                self.show_game_over_screen()
                return "lose"

    def process_camera(self, hands_detector):
        image = self.webcam.read()
        if image is not None:
            image.flags.writeable = False
            image = cv2.flip(image, 1)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            results = self.face_mesh.process(image)
            hand_results = hands_detector.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            self.webcam_image = image

            # --- Gesto de disparo con la mano ---
            if hand_results.multi_hand_landmarks is not None:
                for hand_landmarks in hand_results.multi_hand_landmarks:
                    if self.is_shoot_gesture(hand_landmarks, self.webcam.width(), self.webcam.height()):
                        now = pygame.time.get_ticks()
                        if now - self.last_shot_time > 100:  # 100 ms entre disparos
                            laser = Laser(self.player.rect.centerx, self.player.rect.top, self.laser_img)
                            self.lasers.add(laser)
                            self.laser_sound.play()
                            self.last_shot_time = now

            # --- Detección de rostro para movimiento ---
            if results.multi_face_landmarks is not None:
                for face_landmarks in results.multi_face_landmarks:
                    top = (face_landmarks.landmark[10].x, face_landmarks.landmark[10].y)
                    bottom = (face_landmarks.landmark[152].x, face_landmarks.landmark[152].y)
                    self.face_left_x = face_landmarks.landmark[234].x
                    self.face_right_x = face_landmarks.landmark[454].x
                    self.face_top_y = face_landmarks.landmark[10].y
                    self.face_bottom_y = face_landmarks.landmark[152].y
                    self.face_left_x = self.face_left_x - .1
                    self.face_right_x = self.face_right_x + .1
                    self.face_top_y = self.face_top_y - .1
                    self.face_bottom_y = self.face_bottom_y + .1
                    cv2.line(
                        self.webcam_image, 
                        (int(top[0] * self.webcam.width()), int(top[1] * self.webcam.height())),
                        (int(bottom[0] * self.webcam.width()), int(bottom[1] * self.webcam.height())),
                        (0, 255, 0), 3
                    )
                    cv2.circle(self.webcam_image, (int(top[0] * self.webcam.width()), int(top[1] * self.webcam.height())), 8, (0,0,255), -1)
                    cv2.circle(self.webcam_image, (int(bottom[0] * self.webcam.width()), int(bottom[1] * self.webcam.height())), 8, (0,0,255), -1)
                    self.detect_head_movement(top, bottom)

            k = cv2.waitKey(1) & 0xFF

    def is_shoot_gesture(self, hand_landmarks, image_width, image_height):
        # Pulgar: landmark 4, Índice: landmark 8
        thumb_tip = hand_landmarks.landmark[4]
        index_tip = hand_landmarks.landmark[8]
        x1, y1 = int(thumb_tip.x * image_width), int(thumb_tip.y * image_height)
        x2, y2 = int(index_tip.x * image_width), int(index_tip.y * image_height)
        distance = ((x2 - x1)**2 + (y2 - y1)**2) ** 0.5
        return distance < 40  # Ajusta el umbral según tu cámara

    def detect_head_movement(self, top, bottom):
        radians = math.atan2(bottom[1] - top[1], bottom[0] - top[0])
        degrees = math.degrees(radians)
        min_degrees = 70
        max_degrees = 110
        degree_range = max_degrees - min_degrees
        if degrees < min_degrees: degrees = min_degrees
        if degrees > max_degrees: degrees = max_degrees
        self.movement = ( ((degrees-min_degrees) / degree_range) * 2) - 1

    def render_camera(self):        
        if self.face_left_x < 0: self.face_left_x = 0
        if self.face_right_x > 1: self.face_right_x = 1
        if self.face_top_y < 0: self.face_top_y = 0
        if self.face_bottom_y > 1: self.face_bottom_y = 1

        face_surf = pygame.image.frombuffer(self.webcam_image, (int(self.webcam.width()), int(self.webcam.height())), "BGR")

        face_rect = pygame.Rect(
            int(self.face_left_x*self.webcam.width()),
            int(self.face_top_y*self.webcam.height()), 
            int(self.face_right_x*self.webcam.width()) - int(self.face_left_x*self.webcam.width()),
            int(self.face_bottom_y*self.webcam.height()) - int(self.face_top_y*self.webcam.height())
        )
        
        only_face_surf = pygame.Surface((
            int(self.face_right_x*self.webcam.width()) - int(self.face_left_x*self.webcam.width()),
            int(self.face_bottom_y*self.webcam.height()) - int(self.face_top_y*self.webcam.height())
        ))
        only_face_surf.blit(face_surf, (0,0), face_rect)

        height = only_face_surf.get_rect().height
        width = only_face_surf.get_rect().width
        if width == 0:
            width = 1        
        face_ratio =  height / width
        face_area_width = 130
        face_area_height = face_area_width * face_ratio
        if (face_area_height > self.max_face_surf_height):
            self.max_face_surf_height = face_area_height
        only_face_surf = pygame.transform.scale(only_face_surf, (int(face_area_width),int(self.max_face_surf_height)))
        self.screen.blit(only_face_surf, only_face_surf.get_rect())