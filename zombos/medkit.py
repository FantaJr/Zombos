import pygame

class Medkit:
    def __init__(self, x, y, heal_amount=30):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
        self.heal_amount = heal_amount
        self.color = (255, 0, 0)  # Kırmızı
        self.rect = pygame.Rect(x, y, self.width, self.height)
    
    def draw(self, screen, camera_x=0, camera_y=0):
        screen_x = self.x - camera_x
        screen_y = self.y - camera_y
        
        # Ekran dışındaysa çizme
        if (screen_x < -self.width or screen_x > screen.get_width() or
            screen_y < -self.height or screen_y > screen.get_height()):
            return
        
        # Medkit kutusunu çiz
        pygame.draw.rect(screen, self.color, 
                        (screen_x, screen_y, self.width, self.height))
        
        # Artı işareti çiz (beyaz)
        line_width = 2
        center_x = screen_x + self.width // 2
        center_y = screen_y + self.height // 2
        
        # Yatay çizgi
        pygame.draw.rect(screen, (255, 255, 255),
                        (screen_x + 4, center_y - line_width//2,
                         self.width - 8, line_width))
        
        # Dikey çizgi
        pygame.draw.rect(screen, (255, 255, 255),
                        (center_x - line_width//2, screen_y + 4,
                         line_width, self.height - 8))
    
    def check_collision(self, entity):
        return self.rect.colliderect(pygame.Rect(
            entity.x, entity.y, entity.width, entity.height
        )) 