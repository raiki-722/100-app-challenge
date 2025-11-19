import pygame
import sys

# --- 基本設定 ---
WIDTH, HEIGHT = 800, 600
FPS = 60

# 色の定義（RGB）
BLACK  = (0, 0, 0)
WHITE  = (255, 255, 255)
BLUE   = (50, 150, 255)
RED    = (255, 80, 80)
GREEN  = (80, 255, 120)
ORANGE = (255, 180, 80)

# --- パドル設定 ---
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 15
PADDLE_SPEED = 7

# --- ボール設定 ---
BALL_RADIUS = 8
BALL_SPEED_X = 4
BALL_SPEED_Y = -4

# --- ブロック設定 ---
BRICK_ROWS = 5
BRICK_COLS = 10
BRICK_WIDTH = 70
BRICK_HEIGHT = 20
BRICK_MARGIN_X = 10
BRICK_MARGIN_Y = 5
TOP_OFFSET = 60


def create_bricks():
    """ブロック(矩形)のリストを作る"""
    bricks = []
    colors = [RED, ORANGE, GREEN, BLUE, WHITE]  # 行ごとに色を変える
    for row in range(BRICK_ROWS):
        for col in range(BRICK_COLS):
            x = BRICK_MARGIN_X + col * (BRICK_WIDTH + BRICK_MARGIN_X)
            y = TOP_OFFSET + row * (BRICK_HEIGHT + BRICK_MARGIN_Y)
            rect = pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT)
            bricks.append((rect, colors[row % len(colors)]))
    return bricks
 

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Day09 ブロック崩し")
    clock = pygame.time.Clock()
    font_path = "NotoSansJP-VariableFont_wght.ttf"
    font = pygame.font.SysFont(font_path, 28)

    # パドル初期位置
    paddle = pygame.Rect(
        (WIDTH - PADDLE_WIDTH) // 2,
        HEIGHT - 40,
        PADDLE_WIDTH,
        PADDLE_HEIGHT,
    )

    # ボール初期位置
    ball_x = WIDTH // 2
    ball_y = HEIGHT // 2
    ball_vx = BALL_SPEED_X
    ball_vy = BALL_SPEED_Y

    # ブロック生成
    bricks = create_bricks()

    score = 0
    lives = 3
    running = True

    while running:
        clock.tick(FPS)

        # --- イベント処理 ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # --- キー入力 ---
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle.x -= PADDLE_SPEED
        if keys[pygame.K_RIGHT]:
            paddle.x += PADDLE_SPEED

        # パドルが画面外に出ないようにする
        if paddle.left < 0:
            paddle.left = 0
        if paddle.right > WIDTH:
            paddle.right = WIDTH

        # --- ボールの移動 ---
        ball_x += ball_vx
        ball_y += ball_vy

        # 画面の端との当たり判定（左右）
        if ball_x - BALL_RADIUS <= 0 or ball_x + BALL_RADIUS >= WIDTH:
            ball_vx *= -1
        # 上端
        if ball_y - BALL_RADIUS <= 0:
            ball_vy *= -1

        # 下に落ちたらライフ減少＆リセット
        if ball_y - BALL_RADIUS > HEIGHT:
            lives -= 1
            if lives <= 0:
                # ゲームオーバー
                text = font.render("GAME OVER - Qで終了 / Rで再スタート", True, WHITE)
                screen.blit(text, (80, HEIGHT // 2))
                pygame.display.flip()
                # 入力待ちループ
                wait = True
                while wait:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_q:
                                pygame.quit()
                                sys.exit()
                            if event.key == pygame.K_r:
                                # 状態初期化
                                lives = 3
                                score = 0
                                bricks = create_bricks()
                                ball_x, ball_y = WIDTH // 2, HEIGHT // 2
                                ball_vx, ball_vy = BALL_SPEED_X, BALL_SPEED_Y
                                wait = False
            else:
                # ライフは残っているのでボールだけリセット
                ball_x, ball_y = WIDTH // 2, HEIGHT // 2
                ball_vx, ball_vy = BALL_SPEED_X, BALL_SPEED_Y

        # --- パドルとの当たり判定 ---
        ball_rect = pygame.Rect(
            ball_x - BALL_RADIUS,
            ball_y - BALL_RADIUS,
            BALL_RADIUS * 2,
            BALL_RADIUS * 2,
        )
        if ball_rect.colliderect(paddle) and ball_vy > 0:
            ball_vy *= -1
            # 当たった位置でボールの横方向速度を少し変える（操作感UP）
            hit_pos = (ball_x - paddle.x) / PADDLE_WIDTH  # 0.0〜1.0
            ball_vx = (hit_pos - 0.5) * 10  # 中央で0, 端で左右に大きく曲がる

        # --- ブロックとの当たり判定 ---
        new_bricks = []
        for rect, color in bricks:
            if ball_rect.colliderect(rect):
                ball_vy *= -1
                score += 10
                # ブロックは消えるので new_bricks に追加しない
                
                # ★ スピードアップ（上限付き）
                speed_scale = 1.03   # 3%だけ速くする（値は調整OK）
                ball_vx *= speed_scale
                ball_vy *= speed_scale

                # ★ 速すぎる暴走防止
                max_speed = 12
                ball_vx = max(-max_speed, min(max_speed, ball_vx))
                ball_vy = max(-max_speed, min(max_speed, ball_vy))
            else:
                new_bricks.append((rect, color))
        bricks = new_bricks
        
        # すべてのブロックを壊したらクリア
        if not bricks:
            text = font.render("CLEAR!! おめでとう！ Rで再スタート", True, WHITE)
            screen.blit(text, (150, HEIGHT // 2))
            pygame.display.flip()
            wait = True
            while wait:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                        # 再スタート
                        lives = 3
                        score = 0
                        bricks = create_bricks()
                        ball_x, ball_y = WIDTH // 2, HEIGHT // 2
                        ball_vx, ball_vy = BALL_SPEED_X, BALL_SPEED_Y
                        wait = False

        # --- 描画 ---
        screen.fill(BLACK)

        # ブロック描画
        for rect, color in bricks:
            pygame.draw.rect(screen, color, rect)

        # パドル描画
        pygame.draw.rect(screen, BLUE, paddle)

        # ボール描画
        pygame.draw.circle(screen, WHITE, (int(ball_x), int(ball_y)), BALL_RADIUS)

        # スコア＆ライフ表示
        score_text = font.render(f"Score: {score}", True, WHITE)
        lives_text = font.render(f"Lives: {lives}", True, WHITE)
        speed_text = font.render(f"speed: {abs(ball_vy):.1f}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (WIDTH - 120, 10))
        screen.blit(speed_text, (WIDTH // 2, 10))
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
