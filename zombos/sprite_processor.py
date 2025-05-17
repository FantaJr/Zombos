from PIL import Image
import os

def process_spritesheet(input_path, output_path):
    # Sprite sheet'i aç
    sprite_sheet = Image.open(input_path)
    width, height = sprite_sheet.size
    
    # Her bir sprite'ın boyutlarını hesapla (3x3 grid için)
    sprite_width = width // 3
    sprite_height = height // 3
    
    # Sprite'ları saklamak için liste
    sprites = []
    
    # 3x3 grid'den sprite'ları kes
    for row in range(3):
        for col in range(3):
            # Son satırda sadece ilk 2 sprite var, 3. boş
            if row == 2 and col == 2:
                continue
                
            left = col * sprite_width
            top = row * sprite_height
            right = left + sprite_width
            bottom = top + sprite_height
            
            sprite = sprite_sheet.crop((left, top, right, bottom))
            sprites.append(sprite)
    
    # Yeni sprite sheet boyutlarını hesapla (8 sprite yan yana)
    new_width = sprite_width * 8
    new_height = sprite_height
    
    # Yeni boş sprite sheet oluştur
    new_sheet = Image.new('RGBA', (new_width, new_height), (0, 0, 0, 0))
    
    # Sprite'ları yan yana yerleştir
    for i, sprite in enumerate(sprites):
        new_sheet.paste(sprite, (i * sprite_width, 0))
    
    # Yeni sprite sheet'i kaydet
    new_sheet.save(output_path, 'PNG')

def main():
    # İşlenecek sprite sheet'ler
    sprite_sheets = {
        'zombie_walk.png': 'zombie_walk_horizontal.png',
        'tank_walk.png': 'tank_walk_horizontal.png'
    }
    
    assets_dir = 'assets'
    
    for input_file, output_file in sprite_sheets.items():
        input_path = os.path.join(assets_dir, input_file)
        output_path = os.path.join(assets_dir, output_file)
        
        if os.path.exists(input_path):
            print(f"Processing {input_file}...")
            process_spritesheet(input_path, output_path)
            print(f"Created {output_file}")
        else:
            print(f"Error: {input_file} not found")

def create_player_walk_sheet():
    assets_dir = 'assets'
    frames = []
    
    # enemy2.png'den enemy6.png'ye kadar olan dosyaları yükle
    for i in range(2, 7):
        frame_path = os.path.join(assets_dir, f'enemy{i}.png')
        if os.path.exists(frame_path):
            frame = Image.open(frame_path)
            frames.append(frame)
        else:
            print(f"Error: {frame_path} not found")
            return
    
    # İlk frame'in boyutlarını al
    frame_width = frames[0].width
    frame_height = frames[0].height
    
    # Yeni sprite sheet'i oluştur (5 frame yan yana)
    new_width = frame_width * 5
    new_height = frame_height
    new_sheet = Image.new('RGBA', (new_width, new_height), (0, 0, 0, 0))
    
    # Frame'leri yan yana yerleştir
    for i, frame in enumerate(frames):
        new_sheet.paste(frame, (i * frame_width, 0))
    
    # Yeni sprite sheet'i kaydet
    output_path = os.path.join(assets_dir, 'player_walk.png')
    new_sheet.save(output_path, 'PNG')
    print(f"Created {output_path}")

if __name__ == '__main__':
    main()
    create_player_walk_sheet() 