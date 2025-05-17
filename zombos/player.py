import pygame
import math
from entity import Entity
from animation import Animation

class Player(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, width=60, height=60, health=100)  # Hitbox boyutu orijinal
        self.speed = 300
        self.equipped_gun = None
        self.is_moving = False
        self.is_alive = True
        self.visual_size = (120, 120)  # Görsel boyut ayrı tutulacak
        
        # Animasyonları yükle (görsel boyut büyük)
        self.load_animation("idle", "enemy1.png", 1, 150, self.visual_size)
        self.load_animation("walk", "player_walk.png", 5, 80, self.visual_size)
    
    def update(self, keys, mouse_pos, camera_x, camera_y, game_map):
        if not self.is_alive:
            return
            
        old_x, old_y = self.x, self.y
        movement = [0, 0]
        
        # Tuş kontrollerini işle
        if keys[pygame.K_w]: movement[1] -= 1
        if keys[pygame.K_s]: movement[1] += 1
        if keys[pygame.K_a]: movement[0] -= 1
        if keys[pygame.K_d]: movement[0] += 1
        
        # Mouse pozisyonuna göre açıyı hesapla
        mouse_x = mouse_pos[0] + camera_x
        mouse_y = mouse_pos[1] + camera_y
        dx = mouse_x - self.x
        dy = mouse_y - self.y
        self.angle = math.atan2(dy, dx)
        
        # Mouse yönüne göre karakterin yönünü belirle
        self.facing_right = dx > 0
        
        # Hareket varsa normalize et
        if any(movement):
            length = math.sqrt(movement[0]**2 + movement[1]**2)
            if length != 0:
                movement[0] /= length
                movement[1] /= length
            
            # Pozisyonu güncelle
            self.x += movement[0] * self.speed * (1/60)
            self.y += movement[1] * self.speed * (1/60)
            
            # Yürüme animasyonunu oynat
            if self.current_animation != "walk":
                self.current_animation = "walk"
        else:
            # Durma animasyonunu oynat
            if self.current_animation != "idle":
                self.current_animation = "idle"
        
        # Çarpışma kontrolü (hitbox boyutuyla)
        player_rect = pygame.Rect(
            self.x - self.width/2,
            self.y - self.height/2,
            self.width,
            self.height
        )
        
        if game_map.check_collision(player_rect):
            self.x, self.y = old_x, old_y
        
        # Animasyonu güncelle
        if self.current_animation:
            self.animations[self.current_animation].update(16.67)
    
    def draw(self, screen, camera_x, camera_y):
        if not self.is_alive:
            return

        if self.current_animation and self.animations[self.current_animation]:
            # Döndürülmemiş frame'i al
            frame = self.animations[self.current_animation].get_current_frame()
            
            # Sprite'ı mouse yönüne göre döndür
            angle_degrees = -math.degrees(self.angle)
            rotated_frame = pygame.transform.rotate(frame, angle_degrees)
            
            # Ekran koordinatlarını hesapla
            screen_pos = (self.x - camera_x, self.y - camera_y)
            rotated_rect = rotated_frame.get_rect(center=screen_pos)

            # Sprite'ı çiz
            screen.blit(rotated_frame, rotated_rect.topleft)

            # Silahı çiz (opsiyonel)
            if self.equipped_gun:
                gun_length = 40
                gun_thickness = 4
                gun_end = (
                    self.x + gun_length * math.cos(self.angle),
                    self.y + gun_length * math.sin(self.angle)
                )
                pygame.draw.line(screen,
                                (0, 0, 0),
                                (self.x - camera_x, self.y - camera_y),
                                (gun_end[0] - camera_x, gun_end[1] - camera_y),
                                gun_thickness)

            # Can barı çizimi
            bar_width = 50
            bar_height = 6
            health_ratio = self.health / self.max_health
            health_width = bar_width * health_ratio

            bar_x = screen_pos[0] - bar_width // 2
            bar_y = screen_pos[1] - bar_height // 2 - 60  # Sprite üstüne yerleştirildi

            # Arka plan (kırmızı)
            pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))
            # Mevcut can (yeşil)
            pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, health_width, bar_height))


    def equip_gun(self, gun):
        self.equipped_gun = gun
    
    def shoot(self):
        if self.equipped_gun and self.is_alive:
            gun_end = (
                self.x + 40 * math.cos(self.angle),
                self.y + 40 * math.sin(self.angle)
            )
            return self.equipped_gun.shoot(gun_end[0], gun_end[1], self.angle)
        return None
        
    def take_damage(self, amount):
        super().take_damage(amount)
        if self.health <= 0:
            self.is_alive = False
        return not self.is_alive
