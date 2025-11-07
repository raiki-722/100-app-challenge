import time
import random

print("準備はいい？ Enterキーを押すとスタート！")
input()
print("...")
time.sleep(random.uniform(2,5))
print("今だ！ Enterキーを押して！")
start = time.time()
input()
end = time.time()
print(f"反応速度: {end - start:.3f} 秒")