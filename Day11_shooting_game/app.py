import pygame
import sys
import random

# 画面サイズ
WIDTH, HEIGHT = 480, 640
FPS = 60

# 色
BLACK  = (0, 0, 0)
WHITE  = (255, 255, 255)
BLUE   = (80, 160, 255)
RED    = (255, 80, 80)
YELLOW = (255, 230, 80)

# 自機設定
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 25
PLAYER_SPEED = 5

# 弾設定
BULLET_WIDTH = 4
BULLET_HEIGHT = 10
BULLET_SPEED = -10

# 敵設定
ENEMY_WIDTH = 30
ENEMY_HEIGHT = 20
ENEMY_MIN_SPEED = 2
ENEMY_MAX_SPEED = 5
ENEMY_SPAWN_INTERVAL = 800  # ミリ秒ごとに敵を追加

ENEMY_EVENT = pygame.USEREVENT + 1

def create_enemy():
    """ランダム位置・ランダム速度の敵1体を作る"""
    x = random.randint(0, WIDTH - ENEMY_WIDTH)
    y = -ENEMY_HEIGHT  # 画面の上の外から出現
    speed = random.randint(ENEMY_MIN_SPEED, ENEMY_MAX_SPEED)
    rect = pygame.Rect(x, y, ENEMY_WIDTH, ENEMY_HEIGHT)
    return {"rect": rect, "speed": speed}

def reset_game():
    """ゲーム状態を初期化"""
    # 自機（画面下中央）
    player = pygame.Rect(
        (WIDTH - PLAYER_WIDTH) // 2,
        HEIGHT - PLAYER_HEIGHT - 20,
        PLAYER_WIDTH,
        PLAYER_HEIGHT,
    )
    bullets = []       # {"rect": Rect}
    enemies = []       # {"rect": Rect, "speed": int}
    score = 0
    lives = 3
    game_over = False
    return player, bullets, enemies, score, lives, game_over

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Day11 縦スクロールシューティング")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 28)

    # 敵出現用タイマー
    pygame.time.set_timer(ENEMY_EVENT, ENEMY_SPAWN_INTERVAL)

    player, bullets, enemies, score, lives, game_over = reset_game()

    running = True
    while running:
        dt = clock.tick(FPS)

        # --- イベント処理 ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                if game_over:
                    if event.key == pygame.K_r:
                        player, bullets, enemies, score, lives, game_over = reset_game()
                else:
                    # 弾を撃つ
                    if event.key == pygame.K_SPACE:
                        bullet_rect = pygame.Rect(
                            player.centerx - BULLET_WIDTH // 2,
                            player.top - BULLET_HEIGHT,
                            BULLET_WIDTH,
                            BULLET_HEIGHT,
                        )
                        bullets.append({"rect": bullet_rect})

            # 敵出現イベント
            if event.type == ENEMY_EVENT and not game_over:
                enemies.append(create_enemy())

        keys = pygame.key.get_pressed()
        if not game_over:
            # 自機の左右移動
            if keys[pygame.K_LEFT]:
                player.x -= PLAYER_SPEED
            if keys[pygame.K_RIGHT]:
                player.x += PLAYER_SPEED

            # 画面外に出ないよう制限
            if player.left < 0:
                player.left = 0
            if player.right > WIDTH:
                player.right = WIDTH

            # --- 弾の移動 ---
            for b in bullets:
                b["rect"].y += BULLET_SPEED
            # 画面外に出た弾を削除
            bullets = [b for b in bullets if b["rect"].bottom > 0]

            # --- 敵の移動 ---
            for e in enemies:
                e["rect"].y += e["speed"]

            # 画面外に落ちた敵 → ライフ減
            kept_enemies = []
            for e in enemies:
                if e["rect"].top > HEIGHT:
                    lives -= 1
                else:
                    kept_enemies.append(e)
            enemies = kept_enemies

            # --- 弾と敵の当たり判定 ---
            new_enemies = []
            for e in enemies:
                hit = False
                for b in bullets:
                    if e["rect"].colliderect(b["rect"]):
                        hit = True
                        score += 10
                        # この弾はあとでまとめて削除
                        b["hit"] = True
                if not hit:
                    new_enemies.append(e)
            enemies = new_enemies
            # 当たった弾を削除
            bullets = [b for b in bullets if not b.get("hit")]

            # --- 敵とプレイヤーの当たり判定 ---
            for e in enemies:
                if e["rect"].colliderect(player):
                    lives -= 1
                    enemies.remove(e)
                    break

            # ライフ0でゲームオーバー
            if lives <= 0:
                game_over = True

        # --- 描画 ---
        screen.fill(BLACK)

        # 自機
        pygame.draw.rect(screen, BLUE, player)

        # 弾
        for b in bullets:
            pygame.draw.rect(screen, YELLOW, b["rect"])

        # 敵
        for e in enemies:
            pygame.draw.rect(screen, RED, e["rect"])

        # スコアとライフ
        score_surf = font.render(f"Score: {score}", True, WHITE)
        lives_surf = font.render(f"Lives: {lives}", True, WHITE)
        screen.blit(score_surf, (10, 10))
        screen.blit(lives_surf, (WIDTH - 120, 10))

        # ゲームオーバーメッセージ
        if game_over:
            msg = "GAME OVER - Rで再スタート / ESCで終了"
            text = font.render(msg, True, WHITE)
            rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(text, rect)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
