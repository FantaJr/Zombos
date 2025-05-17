import pygame
import random
from medkit import Medkit
from pathfinding import PathFinder
import math

class Map:
    def __init__(self, width, height, tile_size=96):
        self.width = width
        self.height = height
        self.tile_size = tile_size
        self.grid = [[0 for _ in range(height)] for _ in range(width)]
        self.obstacles = []
        self.medkits = []
        self.zombie_kill_count = 0
        
        # Engelleri rastgele yerleştir
        self.generate_obstacles()
        
        # Pathfinder'ı başlat
        self.pathfinder = PathFinder(self)
        self.wall_image = pygame.image.load("assets/wall.png").convert_alpha()
        self.wall_image = pygame.transform.scale(self.wall_image, (tile_size, tile_size))
        self.ground_image = pygame.image.load("assets/ground.png").convert_alpha()
        self.ground_image = pygame.transform.scale(self.ground_image, (tile_size, tile_size))
    
    def generate_obstacles(self):
        # Haritanın %10'u engel olsun (daha da az engel)
        obstacle_count = int((self.width * self.height) * 0.10)
        
        # Kenarları duvar yap
        for x in range(self.width):
            self.grid[x][0] = 1
            self.grid[x][self.height-1] = 1
        for y in range(self.height):
            self.grid[0][y] = 1
            self.grid[self.width-1][y] = 1
        
        # Rastgele engeller ekle
        placed = 0
        while placed < obstacle_count:
            x = random.randint(2, self.width-3)
            y = random.randint(2, self.height-3)
            
            # Spawn alanını boş bırak (haritanın ortası)
            center_x = self.width // 2
            center_y = self.height // 2
            if abs(x - center_x) <= 3 and abs(y - center_y) <= 3:
                continue
                
            if self.grid[x][y] == 0:
                self.grid[x][y] = 1
                placed += 1
    
    def is_wall(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[x][y] == 1
        return True
    
    def check_collision(self, rect):
        # Çarpışma kontrolünü geliştir
        # Biraz boşluk bırak ki karakterler sıkışmasın
        padding = 5
        rect = rect.inflate(-padding, -padding)
        
        # Dikdörtgenin kapladığı kareleri kontrol et
        start_x = max(0, int(rect.left / self.tile_size))
        end_x = min(self.width, int(rect.right / self.tile_size) + 1)
        start_y = max(0, int(rect.top / self.tile_size))
        end_y = min(self.height, int(rect.bottom / self.tile_size) + 1)
        
        for x in range(start_x, end_x):
            for y in range(start_y, end_y):
                if self.grid[x][y] == 1:
                    wall_rect = pygame.Rect(x * self.tile_size, y * self.tile_size,
                                          self.tile_size, self.tile_size)
                    if rect.colliderect(wall_rect):
                        return True
        return False
    
    def get_spawn_position(self):
        attempts = 0
        max_attempts = 300
        
        while attempts < max_attempts:
            # Kenarlardan birini seç
            if random.random() < 0.5:
                # Sol veya sağ kenar (biraz içeriden)
                x = 1 if random.random() < 0.5 else self.width - 2
                y = random.randint(1, self.height - 2)
            else:
                # Üst veya alt kenar (biraz içeriden)
                x = random.randint(1, self.width - 2)
                y = 1 if random.random() < 0.5 else self.height - 2
            
            # Eğer bu nokta engel değilse kullan
            if not self.is_wall(x, y):
                # Piksel koordinatlarına çevir
                pixel_x = x * self.tile_size + self.tile_size/2
                pixel_y = y * self.tile_size + self.tile_size/2
                return pixel_x, pixel_y
                
            attempts += 1
        
        # Eğer uygun yer bulunamadıysa, varsayılan olarak sol üst köşeye yakın bir yer
        return self.tile_size * 1.5, self.tile_size * 1.5
    
    def spawn_medkit(self, x, y):
        # Koordinatları kare koordinatlarına çevir
        tile_x = int(x / self.tile_size)
        tile_y = int(y / self.tile_size)
        
        # Eğer engel yoksa medkit ekle
        if not self.is_wall(tile_x, tile_y):
            # Piksel koordinatlarına geri çevir (karenin ortası)
            pixel_x = tile_x * self.tile_size + self.tile_size/2
            pixel_y = tile_y * self.tile_size + self.tile_size/2
            self.medkits.append((pixel_x, pixel_y, 30))
    
    def update(self, player):
        # Medkit toplama kontrolü
        for medkit in self.medkits[:]:
            x, y, heal = medkit
            # Oyuncu medkite yeterince yakınsa
            dx = player.x - x
            dy = player.y - y
            if math.sqrt(dx*dx + dy*dy) < 40:  # Toplama mesafesini daha da artırdık
                player.heal(heal)
                self.medkits.remove(medkit)
    
    def draw(self, screen, camera_x=0, camera_y=0):
        # Görünür alanı hesapla
        view_left = max(0, int(camera_x / self.tile_size))
        view_right = min(self.width, int((camera_x + screen.get_width()) / self.tile_size) + 1)
        view_top = max(0, int(camera_y / self.tile_size))
        view_bottom = min(self.height, int((camera_y + screen.get_height()) / self.tile_size) + 1)
        
        # Sadece görünür kareleri çiz
        for x in range(view_left, view_right):
            for y in range(view_top, view_bottom):
                screen_x = x * self.tile_size - camera_x
                screen_y = y * self.tile_size - camera_y
                
                # Zemin rengi (açık gri)
                screen.blit(self.ground_image, (screen_x, screen_y))
                
                """# Izgara çizgileri (koyu gri)
                pygame.draw.rect(screen, (50, 50, 50),
                               (screen_x, screen_y,
                                self.tile_size, self.tile_size), 1)"""
                
                if self.grid[x][y] == 1:
                    screen.blit(self.wall_image, (screen_x, screen_y))

        
        # Medkitleri çiz (sadece görünür olanları)
        for x, y, _ in self.medkits:
            screen_x = x - camera_x - 24  # 48x48 piksel için ortalama
            screen_y = y - camera_y - 24
            
            # Ekran dışındaysa çizme
            if (screen_x < -48 or screen_x > screen.get_width() or
                screen_y < -48 or screen_y > screen.get_height()):
                continue
            
            # Medkit kutusunu çiz (daha da büyük)
            pygame.draw.rect(screen, (255, 0, 0),  # Kırmızı kare
                           (screen_x, screen_y, 48, 48))
            # Beyaz artı
            pygame.draw.rect(screen, (255, 255, 255),
                           (screen_x + 18, screen_y + 6, 12, 36))
            pygame.draw.rect(screen, (255, 255, 255),
                           (screen_x + 6, screen_y + 18, 36, 12))
    
    def on_zombie_killed(self, x, y):
        self.zombie_kill_count += 1
        if self.zombie_kill_count % 3 == 0:  # Her 3 zombide bir medkit
            self.spawn_medkit(x, y) 