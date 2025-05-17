import heapq
import math
import time

class Node:
    def __init__(self, x, y, g_cost=0, h_cost=0):
        self.x = x
        self.y = y
        self.g_cost = g_cost  # Başlangıçtan bu noktaya olan maliyet
        self.h_cost = h_cost  # Bu noktadan hedefe tahmini maliyet
        self.f_cost = g_cost + h_cost  # Toplam maliyet
        self.parent = None
    
    def __lt__(self, other):
        return self.f_cost < other.f_cost

class PathFinder:
    def __init__(self, game_map):
        self.game_map = game_map
        self.last_paths = {}  # Son hesaplanan yolları önbellekte tut
        self.path_timeout = 500  # Yolları 500ms sonra yeniden hesapla
        
    def get_path(self, start_x, start_y, end_x, end_y):
        # Piksel koordinatlarını ızgara koordinatlarına çevir
        start_tile_x = int(start_x / self.game_map.tile_size)
        start_tile_y = int(start_y / self.game_map.tile_size)
        end_tile_x = int(end_x / self.game_map.tile_size)
        end_tile_y = int(end_y / self.game_map.tile_size)
        
        # Başlangıç veya bitiş noktası harita dışındaysa boş yol döndür
        if not (0 <= start_tile_x < self.game_map.width and 
                0 <= start_tile_y < self.game_map.height and
                0 <= end_tile_x < self.game_map.width and
                0 <= end_tile_y < self.game_map.height):
            return []
            
        # Eğer başlangıç ve bitiş noktaları aynıysa boş yol döndür
        if (start_tile_x, start_tile_y) == (end_tile_x, end_tile_y):
            return []
            
        # Önbellekteki yolu kontrol et
        path_key = (start_tile_x, start_tile_y, end_tile_x, end_tile_y)
        current_time = time.time() * 1000  # Milisaniye cinsinden
        
        if path_key in self.last_paths:
            path_time, path = self.last_paths[path_key]
            if current_time - path_time < self.path_timeout:
                return path
        
        # Yol bulunamadıysa veya timeout olduysa yeni yol hesapla
        path = self._calculate_path(start_tile_x, start_tile_y, end_tile_x, end_tile_y)
        
        # Yolu önbelleğe al
        self.last_paths[path_key] = (current_time, path)
        
        # Önbellek boyutunu kontrol et
        if len(self.last_paths) > 1000:  # Maximum 1000 yol tut
            # En eski yolları sil
            current_paths = sorted(self.last_paths.items(), key=lambda x: x[1][0])
            self.last_paths = dict(current_paths[-1000:])
        
        return path
    
    def _calculate_path(self, start_tile_x, start_tile_y, end_tile_x, end_tile_y):
        # A* algoritması için gerekli veri yapıları
        frontier = []
        heapq.heappush(frontier, (0, (start_tile_x, start_tile_y)))
        came_from = {}
        cost_so_far = {}
        came_from[(start_tile_x, start_tile_y)] = None
        cost_so_far[(start_tile_x, start_tile_y)] = 0
        
        found_path = False
        while frontier and not found_path:
            current = heapq.heappop(frontier)[1]
            
            if current == (end_tile_x, end_tile_y):
                found_path = True
                break
            
            # Sadece 4 yöne hareket et (daha hızlı pathfinding)
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                next_x = current[0] + dx
                next_y = current[1] + dy
                
                if not (0 <= next_x < self.game_map.width and 
                       0 <= next_y < self.game_map.height):
                    continue
                
                if self.game_map.is_wall(next_x, next_y):
                    continue
                
                new_cost = cost_so_far[current] + 1
                next_pos = (next_x, next_y)
                
                if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                    cost_so_far[next_pos] = new_cost
                    priority = new_cost + abs(end_tile_x - next_x) + abs(end_tile_y - next_y)
                    heapq.heappush(frontier, (priority, next_pos))
                    came_from[next_pos] = current
        
        if not found_path:
            return []
        
        # Yolu oluştur
        path = []
        current = (end_tile_x, end_tile_y)
        
        while current != (start_tile_x, start_tile_y):
            # Izgara koordinatlarını piksel koordinatlarına çevir
            pixel_x = current[0] * self.game_map.tile_size + self.game_map.tile_size/2
            pixel_y = current[1] * self.game_map.tile_size + self.game_map.tile_size/2
            path.append((pixel_x, pixel_y))
            current = came_from[current]
        
        # Yolu tersine çevir
        path.reverse()
        return path
    
    def _heuristic(self, x1, y1, x2, y2):
        # Diagonal distance heuristic
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        return max(dx, dy) + (math.sqrt(2) - 1) * min(dx, dy)
    
    def _is_valid(self, x, y):
        return (0 <= x < self.game_map.width and 
                0 <= y < self.game_map.height and 
                not self.game_map.is_wall(x, y))
    
    def _find_nearest_empty(self, x, y):
        checked = set()
        queue = [(x, y, 0)]
        
        while queue:
            curr_x, curr_y, dist = queue.pop(0)
            
            if not self.game_map.is_wall(curr_x, curr_y):
                return curr_x, curr_y
            
            for dx, dy in self.directions:
                new_x = curr_x + dx
                new_y = curr_y + dy
                
                if ((new_x, new_y) not in checked and 
                    self._is_valid(new_x, new_y)):
                    checked.add((new_x, new_y))
                    queue.append((new_x, new_y, dist + 1))
        
        return x, y  # En kötü durumda orijinal konumu döndür
    
    def _reconstruct_path(self, end_node):
        path = []
        current = end_node
        
        while current:
            # Kare koordinatlarını piksel koordinatlarına çevir
            pixel_x = (current.x * self.game_map.tile_size) + (self.game_map.tile_size / 2)
            pixel_y = (current.y * self.game_map.tile_size) + (self.game_map.tile_size / 2)
            path.append((pixel_x, pixel_y))
            current = current.parent
        
        return list(reversed(path)) 