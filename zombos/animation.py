import pygame
import os

class Animation:
    def __init__(self, sprite_sheet_path, frame_count, frame_delay_ms, sprite_size, is_spritesheet=True):
        self.sprite_sheet_path = sprite_sheet_path
        self.frame_count = frame_count
        self.frame_delay = frame_delay_ms
        self.accumulated_time = 0
        self.current_frame = 0
        self.frames = []
        
        if is_spritesheet:
            # Sprite sheet'i yükle
            sprite_sheet = pygame.image.load(os.path.join('assets', sprite_sheet_path))
            total_width = sprite_sheet.get_width()
            frame_width = total_width // frame_count  # Her frame'in genişliği
            frame_height = sprite_sheet.get_height()
            
            # Her frame'i kes
            for i in range(frame_count):
                frame_surface = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
                frame_surface.blit(sprite_sheet, (0, 0), 
                                 (i * frame_width, 0, frame_width, frame_height))
                
                # Frame'i istenilen boyuta ölçekle
                if (frame_width, frame_height) != sprite_size:
                    frame_surface = pygame.transform.scale(frame_surface, sprite_size)
                
                self.frames.append(frame_surface)
        """ else:
            # Ayrı frame'leri yükle
            for i in range(1, frame_count + 1):
                frame_path = os.path.join('assets', f'enemy{i}.png')
                frame = pygame.image.load(frame_path).convert_alpha()
                if sprite_size != frame.get_size():
                    frame = pygame.transform.scale(frame, sprite_size)
                self.frames.append(frame)"""
    
    def update(self, delta_time):
        self.accumulated_time += delta_time
        
        if self.accumulated_time >= self.frame_delay:
            self.current_frame = (self.current_frame + 1) % self.frame_count
            self.accumulated_time = 0
    
    def get_current_frame(self, scale=1.0):
        frame = self.frames[self.current_frame]
        if scale != 1.0:
            current_size = frame.get_size()
            scaled_size = (int(current_size[0] * scale), int(current_size[1] * scale))
            frame = pygame.transform.scale(frame, scaled_size)
            
         # Flip işlemi her durumda uygulanmalı
        """ if flip_x or flip_y:
            frame = pygame.transform.flip(frame, flip_x, flip_y)"""
            
        return frame

    def play(self):
        self.is_playing = True
    
    def pause(self):
        self.is_playing = False
    
    def reset(self):
        self.current_frame = 0
        self.accumulated_time = 0 