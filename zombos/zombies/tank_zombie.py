import pygame
import math
from entity import Entity
import random
import os

class TankZombie(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, 48, 48, 200)  # Larger size: 48x48
        self.damage = 35
        self.color = (139, 69, 19)  # Brown
        self.attack_range = 50
        self.attack_cooldown = 1500  # 1.5 seconds
        self.last_attack = 0
        self.max_speed = 2  # Slower
        self.load_animation("walk", "tank_walk_horizontal.png", 8, 60000, (144, 144))  # Boyut ve delay arttı
        
        # Load tank zombie sprite sheet (3x3 grid, 8 frames)
        """try:
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            sprite_path = os.path.join(base_path, "assets", "tank_walk_horizontal.png")
            sprite_sheet = pygame.image.load(sprite_path).convert_alpha()
            
            # Scale sprite sheet to match entity size
            original_frame_size = sprite_sheet.get_height() // 3  # Height of one frame
            scale_factor = self.height / original_frame_size
            new_width = int(sprite_sheet.get_width() * scale_factor)
            new_height = int(sprite_sheet.get_height() * scale_factor)
            scaled_sheet = pygame.transform.scale(sprite_sheet, (new_width, new_height))
            
            # Load walk animation with 3 columns
            self.load_animation("walk", scaled_sheet, self.width, self.height, 8, 150, columns=3)  # Slower animation
        except Exception as e:
            print(f"Failed to load tank zombie sprite sheet! Error: {e}")
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
