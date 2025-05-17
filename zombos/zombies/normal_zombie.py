import pygame
import math
from entity import Entity
import random
import os

class NormalZombie(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, 32, 32, 50)  # Normal size: 32x32
        self.damage = 15
        self.color = (0, 255, 0)  # Green
        self.attack_range = 40
        self.attack_cooldown = 1000  # 1 second
        self.last_attack = 0
        self.max_speed = 3
        self.load_animation("walk", "zombie_walk_horizontal.png", 8, 60000, (96, 96))  # Boyut ve delay arttı
        
        # Load sprite sheet (3x3 grid, 8 frames)
        """ try:
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            sprite_path = os.path.join(base_path, "assets", "zombie_walk_horizontal.png")
            sprite_sheet = pygame.image.load(sprite_path).convert_alpha()
            
            # Scale sprite sheet to match entity size
            original_frame_size = sprite_sheet.get_height() // 3  # Height of one frame
            scale_factor = self.height / original_frame_size
            new_width = int(sprite_sheet.get_width() * scale_factor)
            new_height = int(sprite_sheet.get_height() * scale_factor)
            scaled_sheet = pygame.transform.scale(sprite_sheet, (new_width, new_height))
            
            # Load walk animation with 3 columns
            self.load_animation("walk", scaled_sheet, self.width, self.height, 8, 100, columns=3)
        except Exception as e:
            print(f"Failed to load zombie sprite sheet! Error: {e}")
            print(f"Attempted path: {sprite_path}")
            self.sprite_sheet = None
    """
    def update(self, player, game_map, current_time):
        if not player.is_alive:
            return
            
        # Calculate distance to player
        dx = player.x - self.x
        dy = player.y - self.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        # If not in attack range, move towards player
        if distance > self.attack_range:
            # Pathfinding and movement
            self.update_path(player.x, player.y, game_map, current_time)
            self.move(game_map)
            
            """# Update facing direction based on movement
            if self.velocity['x'] != 0:
                self.facing_right = self.velocity['x'] > 0"""
            
            # Play walk animation
            self.play_animation("walk")
            self.update_animation(current_time)
        else:
            # Attack if in range and cooldown is over
            if current_time - self.last_attack >= self.attack_cooldown:
                self.last_attack = current_time
            # Saldırı mesafesindeyse ve cooldown bittiyse saldır
            if current_time - self.last_attack > self.attack_cooldown:
                player.take_damage(self.damage)
                self.last_attack = current_time
        
        # Animasyonu güncelle
        self.update_animation(current_time)
