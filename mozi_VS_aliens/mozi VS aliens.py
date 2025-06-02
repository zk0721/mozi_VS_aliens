import pygame
import sys
import random
import math
import os
from pygame.locals import *

# 初始化pygame和混音器
pygame.init()
pygame.mixer.init()

# 获取当前脚本所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))

# 屏幕设置
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("mozi VS alien")

# 构建资源文件路径
images_dir = os.path.join(script_dir, "images")
music_dir = os.path.join(script_dir, "music")

# 加载图像
try:
    # 使用相对路径加载图像
    player_img = pygame.image.load(os.path.join(images_dir, "mozi.bmp"))
    bullet_img = pygame.image.load(os.path.join(images_dir, "kuwu.bmp"))
    alien_img = pygame.image.load(os.path.join(images_dir, "alien.bmp"))
    background_img = pygame.image.load(os.path.join(images_dir, "background.bmp"))
    
    # 加载标题图片
    title_img = pygame.image.load(os.path.join(images_dir, "background.bmp"))  # 使用背景图作为标题
    
    # 加载胜利和失败图片
    victory_img = pygame.image.load(os.path.join(images_dir, "win_1.bmp"))
    defeat_img = pygame.image.load(os.path.join(images_dir, "lose_1.bmp"))
    
    # 缩放图像以适应游戏
    player_img = pygame.transform.scale(player_img, (60, 60))
    bullet_img = pygame.transform.scale(bullet_img, (20, 40))
    alien_img = pygame.transform.scale(alien_img, (50, 50))
    background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
    title_img = pygame.transform.scale(title_img, (400, 150))
    
    # 缩放胜利和失败图片
    victory_img = pygame.transform.scale(victory_img, (300, 200))
    defeat_img = pygame.transform.scale(defeat_img, (300, 200))
    
    # 加载音乐
    cover_music = os.path.join(music_dir, "music_4.mp3")
    battle_musics = [
        os.path.join(music_dir, "music_3.mp3"),
        os.path.join(music_dir, "music_2.mp3"),
        os.path.join(music_dir, "music_1.mp3")
    ]
    
    # 尝试加载封面音乐
    try:
        pygame.mixer.music.load(cover_music)
        music_available = True
    except:
        print(f"无法加载音乐: {cover_music}")
        music_available = False
    
except Exception as e:
    print(f"错误: {e}")
    # 如果图像加载失败，创建彩色替代图像
    player_img = pygame.Surface((60, 60), pygame.SRCALPHA)
    pygame.draw.polygon(player_img, (0, 255, 255), [(30, 0), (0, 60), (60, 60)])
    pygame.draw.circle(player_img, (255, 200, 0), (30, 20), 10)
    
    bullet_img = pygame.Surface((20, 40), pygame.SRCALPHA)
    pygame.draw.rect(bullet_img, (255, 255, 0), (5, 0, 10, 40))
    
    alien_img = pygame.Surface((50, 50), pygame.SRCALPHA)
    pygame.draw.circle(alien_img, (255, 0, 0), (25, 25), 20)
    pygame.draw.circle(alien_img, (0, 255, 0), (15, 15), 5)
    pygame.draw.circle(alien_img, (0, 255, 0), (35, 15), 5)
    pygame.draw.arc(alien_img, (0, 255, 255), (10, 25, 30, 20), 0, math.pi, 3)
    
    background_img = pygame.Surface((WIDTH, HEIGHT))
    background_img.fill((0, 0, 50))  # 深蓝色背景
    for i in range(100):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        pygame.draw.circle(background_img, (255, 255, 255), (x, y), 1)
    
    title_img = pygame.Surface((400, 150), pygame.SRCALPHA)
    pygame.draw.rect(title_img, (50, 50, 150), (0, 0, 400, 150), border_radius=20)
    font = pygame.font.SysFont(None, 60)
    title_text = font.render("mozi VS alien", True, (255, 215, 0))
    title_img.blit(title_text, (400//2 - title_text.get_width()//2, 150//2 - title_text.get_height()//2))
    
    # 创建替代的胜利和失败图片
    victory_img = pygame.Surface((300, 200), pygame.SRCALPHA)
    pygame.draw.rect(victory_img, (100, 200, 100), (0, 0, 300, 200), border_radius=15)
    font = pygame.font.SysFont(None, 48)
    victory_text = font.render("胜利!", True, (255, 255, 0))
    victory_img.blit(victory_text, (150 - victory_text.get_width()//2, 100 - victory_text.get_height()//2))
    
    defeat_img = pygame.Surface((300, 200), pygame.SRCALPHA)
    pygame.draw.rect(defeat_img, (200, 100, 100), (0, 0, 300, 200), border_radius=15)
    defeat_text = font.render("失败", True, (255, 255, 0))
    defeat_img.blit(defeat_text, (150 - defeat_text.get_width()//2, 100 - defeat_text.get_height()//2))
    
    music_available = False

# 玩家类 - 继承自pygame.sprite.Sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()  # 调用父类初始化
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 20
        self.speed = 8
        self.health = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
    
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed
    
    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
            # 播放射击音效
            if shoot_sound:
                shoot_sound.play()
    
    def draw_health(self):
        pygame.draw.rect(screen, (255, 0, 0), (self.rect.x, self.rect.bottom + 5, self.rect.width, 5))
        pygame.draw.rect(screen, (0, 255, 0), (self.rect.x, self.rect.bottom + 5, self.rect.width * (self.health / 100), 5))

# 子弹类 - 继承自pygame.sprite.Sprite
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -10
    
    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

# 外星人类 - 继承自pygame.sprite.Sprite
class Alien(pygame.sprite.Sprite):
    def __init__(self, speed=None, rotation_speed=None):
        super().__init__()
        self.image = alien_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        if speed:
            self.speedy = speed
        else:
            self.speedy = random.randrange(1, 5)
        self.speedx = random.randrange(-3, 3)
        self.rotation = 0
        self.rotation_speed = rotation_speed if rotation_speed else random.randrange(-5, 5)
        self.original_image = self.image
    
    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        
        # 旋转外星人
        self.rotation = (self.rotation + self.rotation_speed) % 360
        self.image = pygame.transform.rotate(self.original_image, self.rotation)
        self.rect = self.image.get_rect(center=self.rect.center)
        
        # 如果外星人移出屏幕，重新生成
        if self.rect.top > HEIGHT + 20 or self.rect.left < -50 or self.rect.right > WIDTH + 50:
            self.reset_position()
    
    def reset_position(self):
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 5)
        self.speedx = random.randrange(-3, 3)

# 爆炸效果类 - 继承自pygame.sprite.Sprite
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.size = random.choice([30, 40, 50])
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 165, 0), (self.size//2, self.size//2), self.size//2)
        pygame.draw.circle(self.image, (255, 255, 0), (self.size//2, self.size//2), self.size//3)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50
    
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == 8:
                self.kill()
            else:
                size = self.size - self.frame * 3
                if size < 5:
                    size = 5
                self.image = pygame.Surface((size, size), pygame.SRCALPHA)
                pygame.draw.circle(self.image, (255, 165, 0), (size//2, size//2), size//2)
                pygame.draw.circle(self.image, (255, 255, 0), (size//2, size//2), size//3)
                old_center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = old_center

# 按钮类
class Button:
    def __init__(self, x, y, width, height, text, color=(70, 130, 180), hover_color=(100, 160, 210)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.font = pygame.font.SysFont(None, 36)
        self.is_hovered = False
        
    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
        
    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered
        
    def check_click(self, pos, event):
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(pos)
        return False

# 创建声音效果
try:
    # 尝试加载声音文件
    shoot_sound = pygame.mixer.Sound(buffer=bytearray([random.randint(0, 255) for _ in range(44100)]))
    explosion_sound = pygame.mixer.Sound(buffer=bytearray([random.randint(0, 255) for _ in range(44100)]))
    select_sound = pygame.mixer.Sound(buffer=bytearray([random.randint(0, 255) for _ in range(44100)]))
    victory_sound = pygame.mixer.Sound(buffer=bytearray([random.randint(0, 255) for _ in range(44100)]))
    defeat_sound = pygame.mixer.Sound(buffer=bytearray([random.randint(0, 255) for _ in range(44100)]))
except:
    # 如果声音创建失败
    shoot_sound = None
    explosion_sound = None
    select_sound = None
    victory_sound = None
    defeat_sound = None

# 游戏状态
START_MENU = 0
LEVEL_MODE = 1
ENDLESS_MODE = 2
GAME_OVER = 3
LEVEL_COMPLETE = 4
GAME_COMPLETE = 5

# 游戏主循环
def main():
    # 创建精灵组
    global all_sprites, aliens, bullets
    all_sprites = pygame.sprite.Group()
    aliens = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    
    # 游戏状态
    game_state = START_MENU
    current_level = 1
    level_targets = [10, 15, 20, 25, 30]  # 各关卡目标
    aliens_killed = 0
    score = 0
    
    # 音乐控制变量
    current_battle_music = None
    last_music_change = 0
    music_change_delay = 20000  # 20秒更换一次战斗音乐
    
    # 创建玩家
    player = Player()
    
    # 创建按钮
    level_mode_button = Button(WIDTH//2 - 100, HEIGHT//2, 200, 50, "闯关模式")
    endless_mode_button = Button(WIDTH//2 - 100, HEIGHT//2 + 70, 200, 50, "无尽模式")
    restart_button = Button(WIDTH//2 - 100, HEIGHT//2 + 70, 200, 50, "重新开始")
    next_level_button = Button(WIDTH//2 - 100, HEIGHT//2 + 70, 200, 50, "下一关")
    menu_button = Button(WIDTH//2 - 100, HEIGHT//2 + 140, 200, 50, "返回菜单")
    
    # 游戏循环
    clock = pygame.time.Clock()
    running = True
    
    # 背景星星
    stars = []
    for i in range(100):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        size = random.randint(1, 3)
        speed = random.uniform(0.1, 0.5)
        stars.append([x, y, size, speed])
    
    # 生成初始外星人
    def generate_aliens(num=8, level=1):
        for _ in range(num):
            # 随着关卡增加，外星人移动和旋转更快
            speed = 1.0 + level * 0.3
            rotation_speed = random.randrange(3, 5) + level * 0.5
            alien = Alien(speed, rotation_speed)
            all_sprites.add(alien)
            aliens.add(alien)
    
    # 重置游戏状态
    def reset_game(player, level_mode=False, level=1):
        # 重置精灵组
        all_sprites.empty()
        aliens.empty()
        bullets.empty()
        
        # 添加玩家
        player.health = 100
        player.rect.centerx = WIDTH // 2
        player.rect.bottom = HEIGHT - 20
        all_sprites.add(player)
        
        # 生成外星人
        generate_aliens(8, level)
        
        # 重置分数和击杀数
        nonlocal aliens_killed, score
        aliens_killed = 0
        score = 0
    
    # 初始重置游戏
    reset_game(player, level_mode=False, level=current_level)
    
    # 开始播放封面音乐
    if music_available:
        pygame.mixer.music.play(-1)  # -1表示循环播放
    
    # 添加音效播放标志
    victory_sound_played = False
    defeat_sound_played = False
    
    while running:
        # 控制游戏速度
        clock.tick(60)
        
        # 处理事件
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    if game_state in [LEVEL_MODE, ENDLESS_MODE]:
                        game_state = START_MENU
                        # 切换回封面音乐
                        if music_available:
                            pygame.mixer.music.load(cover_music)
                            pygame.mixer.music.play(-1)
                    else:
                        running = False
                if event.key == K_SPACE and game_state in [LEVEL_MODE, ENDLESS_MODE]:
                    player.shoot()
                # 添加音乐控制快捷键
                if event.key == K_m:
                    # M键切换音乐开关
                    if music_available:
                        if pygame.mixer.music.get_busy():
                            pygame.mixer.music.pause()
                        else:
                            pygame.mixer.music.unpause()
                if event.key == K_PLUS or event.key == K_EQUALS:
                    # 增加音量
                    current_volume = pygame.mixer.music.get_volume()
                    new_volume = min(1.0, current_volume + 0.1)
                    pygame.mixer.music.set_volume(new_volume)
                if event.key == K_MINUS:
                    # 减小音量
                    current_volume = pygame.mixer.music.get_volume()
                    new_volume = max(0.0, current_volume - 0.1)
                    pygame.mixer.music.set_volume(new_volume)
            elif event.type == MOUSEBUTTONDOWN:
                if game_state == START_MENU:
                    if level_mode_button.check_click(mouse_pos, event):
                        game_state = LEVEL_MODE
                        current_level = 1
                        reset_game(player, level_mode=True, level=current_level)
                        # 切换到战斗音乐
                        if music_available and battle_musics:
                            pygame.mixer.music.load(random.choice(battle_musics))
                            pygame.mixer.music.play(-1)
                            current_battle_music = pygame.mixer.music.get_pos()
                            last_music_change = pygame.time.get_ticks()
                        if select_sound:
                            select_sound.play()
                    elif endless_mode_button.check_click(mouse_pos, event):
                        game_state = ENDLESS_MODE
                        current_level = 1
                        reset_game(player)
                        # 切换到战斗音乐
                        if music_available and battle_musics:
                            pygame.mixer.music.load(random.choice(battle_musics))
                            pygame.mixer.music.play(-1)
                            current_battle_music = pygame.mixer.music.get_pos()
                            last_music_change = pygame.time.get_ticks()
                        if select_sound:
                            select_sound.play()
                elif game_state in [GAME_OVER, GAME_COMPLETE]:
                    if restart_button.check_click(mouse_pos, event):
                        current_level = 1
                        reset_game(player, level_mode=True, level=current_level)
                        game_state = LEVEL_MODE
                        # 重置音效播放标志
                        victory_sound_played = False
                        defeat_sound_played = False
                        # 切换到战斗音乐
                        if music_available and battle_musics:
                            pygame.mixer.music.load(random.choice(battle_musics))
                            pygame.mixer.music.play(-1)
                            current_battle_music = pygame.mixer.music.get_pos()
                            last_music_change = pygame.time.get_ticks()
                        if select_sound:
                            select_sound.play()
                    elif menu_button.check_click(mouse_pos, event):
                        game_state = START_MENU
                        # 重置音效播放标志
                        victory_sound_played = False
                        defeat_sound_played = False
                        # 切换到封面音乐
                        if music_available:
                            pygame.mixer.music.load(cover_music)
                            pygame.mixer.music.play(-1)
                        if select_sound:
                            select_sound.play()
                elif game_state == LEVEL_COMPLETE:
                    if next_level_button.check_click(mouse_pos, event):
                        current_level += 1
                        if current_level > 5:
                            game_state = GAME_COMPLETE
                        else:
                            reset_game(player, level_mode=True, level=current_level)
                            game_state = LEVEL_MODE
                            # 重置音效播放标志
                            victory_sound_played = False
                            # 继续播放战斗音乐
                            if music_available and battle_musics:
                                pygame.mixer.music.load(random.choice(battle_musics))
                                pygame.mixer.music.play(-1)
                                current_battle_music = pygame.mixer.music.get_pos()
                                last_music_change = pygame.time.get_ticks()
                        if select_sound:
                            select_sound.play()
                    elif menu_button.check_click(mouse_pos, event):
                        game_state = START_MENU
                        # 重置音效播放标志
                        victory_sound_played = False
                        # 切换到封面音乐
                        if music_available:
                            pygame.mixer.music.load(cover_music)
                            pygame.mixer.music.play(-1)
                        if select_sound:
                            select_sound.play()
        
        # 更新按钮状态
        if game_state == START_MENU:
            level_mode_button.check_hover(mouse_pos)
            endless_mode_button.check_hover(mouse_pos)
        elif game_state in [GAME_OVER, GAME_COMPLETE]:
            restart_button.check_hover(mouse_pos)
            menu_button.check_hover(mouse_pos)
        elif game_state == LEVEL_COMPLETE:
            next_level_button.check_hover(mouse_pos)
            menu_button.check_hover(mouse_pos)
        
        # 更新游戏状态
        if game_state == START_MENU:
            # 更新星星背景
            for i in range(len(stars)):
                stars[i][1] += stars[i][3]
                if stars[i][1] > HEIGHT:
                    stars[i][1] = 0
                    stars[i][0] = random.randint(0, WIDTH)
        
        elif game_state in [LEVEL_MODE, ENDLESS_MODE]:
            # 定期更换战斗音乐
            now = pygame.time.get_ticks()
            if music_available and battle_musics and now - last_music_change > music_change_delay:
                pygame.mixer.music.load(random.choice(battle_musics))
                pygame.mixer.music.play(-1)
                last_music_change = now
            
            # 更新游戏
            all_sprites.update()
            
            # 检测子弹和外星人碰撞
            hits = pygame.sprite.groupcollide(aliens, bullets, True, True)
            for hit in hits:
                score += 10
                aliens_killed += 1
                explosion = Explosion(hit.rect.center)
                all_sprites.add(explosion)
                if explosion_sound:
                    explosion_sound.play()
                
                # 在闯关模式下，检查是否完成关卡目标
                if game_state == LEVEL_MODE:
                    if aliens_killed >= level_targets[current_level-1]:
                        game_state = LEVEL_COMPLETE
                        # 播放胜利音效
                        if victory_sound and not victory_sound_played:
                            victory_sound.play()
                            victory_sound_played = True
                        # 切换到封面音乐
                        if music_available:
                            pygame.mixer.music.load(cover_music)
                            pygame.mixer.music.play(-1)
                
                # 生成新的外星人
                if game_state == ENDLESS_MODE or (game_state == LEVEL_MODE and aliens_killed < level_targets[current_level-1]):
                    # 随着时间推移，外星人速度增加
                    speed_factor = current_level * 0.3 if game_state == LEVEL_MODE else 0.01 * score
                    alien = Alien(1.0 + speed_factor)
                    all_sprites.add(alien)
                    aliens.add(alien)
            
            # 检测外星人和玩家碰撞
            hits = pygame.sprite.spritecollide(player, aliens, True)
            for hit in hits:
                player.health -= 20
                explosion = Explosion(hit.rect.center)
                all_sprites.add(explosion)
                if explosion_sound:
                    explosion_sound.play()
                
                # 生成新的外星人
                speed_factor = current_level * 0.3 if game_state == LEVEL_MODE else 0.01 * score
                alien = Alien(1.0 + speed_factor)
                all_sprites.add(alien)
                aliens.add(alien)
                
                if player.health <= 0:
                    game_state = GAME_OVER
                    # 播放失败音效
                    if defeat_sound and not defeat_sound_played:
                        defeat_sound.play()
                        defeat_sound_played = True
                    # 停止音乐
                    if music_available:
                        pygame.mixer.music.stop()
        
        # 绘制
        # 绘制背景
        screen.fill((0, 0, 30))  # 深蓝色背景
        
        # 绘制星星
        for star in stars:
            pygame.draw.circle(screen, (255, 255, 255), (int(star[0]), int(star[1])), star[2])
        
        if game_state == START_MENU:
            # 绘制标题
            screen.blit(title_img, (WIDTH//2 - title_img.get_width()//2, 80))
            
            # 绘制游戏模式选择
            title_font = pygame.font.SysFont(None, 48)
            mode_title = title_font.render("选择游戏模式", True, (255, 215, 0))
            screen.blit(mode_title, (WIDTH//2 - mode_title.get_width()//2, 250))
            
            # 绘制按钮
            level_mode_button.draw(screen)
            endless_mode_button.draw(screen)
            
            # 绘制控制提示
            controls_font = pygame.font.SysFont(None, 24)
            controls = controls_font.render("方向键移动，空格射击，ESC返回", True, (200, 200, 255))
            screen.blit(controls, (WIDTH//2 - controls.get_width()//2, HEIGHT - 30))
            
            # 绘制音乐控制提示
            music_controls = controls_font.render("M: 音乐开关 +/-: 音量调节", True, (150, 200, 255))
            screen.blit(music_controls, (WIDTH//2 - music_controls.get_width()//2, HEIGHT - 60))
            
            # 绘制版本信息
            version = controls_font.render("版本 1.0 - mozi VS alien", True, (150, 150, 200))
            screen.blit(version, (10, HEIGHT - 30))
        
        elif game_state in [LEVEL_MODE, ENDLESS_MODE]:
            # 绘制游戏背景
            screen.blit(background_img, (0, 0))
            
            # 如果背景图加载失败，绘制星星背景
            if background_img.get_size() == (1, 1):  # 如果背景图是默认的，说明加载失败
                screen.fill((0, 0, 50))
                for i in range(100):
                    x = random.randint(0, WIDTH)
                    y = random.randint(0, HEIGHT)
                    pygame.draw.circle(screen, (255, 255, 255), (x, y), 1)
            
            all_sprites.draw(screen)
            player.draw_health()
            
            # 显示分数
            font = pygame.font.SysFont(None, 36)
            score_text = font.render(f"分数: {score}", True, (255, 255, 0))
            screen.blit(score_text, (10, 10))
            
            # 显示生命值
            health_text = font.render(f"生命值: {player.health}", True, (0, 255, 0))
            screen.blit(health_text, (10, 50))
            
            # 在闯关模式下显示关卡信息
            if game_state == LEVEL_MODE:
                level_text = font.render(f"关卡: {current_level}/5", True, (255, 200, 0))
                screen.blit(level_text, (WIDTH - level_text.get_width() - 10, 10))
                
                target_text = font.render(f"目标: {aliens_killed}/{level_targets[current_level-1]}", True, (200, 200, 255))
                screen.blit(target_text, (WIDTH - target_text.get_width() - 10, 50))
            
            # 绘制标题
            title_font = pygame.font.SysFont(None, 36)
            title = title_font.render("mozi VS alien", True, (255, 200, 0))
            screen.blit(title, (WIDTH//2 - title.get_width()//2, 10))
            
            # 绘制音乐控制提示
            controls_font = pygame.font.SysFont(None, 24)
            music_controls = controls_font.render("M: 音乐开关 +/-: 音量调节", True, (150, 200, 255))
            screen.blit(music_controls, (WIDTH - music_controls.get_width() - 10, HEIGHT - 30))
        
        elif game_state == GAME_OVER:
            # 绘制半透明覆盖层
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))
            
            # 绘制失败图片
            screen.blit(defeat_img, (WIDTH//2 - defeat_img.get_width()//2, HEIGHT//3 - 30))
            
            # 绘制游戏结束文本
            font = pygame.font.SysFont(None, 72)
            game_over_text = font.render("游戏结束", True, (255, 50, 50))
            screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//3 + 180))
            
            # 绘制分数
            score_font = pygame.font.SysFont(None, 48)
            score_text = score_font.render(f"最终分数: {score}", True, (255, 255, 0))
            screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2 + 50))
            
            # 绘制按钮
            restart_button.draw(screen)
            menu_button.draw(screen)
            
            # 绘制音乐控制提示
            controls_font = pygame.font.SysFont(None, 24)
            music_controls = controls_font.render("M: 音乐开关 +/-: 音量调节", True, (150, 200, 255))
            screen.blit(music_controls, (WIDTH//2 - music_controls.get_width()//2, HEIGHT - 60))
        
        elif game_state == LEVEL_COMPLETE:
            # 绘制半透明覆盖层
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 50, 0, 180))
            screen.blit(overlay, (0, 0))
            
            # 绘制胜利图片
            screen.blit(victory_img, (WIDTH//2 - victory_img.get_width()//2, HEIGHT//4 - 20))
            
            # 绘制关卡完成文本
            font = pygame.font.SysFont(None, 72)
            level_text = font.render(f"第 {current_level} 关 完成!", True, (50, 255, 50))
            screen.blit(level_text, (WIDTH//2 - level_text.get_width()//2, HEIGHT//3 + 180))
            
            # 绘制分数
            score_font = pygame.font.SysFont(None, 48)
            score_text = score_font.render(f"当前分数: {score}", True, (255, 255, 0))
            screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2 + 50))
            
            # 绘制按钮
            next_level_button.draw(screen)
            menu_button.draw(screen)
            
            # 绘制音乐控制提示
            controls_font = pygame.font.SysFont(None, 24)
            music_controls = controls_font.render("M: 音乐开关 +/-: 音量调节", True, (150, 200, 255))
            screen.blit(music_controls, (WIDTH//2 - music_controls.get_width()//2, HEIGHT - 60))
        
        elif game_state == GAME_COMPLETE:
            # 绘制半透明覆盖层
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((50, 0, 50, 180))
            screen.blit(overlay, (0, 0))
            
            # 绘制胜利图片（在游戏完成时也显示胜利图片）
            screen.blit(victory_img, (WIDTH//2 - victory_img.get_width()//2, HEIGHT//4 - 20))
            
            # 绘制游戏完成文本
            font = pygame.font.SysFont(None, 72)
            complete_text = font.render("恭喜通关!", True, (255, 215, 0))
            screen.blit(complete_text, (WIDTH//2 - complete_text.get_width()//2, HEIGHT//3 + 180))
            
            # 绘制分数
            score_font = pygame.font.SysFont(None, 48)
            score_text = score_font.render(f"最终分数: {score}", True, (255, 255, 0))
            screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2 + 50))
            
            # 绘制按钮
            restart_button.draw(screen)
            menu_button.draw(screen)
            
            # 绘制音乐控制提示
            controls_font = pygame.font.SysFont(None, 24)
            music_controls = controls_font.render("M: 音乐开关 +/-: 音量调节", True, (150, 200, 255))
            screen.blit(music_controls, (WIDTH//2 - music_controls.get_width()//2, HEIGHT - 60))
        
        # 更新屏幕
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()