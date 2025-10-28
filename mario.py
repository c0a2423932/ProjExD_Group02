import os
import sys
import pygame as pg

WIDTH, HEIGHT = 900, 600
FPS = 60
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Colors
BG = (135, 206, 235)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (50, 205, 50)
BROWN = (139, 69, 19)
GOLD = (255, 215, 0)
RED = (220, 20, 60)


class Player:
    def __init__(self, x, y):
        self.rect = pg.Rect(x, y, 40, 50)
        self.vx = 0.0
        self.vy = 0.0
        self.speed = 5
        self.jump_power = 14
        self.on_ground = False

    def handle_input(self, keys):
        self.vx = 0
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -self.speed
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = self.speed
        if (keys[pg.K_SPACE] or keys[pg.K_z] or keys[pg.K_UP]) and self.on_ground:
            self.vy = -self.jump_power
            self.on_ground = False

    def apply_gravity(self):
        self.vy += 0.8  # gravity
        if self.vy > 20:
            self.vy = 20

    def update(self, platforms):
        self.rect.x += int(self.vx)
        self.collide(self.vx, 0, platforms)
        self.apply_gravity()
        self.rect.y += int(self.vy)
        self.on_ground = False
        self.collide(0, self.vy, platforms)

    def collide(self, vx, vy, platforms):
        for p in platforms:
            if self.rect.colliderect(p):
                if vx > 0:
                    self.rect.right = p.left
                if vx < 0:
                    self.rect.left = p.right
                if vy > 0:
                    self.rect.bottom = p.top
                    self.vy = 0
                    self.on_ground = True
                if vy < 0:
                    self.rect.top = p.bottom
                    self.vy = 0

    def draw(self, surf):
        pg.draw.rect(surf, RED, self.rect)


class Enemy:
    def __init__(self, x, y, w=40, h=40, left_bound=None, right_bound=None):
        self.rect = pg.Rect(x, y, w, h)
        self.vx = 2
        self.left_bound = left_bound
        self.right_bound = right_bound

    def update(self):
        self.rect.x += self.vx
        if self.left_bound is not None and self.rect.left < self.left_bound:
            self.rect.left = self.left_bound
            self.vx *= -1
        if self.right_bound is not None and self.rect.right > self.right_bound:
            self.rect.right = self.right_bound
            self.vx *= -1

    def draw(self, surf):
        pg.draw.rect(surf, (80, 0, 80), self.rect)
#落ちてくる敵
class FallingEnemy:
    def __init__(self, x, y, w=40, h=40, speed=2):
        self.rect = pg.Rect(x, y, w, h)
        self.vy = speed  # 落下速度

    def update(self):
        self.rect.y += self.vy  # 下に落ちる

        # 画面外に出たら上にリセット
        if self.rect.top > HEIGHT:
            self.rect.bottom = 0

    def draw(self, surf):
        pg.draw.rect(surf, (0, 0, 255), self.rect)  # 青色の敵


def build_level():
    platforms = []
    platforms.append(pg.Rect(0, HEIGHT - 40, WIDTH, 40))
    platforms.append(pg.Rect(100, 460, 200, 20))
    platforms.append(pg.Rect(380, 360, 180, 20))
    platforms.append(pg.Rect(600, 280, 220, 20))
    platforms.append(pg.Rect(250, 520, 120, 20))
    platforms.append(pg.Rect(480, 520, 80, 20))
    return platforms



def draw_text(surf, text, size, x, y, color=BLACK, center=True):
    font = pg.font.Font(None, size)
    txt = font.render(text, True, color)
    rect = txt.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    surf.blit(txt, rect)

def main():
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("北極探検ゲーム")
    clock = pg.time.Clock()

    state = "start"

    # 初期化用関数
    def init_game():
        player = Player(50, HEIGHT - 90 - 50)  # プレイヤーの初期位置
        platforms = build_level()
        coins = [
            pg.Rect(150, 420, 12, 12),
            pg.Rect(420, 320, 12, 12),
            pg.Rect(650, 240, 12, 12),
            pg.Rect(270, 480, 12, 12),
        ]
        enemies = [Enemy(420, HEIGHT - 80, left_bound=400, right_bound=760)]
        falling_enemies = [FallingEnemy(200, 0, speed=2), FallingEnemy(500, -150, speed=2)]
        score = 0
        return player, platforms, coins, enemies, falling_enemies, score

    player, platforms, coins, enemies, falling_enemies, score = init_game()
    font = pg.font.Font(None, 36)

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        keys = pg.key.get_pressed()

        # スタート画面
        if state == "start":
            screen.fill(BG)
            draw_text(screen, "GAME START", 80, WIDTH // 2, HEIGHT // 3, WHITE)
            draw_text(screen, "Press SPACE to Start", 40, WIDTH // 2, HEIGHT // 2)
            draw_text(screen, "< >: Move    SPACE : Jump", 30, WIDTH // 2, HEIGHT // 2 + 60, BLACK)
            pg.display.flip()
            if keys[pg.K_SPACE]:
                state = "play"
            continue

        # ゲームプレイ中
        if state == "play":
            player.handle_input(keys)
            player.update(platforms)

            # 敵の更新
            for e in enemies:
                e.update()
            for fe in falling_enemies:
                fe.update()

            # コイン取得
            for c in coins[:]:
                if player.rect.colliderect(c):
                    coins.remove(c)
                    score += 1

            # 敵との衝突判定
            dead = False
            for e in enemies:
                if player.rect.colliderect(e.rect):
                    if player.vy > 0 and player.rect.bottom - e.rect.top < 20:
                        enemies.remove(e)
                        player.vy = -8
                    else:
                        dead = True
            for fe in falling_enemies:
                if player.rect.colliderect(fe.rect):
                    dead = True

            # 画面外判定
            if player.rect.top > HEIGHT:
                dead = True

            if dead:
                state = "gameover"

            # 描画
            screen.fill(BG)
            for p in platforms:
                pg.draw.rect(screen, BROWN, p)
            for c in coins:
                pg.draw.rect(screen, GOLD, c)
            for e in enemies:
                e.draw(screen)
            for fe in falling_enemies:
                fe.draw(screen)
            player.draw(screen)
            txt = font.render(f'Score: {score}', True, BLACK)
            screen.blit(txt, (10, 10))
            pg.display.flip()

        # ゲームオーバー画面
        elif state == "gameover":
            screen.fill(BG)
            draw_text(screen, "GAME OVER", 80, WIDTH // 2, HEIGHT // 3, WHITE)
            draw_text(screen, f"Your Score: {score}", 40, WIDTH // 2, HEIGHT // 2)
            draw_text(screen, "Press R to Retry or ESC to Quit", 30, WIDTH // 2, HEIGHT // 2 + 60, BLACK)
            pg.display.flip()

            if keys[pg.K_r]:
                # リトライ時にゲーム状態を初期化
                player, platforms, coins, enemies, falling_enemies, score = init_game()
                state = "start"
            elif keys[pg.K_ESCAPE]:
                running = False

    pg.quit()


if __name__ == '__main__':
    main()




