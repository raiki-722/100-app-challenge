import time
import random

# 出題する単語のリスト
WORDS = [
    "python", "streamlit", "variable", "function", "random",
    "soccer", "anime", "typing", "wizard", "goblin"
]

def ask_word(round_no, word):
    """1問ぶんのタイピングを行い、正解かどうかと時間を返す"""
    print(f"\n--- 第 {round_no} 問 ---")
    print(f"この単語を入力してください： {word}")
    input("準備ができたら Enter を押すとスタートします…")

    start = time.time()
    user = input("> ")
    end = time.time()

    elapsed = end - start  # かかった時間（秒）

    if user == word:
        print(f"正解！ {elapsed:.2f} 秒かかりました。")
        return True, elapsed
    else:
        print(f"不正解… 正解は「{word}」でした。")
        return False, elapsed

def main():
    print("=== タイピングスピードゲーム Day07 ===")
    print("表示された英単語をできるだけ早く、正確に入力してください。")
    print("全部で 5 問 出題します。\n")

    num_rounds = 5  # 出題数
    correct_count = 0
    times = []

    for i in range(1, num_rounds + 1):
        # ランダムに単語を選ぶ
        word = random.choice(WORDS)
        is_correct, elapsed = ask_word(i, word)

        if is_correct:
            correct_count += 1
        times.append(elapsed)

    # 結果表示
    print("\n=== 結果 ===")
    avg_time = sum(times) / len(times)
    print(f"正解数: {correct_count} / {num_rounds}")
    print(f"平均タイム: {avg_time:.2f} 秒")

    if correct_count == num_rounds:
        print("すごい！全問正解！🎉")
    elif correct_count == 0:
        print("どんまい！慣れればきっと速くなるよ💪")
    else:
        print("おつかれさま！明日は今日より 0.5 秒だけ速くなろう🔥")

if __name__ == "__main__":
    main()