import pygame
import math
from animation import Animation

class Entity:
    def __init__(self, x, y, width, height, health=100):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.health = health
        self.max_health = health
        self.velocity = {'x': 0, 'y': 0}
        self.acceleration = {'x': 0, 'y': 0}
        self.max_speed = 5
        self.acceleration_rate = 0.5
        self.friction = 0.1
        self.angle = 0
        self.collision_cooldown = 0
        self.path = []
        self.path_index = 0
        self.path_update_timer = 0
        self.path_update_delay = 500  # Her 500ms'de bir yol güncelleme

        # Animasyon değişkenleri
        self.animations = {}
        self.current_animation = None
        #self.facing_right = True
        #self.facing_up = True

    def load_animation(self, name, sprite_sheet_path, frame_count, frame_delay, sprite_size, is_spritesheet=True):
        self.animations[name] = Animation(sprite_sheet_path, frame_count, frame_delay, sprite_size, is_spritesheet)
        if not self.current_animation:
            self.current_animation = name

    def play_animation(self, name):
        if name in self.animations and self.current_animation != name:
            self.current_animation = name
            self.animations[name].reset()

    def update_facing_direction(self):
        if abs(self.velocity['x']) > 0.1 or abs(self.velocity['y']) > 0.1:
            angle = math.atan2(self.velocity['y'], self.velocity['x'])
            #self.facing_right = math.cos(angle) > 0
            #self.facing_up = math.sin(angle) < 0

    def update_animation(self, current_time):
        if self.current_animation:
            self.animations[self.current_animation].update(current_time)
            #self.animations[self.current_animation].flip_x = not self.facing_right
            #self.animations[self.current_animation].flip_y = not self.facing_up

        """ # Hareket yönüne göre animasyon seçimi
        if abs(self.velocity['x']) > 0.1 or abs(self.velocity['y']) > 0.1:
            if abs(self.velocity['y']) > abs(self.velocity['x']):
                if self.facing_up:
                    self.play_animation("walk_up")
                else:
                    self.play_animation("walk_down")
            else:
                if self.facing_right:
                    self.play_animation("walk_right")
                else:
                    self.play_animation("walk_left")"""

    def update_path(self, target_x, target_y, game_map, current_time):
        # Yol güncellemesi için zaman kontrolü
        if current_time - self.path_update_timer > self.path_update_delay:
            self.path = game_map.pathfinder.get_path(self.x, self.y, target_x, target_y)
            self.path_index = 0
            self.path_update_timer = current_time

        # Eğer geçerli bir yol varsa, o yolu takip et
        if self.path and self.path_index < len(self.path):
            next_x, next_y = self.path[self.path_index]

            # Bir sonraki noktaya yeterince yaklaştıysak, sonraki noktaya geç
            distance_to_next = math.sqrt((next_x - self.x)**2 + (next_y - self.y)**2)
            if distance_to_next < self.max_speed:
                self.path_index += 1
            else:
                self.apply_acceleration(next_x, next_y)
        else:
            # Doğrudan hedefe git (yol bulunamadıysa)
            self.apply_acceleration(target_x, target_y)

    def apply_acceleration(self, target_x, target_y):
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx*dx + dy*dy)

        if distance > 0:
            self.acceleration['x'] = (dx/distance) * self.acceleration_rate
            self.acceleration['y'] = (dy/distance) * self.acceleration_rate

    def move(self, game_map):
        # İvmeyi hıza uygula
        self.velocity['x'] += self.acceleration['x']
        self.velocity['y'] += self.acceleration['y']

        # Maksimum hız kontrolü
        speed = math.sqrt(self.velocity['x']**2 + self.velocity['y']**2)
        if speed > self.max_speed:
            self.velocity['x'] = (self.velocity['x'] / speed) * self.max_speed
            self.velocity['y'] = (self.velocity['y'] / speed) * self.max_speed

        # Sürtünme uygula
        self.velocity['x'] *= (1 - self.friction)
        self.velocity['y'] *= (1 - self.friction)

        # X ekseni hareketi
        new_x = self.x + self.velocity['x']
        hitbox_x = pygame.Rect(
            new_x - self.width/2,
            self.y - self.height/2,
            self.width,
            self.height
        )
        if not game_map.check_collision(hitbox_x):
            self.x = new_x
        else:
            self.velocity['x'] = 0

        # Y ekseni hareketi
        new_y = self.y + self.velocity['y']
        hitbox_y = pygame.Rect(
            self.x - self.width/2,
            new_y - self.height/2,
            self.width,
            self.height
        )
        if not game_map.check_collision(hitbox_y):
            self.y = new_y
        else:
            self.velocity['y'] = 0

        # İvmeyi sıfırla
        self.acceleration['x'] = 0
        self.acceleration['y'] = 0

        # Yönü güncelle
        self.update_facing_direction()

    def draw(self, screen, camera_x, camera_y):
        if self.current_animation and self.animations[self.current_animation]:
            # Dönmeden önce çerçeveyi al
            frame = self.animations[self.current_animation].get_current_frame()

            # Sprite'ı açıya göre döndür
            rotated_frame = pygame.transform.rotozoom(frame, -math.degrees(self.angle), 1.0)

            # Yeni döndürülmüş görselin ortasını ayarla
            frame_rect = rotated_frame.get_rect()
            screen_x = self.x - camera_x - frame_rect.width // 2
            screen_y = self.y - camera_y - frame_rect.height // 2

            screen.blit(rotated_frame, (screen_x, screen_y))

            # Can barı
            bar_width = 50
            bar_height = 5
            health_width = (self.health / self.max_health) * bar_width

            pygame.draw.rect(screen, (255, 0, 0),
                            (screen_x + frame_rect.width / 2 - bar_width / 2,
                            screen_y - 10, bar_width, bar_height))
            pygame.draw.rect(screen, (0, 255, 0),
                            (screen_x + frame_rect.width / 2 - bar_width / 2,
                            screen_y - 10, health_width, bar_height))


    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            return True
        return False

    def heal(self, amount):
        self.health = min(self.health + amount, self.max_health)

    def look_at(self, target_x, target_y):
        dx = target_x - self.x
        dy = target_y - self.y
        self.angle = math.atan2(dy, dx)

    def get_position(self):
        return (self.x, self.y)
