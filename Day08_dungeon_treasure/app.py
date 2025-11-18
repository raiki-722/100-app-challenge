import random

WIDTH = 10
HEIGHT = 10

WALL = "#"
EMPTY = "."
PLAYER = "P"
TREASURE = "T"
ENEMY = "E"

def create_empty_map(width, height):
    """高さheight×幅widthの空のマップを作る"""
    return [[EMPTY for _ in range(width)] for _ in range(height)]

def add_walls(game_map, wall_rate=0.18):
    """ランダムに壁を配置する（スタート位置は開けておく）"""
    h = len(game_map)
    w = len(game_map[0])
    for y in range(h):
        for x in range(w):
            if (y, x) == (0, 0):  # スタート位置は必ず空
                continue
            if random.random() < wall_rate:
                game_map[y][x] = WALL

def random_empty_cell(game_map):
    """空マスからランダムに1つ選んで座標(y, x)を返す"""
    h = len(game_map)
    w = len(game_map[0])
    empties = [(y, x) for y in range(h) for x in range(w) if game_map[y][x] == EMPTY]
    return random.choice(empties)

def draw_map(game_map, player_pos, hp, steps):
    """マップとステータスを表示"""
    h = len(game_map)
    w = len(game_map[0])
    print("\n=== ダンジョン ===")
    for y in range(h):
        row_str = ""
        for x in range(w):
            if (y, x) == player_pos:
                row_str += PLAYER
            else:
                row_str += game_map[y][x]
        print(row_str)
    print("===================")
    print(f"HP: {hp}   歩数: {steps}")
    print("操作: w=上 s=下 a=左 d=右 q=終了")

def move(player_pos, command):
    """入力コマンドから、新しい座標を計算"""
    y, x = player_pos
    if command == "w":
        y -= 1
    elif command == "s":
        y += 1
    elif command == "a":
        x -= 1
    elif command == "d":
        x += 1
    return y, x

def in_bounds(pos, width, height):
    """マップ範囲内ならTrue"""
    y, x = pos
    return 0 <= y < height and 0 <= x < width

def main():
    # 初期設定
    game_map = create_empty_map(WIDTH, HEIGHT)
    add_walls(game_map, wall_rate=0.18)

    # プレイヤー初期位置
    player_pos = (0, 0)

    # 宝物の配置
    ty, tx = random_empty_cell(game_map)
    game_map[ty][tx] = TREASURE

    # 敵の配置（3体くらい）
    for _ in range(3):
        ey, ex = random_empty_cell(game_map)
        game_map[ey][ex] = ENEMY

    hp = 3
    steps = 0

    print("=== Day08: ダンジョン宝探しゲーム ===")
    print("宝(T)を見つけたら勝ち！ 敵(E)にぶつかるとHPが減るよ。")
    print("壁(#)は通れない。Pが自分の位置です。")

    while True:
        draw_map(game_map, player_pos, hp, steps)

        cmd = input("コマンド > ").strip().lower()
        if cmd == "q":
            print("ゲームを終了します。")
            break
        if cmd not in ("w", "a", "s", "d"):
            print("w/a/s/d/q のどれかを入力してください。")
            continue

        new_pos = move(player_pos, cmd)

        # マップ外チェック
        if not in_bounds(new_pos, WIDTH, HEIGHT):
            print("これ以上は進めない！(マップ外)")
            continue

        ny, nx = new_pos
        cell = game_map[ny][nx]

        # 壁チェック
        if cell == WALL:
            print("壁があって進めない！")
            continue

        # 歩数カウント
        steps += 1

        # マスの中身で分岐
        if cell == TREASURE:
            player_pos = new_pos
            draw_map(game_map, player_pos, hp, steps)
            print("\n💎 宝を見つけた！おめでとう！")
            print(f"クリアまでの歩数: {steps}")
            break
        elif cell == ENEMY:
            hp -= 1
            print("⚔ 敵にぶつかった！ HPが1減った！")
            if hp <= 0:
                player_pos = new_pos
                draw_map(game_map, player_pos, 0, steps)
                print("\n💀 HPが0になってしまった… ゲームオーバー")
                break
            # 敵マスは1回ぶつかったら空にする
            game_map[ny][nx] = EMPTY
            player_pos = new_pos
        else:
            # ただの空きマス
            player_pos = new_pos

    print("プレイありがとう！")

if __name__ == "__main__":
    main()
