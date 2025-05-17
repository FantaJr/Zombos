import pygame
import math
from entity import Entity
import random
import os

class FastZombie(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, 24, 24, 30)  # Smaller size: 24x24
        self.damage = 15
        self.color = (255, 165, 0)  # Orange
        self.attack_range = 35
        self.attack_cooldown = 800  # 0.8 seconds
        self.last_attack = 0
        self.max_speed = 6  # Faster
        self.load_animation("walk", "zombie_walk_horizontal.png", 8, 60000, (72, 72))  # Boyut ve delay arttı
        """
        # Load fast zombie sprite sheet (3x3 grid, 8 frames)
        try:
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
            self.load_animation("walk", scaled_sheet, self.width, self.height, 8, 80, columns=3)  # Faster animation
        except Exception as e:
            print(f"Failed to load fast zombie sprite sheet! Error: {e}")
            print(f"Attempted path: {sprite_path}")
            self.sprite_sheet = None"""
    
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
            
            # Update facing direction based on movement
            """if self.velocity['x'] != 0:
                self.facing_right = self.velocity['x'] > 0"""
            
            # Play walk animation
            self.play_animation("walk")
            self.update_animation(current_time)
        else:
            # Attack if in range and cooldown is over
            if current_time - self.last_attack >= self.attack_cooldown:
                self.last_attack = current_time
                player.take_damage(self.damage)
