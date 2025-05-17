import pygame
import random
import math
from player import Player
from gun import Pistol, Shotgun, MachineGun
from zombies.normal_zombie import NormalZombie
from zombies.fast_zombie import FastZombie
from zombies.tank_zombie import TankZombie
from map import Map
import traceback
from animation import Animation

# Pygame başlat
pygame.init()

# Ekran ayarları
info = pygame.display.Info()
SCREEN_WIDTH = info.current_w
SCREEN_HEIGHT = info.current_h
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Zombi Oyunu")

# FPS ayarı
clock = pygame.time.Clock()

# Renkler
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Harita oluştur (25x25 kare)
game_map = Map(50, 50)

# Oyun nesneleri
player = Player(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
player.equip_gun(Shotgun())  # Başlangıç silahı

zombies = []
bullets = []

# Oyun değişkenleri
score = 0
wave = 0
zombies_in_wave = 0
wave_completed = True
spawn_timer = 0
spawn_delay = 2000  # 2 saniye
game_over = False
running = True

# Kamera pozisyonu
camera_x = 0
camera_y = 0
"""
# Animasyonları yükle
try:
    # Zombi animasyonları için sprite sheet'leri yükle
    zombie_animation = Animation('zombie_walk_horizontal.png', 8, 600, (32, 32), is_spritesheet=True)
    tank_animation = Animation('tank_walk_horizontal.png', 8, 600, (48, 48), is_spritesheet=True)
    
    # Oyuncu animasyonu (ayrı frame'ler)
    player_animation = Animation('enemy', 6, 150, (80, 80), is_spritesheet=False)
except Exception as e:
    print(f"Animation loading error: {e}")
    print(traceback.format_exc())"""

# Font
font = pygame.font.Font(None, 36)

def draw_game_over():
    # Yarı saydam siyah overlay
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.fill(BLACK)
    overlay.set_alpha(128)
    screen.blit(overlay, (0, 0))
    
    # Game Over yazısı
    game_over_text = font.render("GAME OVER", True, RED)
    score_text = font.render(f"Final Skor: {score}", True, WHITE)
    wave_text = font.render(f"Son Dalga: {wave}", True, WHITE)
    restart_text = font.render("Yeniden başlamak için SPACE'e basın", True, WHITE)
    
    screen.blit(game_over_text, 
                (SCREEN_WIDTH//2 - game_over_text.get_width()//2, 
                 SCREEN_HEIGHT//2 - 60))
    screen.blit(score_text, 
                (SCREEN_WIDTH//2 - score_text.get_width()//2, 
                 SCREEN_HEIGHT//2))
    screen.blit(wave_text, 
                (SCREEN_WIDTH//2 - wave_text.get_width()//2, 
                 SCREEN_HEIGHT//2 + 40))
    screen.blit(restart_text, 
                (SCREEN_WIDTH//2 - restart_text.get_width()//2, 
                 SCREEN_HEIGHT//2 + 100))

def reset_game():
    global player, zombies, bullets, score, wave, zombies_in_wave, wave_completed, spawn_timer ,game_over
    
    player = Player(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
    player.equip_gun(Pistol())
    zombies = []
    bullets = []
    score = 0
    wave = 0
    zombies_in_wave = 0
    wave_completed = True
    spawn_timer = 0
    game_over = False

def start_new_wave():
    global wave, zombies_in_wave, wave_completed, spawn_timer
    wave_completed = False
    zombies_in_wave = wave * 5  # Her wave'de 5 zombi daha fazla
    spawn_timer = pygame.time.get_ticks()

while running:
    # FPS ayarı
    clock.tick(60)
    current_time = pygame.time.get_ticks()
    
    # Event kontrolü
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE and game_over:
                reset_game()
            elif not game_over:
                # Silah değiştirme
                if event.key == pygame.K_1:
                    player.equip_gun(Pistol())
                elif event.key == pygame.K_2:
                    player.equip_gun(Shotgun())
                elif event.key == pygame.K_3:
                    player.equip_gun(MachineGun())
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            # Ateş et
            new_bullets = player.shoot()
            if isinstance(new_bullets, list):
                bullets.extend(new_bullets)
            elif new_bullets:
                bullets.append(new_bullets)
    
    if not game_over:
        # Kamera pozisyonunu güncelle
        camera_x = player.x - SCREEN_WIDTH//2
        camera_y = player.y - SCREEN_HEIGHT//2
        
        # Mouse pozisyonunu al ve açıyı hesapla
        mouse_pos = pygame.mouse.get_pos()
        mouse_x = mouse_pos[0] + camera_x
        mouse_y = mouse_pos[1] + camera_y
        angle = math.atan2(mouse_y - player.y, mouse_x - player.x)
        player.angle = angle  # Karakterin açısını güncelle
        
        # Wave kontrolü
        if wave_completed and not zombies:
            wave += 1
            start_new_wave()
        
        # Zombi spawn kontrolü
        if not wave_completed and zombies_in_wave > 0 and current_time - spawn_timer > spawn_delay:
            spawn_timer = current_time
            
            # Spawn pozisyonu al
            x, y = game_map.get_spawn_position()
            
            # Rastgele zombi türü
            zombie_type = random.randint(0, 100)
            if zombie_type < 60:  # %60 normal
                zombie = NormalZombie(x, y)
                #zombie.load_animation("walk", "zombie_walk_horizontal.png", 8, 600, (96, 96))  # Boyut ve delay arttı
            elif zombie_type < 90:  # %30 hızlı
                zombie = FastZombie(x, y)
                #zombie.load_animation("walk", "zombie_walk_horizontal.png", 8, 600, (72, 72))  # Boyut ve delay arttı
            else:  # %10 tank
                zombie = TankZombie(x, y)
                #zombie.load_animation("walk", "tank_walk_horizontal.png", 8, 600, (144, 144))  # Boyut ve delay arttı
            
            zombies.append(zombie)
            zombies_in_wave -= 1
            
            if zombies_in_wave <= 0:
                wave_completed = True
        
        # Zombileri güncelle
        for zombie in zombies[:]:
            # Zombinin hareket yönüne göre açısını güncelle
            if zombie.velocity['x'] != 0 or zombie.velocity['y'] != 0:
                zombie.angle = math.atan2(zombie.velocity['y'], zombie.velocity['x'])
            zombie.update(player, game_map, current_time)
        
        # Oyuncu güncelleme
        keys = pygame.key.get_pressed()
        player.update(keys, mouse_pos, camera_x, camera_y, game_map)
        
        # Mermileri güncelle
        for bullet in bullets[:]:
            bullet.update(game_map)  # game_map parametresini ekledik
            
            # Ekran dışına çıkan mermileri sil
            if (bullet.x < -50 or bullet.x > game_map.width * game_map.tile_size + 50 or
                bullet.y < -50 or bullet.y > game_map.height * game_map.tile_size + 50):
                bullets.remove(bullet)
                continue
            
            # Zombi vuruş kontrolü
            for zombie in zombies[:]:
                if bullet.check_collision(zombie):
                    if zombie.take_damage(bullet.damage):
                        zombies.remove(zombie)
                        score += 10
                        # Zombi öldüğünde medkit spawn kontrolü
                        if random.random() < 0.1:  # %10 şans
                            game_map.spawn_medkit(zombie.x, zombie.y)
                    break
        
        # Haritayı güncelle
        game_map.update(player)
        
        # Oyuncu ölüm kontrolü
        if not player.is_alive:
            game_over = True
    
    # Ekranı temizle
    screen.fill(BLACK)
    
    # Haritayı çiz
    game_map.draw(screen, camera_x, camera_y)
    
    # Mermileri çiz
    for bullet in bullets:
        bullet.draw(screen, camera_x, camera_y)
    
    # Zombileri çiz
    for zombie in zombies:
        zombie.draw(screen, camera_x, camera_y)
    
    # Oyuncuyu çiz
    player.draw(screen, camera_x, camera_y)
    
    # Skor ve dalga bilgisi
    score_text = font.render(f'Skor: {score}', True, WHITE)
    wave_text = font.render(f'Dalga: {wave}', True, WHITE)
    health_text = font.render(f'Can: {player.health}/{player.max_health}', True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(wave_text, (10, 50))
    screen.blit(health_text, (10, 90))
    
    # Game Over ekranı
    if game_over:
        draw_game_over()
    
    # Ekranı güncelle
    pygame.display.flip()

pygame.quit()
