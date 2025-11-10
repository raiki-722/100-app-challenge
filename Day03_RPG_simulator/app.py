import random
import time

def do_attack(attacker, defender):
    """攻撃関数：攻撃者が守備側にランダムなダメージを与える"""
    if random.random() < 0.05:  #　5%でミス
        print("ミス！")
        return 0
    base = random.randint(*attacker["atk"])
    if random.random() < 0.10:  # 10%でクリティカル
        base = int(base * 1.5)
        print("クリティカル！")
    
    #防御半減
    dmg = base // 2 if defender.get("guard") else base
    defender["hp"] = max(0, defender["hp"] - dmg)
    #１回食らったら防御解除
    if defender.get("guard"):
        defender["guard"] = False

    print(f"{attacker['name']}の攻撃！{defender['name']}に{dmg}のダメージ！")
    return dmg

def do_heal(target):
    low, high = target.get("heal", (8,14))
    amt = random.randint(low, high)
    before = target["hp"]
    target["hp"] = min(target["hp_max"], target["hp"] + amt)
    real = target["hp"] - before
    print(f"{target["name"]}は{real}回復した")
    return real

def use_item(target,item):
    if item["num"] <= 0:
        print("ポーションがもうない！")
        return 0
    before = target["hp"]
    target["hp"] = min(target["hp_max"], target["hp"] + item["heal"])
    item["num"] -= 1
    real = target["hp"] - before
    print(f"{target["name"]}は{real}回復した")

def start_guard(target):
    target["guard"] = True
    print(f"{target["name"]}は身を守っている（次のダメ半減）")

def enemy_ai(enemy, player):
     # HPが少ないときは回復 30% / それ以外は攻撃 90% / たまに防御 10%
     import random
     if enemy["hp"] <= enemy["hp_max"] * 0.35 and random.random() < 0.3:
         return "h"
     r = random.random()
     if r < 0.9:
         return "a"
     else:
         return "g"

def show_status(player, enemy, item):
    """現在のHPを表示"""
    print(f"{player['name']} HP： {player["hp"]}    {enemy['name']} HP： {enemy['hp']}")
    print(f"{item["name"]} 　残り{item["num"]}個")
    print("-" * 30)

def choose_command():
    while True:
        cmd = input("[A]攻撃 / [H]回復 / [G]防御 / [P]ポーションを使う> ").strip().lower()
        if cmd in ("a", "h", "g", "p"):
            return cmd
        print("a/h/g/p のいずれかで入力してください。")

def battle(player, enemy, item):
    """戦闘メインループ"""
    print("--- バトル開始！ ---")
    while player["hp"] > 0 and enemy["hp"] > 0:
        # プレイヤーのターン
        show_status(player, enemy, item)
        cmd = choose_command()
        if cmd == "a":
            dmg = do_attack(player, enemy)
        elif cmd == "h":
            amt = do_heal(player)
        elif cmd == "g":
            start_guard(player)
        elif cmd == "p":
            use_item(player,item)

        if enemy["hp"] <= 0:
            print(f"{enemy["name"]}を倒した！")
            break

        #　敵のターン
        e_cmd = enemy_ai(enemy, player)     # "a"/"h"/"g"のいずれか
        if e_cmd == "a":
            dmg = do_attack(enemy, player)
        elif e_cmd == "h":
            amt = do_heal(enemy)
        elif e_cmd == "g":
            start_guard(enemy)

        if player["hp"] <= 0:
            print(f"{player["name"]}は負けてしまった")
            break

    
def main():
    player = {"name": "あなた", "hp": 60, "hp_max": 60, "atk":(10,18), "heal":(10,16), "guard":False}
    enemy = {"name": "ゴブリン", "hp": 55, "hp_max": 55, "atk":(8,16), "heal":(5,10), "guard":False}
    item = {"name": "ポーション", "heal": 20, "num": 3}
    battle(player, enemy, item)
    
if __name__ == "__main__":
    main()