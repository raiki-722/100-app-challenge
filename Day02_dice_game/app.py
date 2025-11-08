import random

print("ダイスゲームへようこそ！")
input("Enterキーでサイコロを振ります...")

player = random.randint(1, 6)
cpu = random.randint(1, 6)

print(f"あなたの出目： {player}")
print(f"コンピューターの出目：{cpu}")

if player > cpu:
    print("あなたの勝ち！")
elif cpu > player:
    print("コンピューターの勝ち！")
else:
    print("引き分け！")
    