import pygame
import math

class Bullet:
    def __init__(self, x, y, size, damage, velocity_x, velocity_y):
        self.x = x
        self.y = y
        self.size = size
        self.damage = damage
        self.velocity = {'x': velocity_x, 'y': velocity_y}
        self.active = True
        self.speed = 1  # Mermi hızını artırdık
    
    def update(self, game_map):
        if not self.active:
            return
            
        # Çok küçük adımlarla hareket et
        STEP_COUNT = 20  # Çok daha fazla adım
        dx = self.velocity['x'] * self.speed / STEP_COUNT
        dy = self.velocity['y'] * self.speed / STEP_COUNT
        
        for _ in range(STEP_COUNT):
            # Sonraki pozisyonu hesapla
            next_x = self.x + dx
            next_y = self.y + dy
            
            # Mermi için 4 köşe noktası kontrol et
            check_points = [
                (next_x - self.size/2, next_y - self.size/2),  # Sol üst
                (next_x + self.size/2, next_y - self.size/2),  # Sağ üst
                (next_x - self.size/2, next_y + self.size/2),  # Sol alt
                (next_x + self.size/2, next_y + self.size/2)   # Sağ alt
            ]
            
            # Herhangi bir nokta duvara çarparsa mermiyi yok et
            collision = False
            for point_x, point_y in check_points:
                point_rect = pygame.Rect(point_x - 1, point_y - 1, 2, 2)
                if game_map.check_collision(point_rect):
                    collision = True
                    break
            
            if collision:
                self.active = False
                return
            
            # Çarpışma yoksa pozisyonu güncelle
            self.x = next_x
            self.y = next_y
        
        # Harita sınırlarını kontrol et
        if (self.x < 0 or self.x > game_map.width * game_map.tile_size or
            self.y < 0 or self.y > game_map.height * game_map.tile_size):
            self.active = False
    
    def draw(self, screen, camera_x=0, camera_y=0):
        if not self.active:
            return
            
        screen_x = int(self.x - camera_x)
        screen_y = int(self.y - camera_y)
        
        # Ekran dışındaysa çizme
        if (screen_x < -self.size or screen_x > screen.get_width() or
            screen_y < -self.size or screen_y > screen.get_height()):
            return
            
        # Mermiyi çiz
        pygame.draw.circle(screen, (255, 255, 0), 
                         (screen_x, screen_y), 
                         self.size)
    
    def check_collision(self, entity):
        if not self.active:
            return False
            
        # Geliştirilmiş çarpışma kontrolü
        bullet_center_x = self.x
        bullet_center_y = self.y
        entity_center_x = entity.x
        entity_center_y = entity.y
        
        # Mermi ve zombi arasındaki mesafeyi hesapla
        distance = math.sqrt((bullet_center_x - entity_center_x)**2 + 
                           (bullet_center_y - entity_center_y)**2)
        
        # Eğer mesafe mermi boyutu + zombi boyutunun yarısından küçükse çarpışma var
        collision_distance = self.size + min(entity.width, entity.height)/3
        if distance < collision_distance:
            self.active = False
            return True
        return False 