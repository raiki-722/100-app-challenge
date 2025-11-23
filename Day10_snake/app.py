import pygame
import time
import random

# 初期化
pygame.init()

# 色の定義
WHITE = (255, 255, 255)
YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)
GRAY = (169, 169, 169)

# 画面サイズ
DIS_WIDTH = 600
DIS_HEIGHT = 400

dis = pygame.display.set_mode((DIS_WIDTH, DIS_HEIGHT))
pygame.display.set_caption('Snake Game by Antigravity')

clock = pygame.time.Clock()

SNAKE_BLOCK = 10
INITIAL_SPEED = 15

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

def your_score(score, level):
    value = score_font.render("Score: " + str(score) + "  Level: " + str(level), True, YELLOW)
    dis.blit(value, [0, 0])

def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, GREEN, [x[0], x[1], snake_block, snake_block])

def draw_obstacles(obstacles):
    for obs in obstacles:
        pygame.draw.rect(dis, GRAY, [obs[0], obs[1], SNAKE_BLOCK, SNAKE_BLOCK])

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    text_rect = mesg.get_rect(center=(DIS_WIDTH/2, DIS_HEIGHT/2))
    dis.blit(mesg, text_rect)

def generate_obstacles(num_obstacles, snake_list, food_pos):
    obstacles = []
    while len(obstacles) < num_obstacles:
        obs_x = round(random.randrange(0, DIS_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
        obs_y = round(random.randrange(0, DIS_HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0
        
        # スネークの初期位置周辺（安全地帯）とフード位置を避ける
        safe_zone = False
        for x in snake_list:
             if abs(x[0] - obs_x) < 50 and abs(x[1] - obs_y) < 50:
                 safe_zone = True
                 break
        
        if [obs_x, obs_y] not in obstacles and [obs_x, obs_y] != food_pos and not safe_zone:
            obstacles.append([obs_x, obs_y])
    return obstacles

def gameLoop():
    game_over = False
    game_close = False

    x1 = DIS_WIDTH / 2
    y1 = DIS_HEIGHT / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1
    
    # 初期スネーク位置をリストに入れる（障害物生成時の安全地帯判定のため）
    snake_List.append([x1, y1])

    foodx = round(random.randrange(0, DIS_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
    foody = round(random.randrange(0, DIS_HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0

    level = 1
    current_speed = INITIAL_SPEED
    obstacles = generate_obstacles(0, snake_List, [foodx, foody]) # レベル1は障害物なし（または初期設定に従うならここで生成）
    
    # 初期レベルの障害物設定（レベル1から障害物ありにする場合）
    # obstacles = generate_obstacles(5, snake_List, [foodx, foody]) 
    # 今回の要件では「レベルアップで障害物増加」なので、初期は0または少量からスタートし、
    # レベルアップ時に増やす実装にします。
    # 要件「障害物はランダムに10個配置」とあるので、初期から10個配置します。
    obstacles = generate_obstacles(10, snake_List, [foodx, foody])


    while not game_over:

        while game_close == True:
            dis.fill(BLUE)
            message("You Lost! Press C-Play Again or Q-Quit", RED)
            your_score(Length_of_snake - 1, level)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -SNAKE_BLOCK
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = SNAKE_BLOCK
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -SNAKE_BLOCK
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = SNAKE_BLOCK
                    x1_change = 0

        if x1 >= DIS_WIDTH or x1 < 0 or y1 >= DIS_HEIGHT or y1 < 0:
            game_close = True
        
        # 障害物との衝突判定
        for obs in obstacles:
            if x1 == obs[0] and y1 == obs[1]:
                game_close = True

        x1 += x1_change
        y1 += y1_change
        dis.fill(BLACK)
        
        # 障害物の描画
        draw_obstacles(obstacles)

        pygame.draw.rect(dis, RED, [foodx, foody, SNAKE_BLOCK, SNAKE_BLOCK])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(SNAKE_BLOCK, snake_List)
        your_score(Length_of_snake - 1, level)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, DIS_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
            foody = round(random.randrange(0, DIS_HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0
            
            # フードが障害物と重ならないようにする
            while [foodx, foody] in obstacles:
                foodx = round(random.randrange(0, DIS_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
                foody = round(random.randrange(0, DIS_HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0

            Length_of_snake += 1
            
            # レベルアップ判定 (スコア20ごと)
            current_score = Length_of_snake - 1
            if current_score > 0 and current_score % 20 == 0:
                level += 1
                current_speed += 2
                
                dis.fill(BLACK)
                message(f"Level Up! Level {level}", YELLOW)
                pygame.display.update()
                time.sleep(2)
                
                # レベルアップ時のリセット処理
                # スネーク位置リセット
                x1 = DIS_WIDTH / 2
                y1 = DIS_HEIGHT / 2
                x1_change = 0
                y1_change = 0
                snake_List = []
                Length_of_snake = 1
                snake_List.append([x1, y1])
                
                # 障害物再生成（数を増やす）
                num_obstacles = 10 + (level - 1) * 5
                obstacles = generate_obstacles(num_obstacles, snake_List, [foodx, foody])

        clock.tick(current_speed)

    pygame.quit()
    quit()

if __name__ == "__main__":
    gameLoop()
