# Day05: テキストクイズ（CSV版）
import csv
import random
import time

def load_questions(path="questions.csv"):
    """CSVから[{"q":..., "a":...}, ...]を作る"""
    items = []
    with open(path, encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            q = row.get("question", "").strip()
            a = row.get("answer", "").strip()
            if q and a:
                items.append({"q": q, "a": a})
    if not items:
        raise ValueError("問題が読み込めませんでした。questions.csvを確認してください。")
    return items

def ask_one(item, time_limit=None):
    """1問出題。time_limit(秒)があれば制限時間を適用"""
    print("\nQ.", item["q"])
    if time_limit:
        print(f"(制限時間: {time_limit}秒)")

    start = time.time()
    user = input("あなたの答え> ").strip()
    elapsed = time.time() - start

    if time_limit and elapsed > time_limit:
        print(f"時間切れ… ({elapsed:.1f}秒) 正解は「{item['a']}」")
        return False, elapsed

    if user.lower() == item["a"].lower():
        print("正解！🎉")
        return True, elapsed
    else:
        print(f"不正解… 正解は「{item['a']}」")
        return False, elapsed

def main():
    print("=== テキストクイズ（CSV版） ===")
    qa = load_questions("questions.csv")

    # 問題をシャッフル
    random.shuffle(qa)

    # 設定（必要に応じて変更）
    NUM_QUESTIONS = min(5, len(qa))  # 出題数
    TIME_LIMIT = 0                   # 0なら無効（例: 10 で10秒制限）
    print(f"出題数: {NUM_QUESTIONS} / 全{len(qa)}問\n")

    correct = 0
    times = []
    for i in range(NUM_QUESTIONS):
        ok, sec = ask_one(qa[i], time_limit=TIME_LIMIT)
        correct += int(ok)
        times.append(sec)

    avg_time = sum(times)/len(times) if times else 0.0
    print("\n=== 結果 ===")
    print(f"正解 {correct}/{NUM_QUESTIONS}  ({correct/NUM_QUESTIONS*100:.1f}%)")
    if TIME_LIMIT:
        print(f"平均回答時間: {avg_time:.2f} 秒")

if __name__ == "__main__":
    main()