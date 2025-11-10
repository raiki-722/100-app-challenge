import random
import time

def attack(attaker, defender):
    """攻撃関数：攻撃者が守備側にランダムなダメージを与える"""
    damage = random.randint(8,20)
    defender["hp"] -= damage
    print(f"{attaker['name']}の攻撃！{defender['name']}に{damage}のダメージ！")
    return damage

def show_status(player, enemy):
    """現在のHPを表示"""
    print(f"{player['name']} HP： {player["hp"]}    {enemy['name']} HP： {enemy['hp']}")
    print("-" * 30)

def battle(player, enemy):
    """戦闘メインループ"""
    print("--- バトル開始！ ---")
    show_status(player, enemy)
    while player["hp"] > 0 and enemy["hp"] > 0:
        # プレイヤーの攻撃
        attack(player, enemy)
        if enemy["hp"] <= 0:
            print(f"{enemy['name']}を倒した！")
            break
        time.sleep(0.5)

        #敵の攻撃
        attack(enemy, player)
        if player["hp"] <= 0:
            print(f"{player['name']}は倒れた…")
            break

        show_status(player, enemy)
        time.sleep(0.5)
    
def main():
    player = {"name": "あなた", "hp": 50}
    enemy = {"name": "スライム", "hp": 50}
    battle(player, enemy)
    
if __name__ == "__main__":
    main()