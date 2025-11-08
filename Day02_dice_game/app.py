import argparse
import csv
import os
import random
from datetime import datetime

# ダイスのアスキーアート
DICE_ART = {
    1: ["+-------+",
        "|       |",
        "|   ●   |",
        "|       |",
        "+-------+"],
    2: ["+-------+",
        "| ●     |",
        "|       |",
        "|     ● |",
        "+-------+"],
    3: ["+-------+",
        "| ●     |",
        "|   ●   |",
        "|     ● |",
        "+-------+"],
    4: ["+-------+",
        "| ●   ● |",
        "|       |",
        "| ●   ● |",
        "+-------+"],
    5: ["+-------+",
        "| ●   ● |",
        "|   ●   |",
        "| ●   ● |",
        "+-------+"],
    6: ["+-------+",
        "| ●   ● |",
        "| ●   ● |",
        "| ●   ● |",
        "+-------+"],
}

# ダイスの見た目の定義
def print_dice(player_roll, cpu_roll, player_name="You", cpu_name="CPU"):
    left = DICE_ART[player_roll]
    right = DICE_ART[cpu_roll]
    title = f"{player_name:^11} vs {cpu_name:^11}"
    print(title)
    for l, r in zip(left, right):
        print(f"{l}   {r}")
    print(f"{player_name}: {player_roll}   {cpu_name}: {cpu_roll}")

#　対戦結果の記録
def log_result(path, row):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    file_exists = os.path.exists(path)
    with open(path, "a", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        if not file_exists:
            w.writerow(["timestamp","player","cpu","winner","player_point","cpu_point","rule"])
        w.writerow(row)

#　１ラウンド対戦する
def play_round(args, player_name="You", cpu_name="CPU"):
    input("Enterキーでサイコロを振る…")
    player = random.randint(1, 6)
    cpu = random.randint(1, 6)
    print_dice(player, cpu, player_name, cpu_name)

    # クリティカル計算
    p_point = 0
    c_point = 0
    rule_note = []
    if player > cpu:
        p_point = 1
        rule_note.append("win")
    elif player < cpu:
        c_point = 1
        rule_note.append("lose")
    else:
        # 引き分けの扱い
        if args.draw == "reroll":
            print("引き分け！リロールします。")
            return play_round(args, player_name, cpu_name)
        elif args.draw == "give":
            p_point = 1
            c_point = 1
            rule_note.append("draw-give")

    if args.critical and player == 6 and p_point > 0:
        p_point += 1
        rule_note.append("critical+1")
    if args.critical and cpu == 6 and c_point > 0:
        c_point += 1
        rule_note.append("critical+1(cpu)")

    # 勝者表示（同点加点のときは勝者なし）
    winner = "-"
    if p_point > c_point:
        winner = player_name
        print(f"→ {player_name} の勝ち (+{p_point})")
    elif c_point > p_point:
        winner = cpu_name
        print(f"→ {cpu_name} の勝ち (+{c_point})")
    else:
        print("→ 双方にポイント")

    # ログ
    log_result(
        path="logs/dice_log.csv",
        row=[datetime.now().isoformat(timespec="seconds"),
             player_name, cpu_name, winner, p_point, c_point, "|".join(rule_note)]
    )
    return p_point, c_point

#　プログラムのメイン機能
def main():
    parser = argparse.ArgumentParser(description="Day02: ダイス・デュエル")
    parser.add_argument("--best", type=int, default=3,
                        help="Best of N（奇数を推奨）。例: 3なら先取2、5なら先取3")
    parser.add_argument("--no-critical", dest="critical", action="store_false",
                        help="クリティカル(6で+1点)を無効化")
    parser.add_argument("--draw", choices=["reroll","give"], default="reroll",
                        help="引き分け時の処理: reroll(振り直し) / give(双方に1点)")
    parser.add_argument("--name", type=str, default="You", help="プレイヤー名")
    args = parser.parse_args()

    if args.best < 1:
        print("Best of N は1以上を指定してください。例: 3, 5, 7")
        return
    target = args.best // 2 + 1  # 先取ポイント

    print("🎲 ダイス・デュエル（改良版）へようこそ！")
    print(f"- 先取: {target}（Best of {args.best}）")
    print(f"- クリティカル: {'有効' if args.critical else '無効'}")
    print(f"- 引き分け: {'リロール' if args.draw=='reroll' else '双方1点'}")
    print("- Enterで開始します。")
    input()

    p_total = 0
    c_total = 0
    round_no = 1
    while p_total < target and c_total < target:
        print(f"\n--- Round {round_no} ---")
        p, c = play_round(args, player_name=args.name, cpu_name="CPU")
        p_total += p
        c_total += c
        print(f"[Score] {args.name}: {p_total}  CPU: {c_total}")
        round_no += 1

    print("\n===== 結果 =====")
    if p_total > c_total:
        print(f"🏆 Winner: {args.name}（{p_total} - {c_total}）")
    else:
        print(f"🏆 Winner: CPU（{c_total} - {p_total}）")
    print("対戦ありがとうございました！")

if __name__ == "__main__":
    main()
