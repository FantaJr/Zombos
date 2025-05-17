import pygame
import math
from bullet import Bullet

class Gun:
    def __init__(self, damage, bullet_speed, fire_rate, bullet_size=2):
        self.damage = damage
        self.bullet_speed = bullet_speed
        self.fire_rate = fire_rate  # Saniyede kaç mermi
        self.bullet_size = bullet_size
        self.last_shot_time = 0
    
    def shoot(self, x, y, angle):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > 1000 / self.fire_rate:
            self.last_shot_time = current_time
            
            # Mermi hızını hesapla
            velocity_x = math.cos(angle) * self.bullet_speed
            velocity_y = math.sin(angle) * self.bullet_speed
            
            # Yeni mermi oluştur
            return Bullet(x, y, self.bullet_size, self.damage, velocity_x, velocity_y)
        return None

class Pistol(Gun):
    def __init__(self):
        super().__init__(damage=10, bullet_speed=10, fire_rate=2)

class Shotgun(Gun):
    def __init__(self):
        super().__init__(damage=20, bullet_speed=8, fire_rate=1)
    
    def shoot(self, x, y, angle):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > 1000 / self.fire_rate:
            self.last_shot_time = current_time
            bullets = []
            
            # 5 mermi, her biri farklı açıda
            for i in range(-2, 3):
                spread_angle = angle + math.radians(i * 10)
                velocity_x = math.cos(spread_angle) * self.bullet_speed
                velocity_y = math.sin(spread_angle) * self.bullet_speed
                bullets.append(Bullet(x, y, self.bullet_size, self.damage, velocity_x, velocity_y))
            
            return bullets
        return None

class MachineGun(Gun):
    def __init__(self):
        super().__init__(damage=5, bullet_speed=12, fire_rate=10) 