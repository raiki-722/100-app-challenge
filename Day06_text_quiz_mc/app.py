# Day06: 4択テキストクイズ（Streamlit GUI）
# 目的: CSV読み込み / 選択肢ボタン / スコア・進捗表示 / 再スタート

import streamlit as st
import pandas as pd
import random
from io import StringIO
from typing import List, Dict

st.set_page_config(page_title="4択テキストクイズ", page_icon="🧠", layout="centered")
st.title("🧠 4択テキストクイズ（Streamlit）")
st.caption("CSVから問題を読み込んで、ボタンで回答できます。学習ログには出題数と正答数を表示。")

# ---------------------------
# 1) データ読み込みの関数
# ---------------------------
def load_questions_from_csv(file) -> List[Dict]:
    """CSVから [{'q':..., 'choices': [...], 'answer_idx': 0-3}, ...] を作る"""
    df = pd.read_csv(file)
    # 必要な列があるか確認
    needed = ["question", "choice1", "choice2", "choice3", "choice4", "answer"]
    if not all(col in df.columns for col in needed):
        raise ValueError("CSVのヘッダーは question,choice1,choice2,choice3,choice4,answer が必要です。")
    items = []
    for _, row in df.iterrows():
        q = str(row["question"]).strip()
        choices = [str(row[f"choice{i}"]).strip() for i in range(1,5)]
        ans = str(row["answer"]).strip()
        if not (q and all(choices) and ans.isdigit()):
            continue
        idx = int(ans) - 1  # 1-4 -> 0-3
        if idx not in (0,1,2,3):
            continue
        items.append({"q": q, "choices": choices, "answer_idx": idx})
    if not items:
        raise ValueError("有効な問題がありません。CSVの内容を確認してください。")
    return items

# ---------------------------
# 2) 初期データの用意（サンプル or questions.csv）
# ---------------------------
def get_default_questions() -> List[Dict]:
    csv_text = """question,choice1,choice2,choice3,choice4,answer
Pythonで乱数を出す標準モジュールは？,math,random,time,os,2
リストの長さを返す関数は？,len,size,length,count,1
文字列を小文字にするメソッドは？,lowercase,downcase,lower,to_lower,3
辞書型のキー集合を得るメソッドは？,get,items,keys,values,3
for文で回数を指定するとき使うのは？,loop,range,seq,list,2
"""
    return load_questions_from_csv(StringIO(csv_text))

# ---------------------------
# 3) セッション状態（ゲーム進行用）
# ---------------------------
if "questions" not in st.session_state:
    # まずはサンプル問題をロード
    st.session_state.questions = get_default_questions()
    random.shuffle(st.session_state.questions)
if "index" not in st.session_state:
    st.session_state.index = 0         # 何問目か（0始まり）
if "correct" not in st.session_state:
    st.session_state.correct = 0       # 正解数
if "last_choice" not in st.session_state:
    st.session_state.last_choice = None  # 直前に選んだ選択肢番号
if "locked" not in st.session_state:
    st.session_state.locked = False    # 回答後はロックして次へ
if "choices" not in st.session_state:
    st.session_state.choices = None      # 今表示している選択肢の並び
if "correct_idx" not in st.session_state:
    st.session_state.correct_idx = None  # その並びでの正解インデックス
if "choices_index" not in st.session_state:
    st.session_state.choices_index = -1  # どの問題(index)用の並びか

# ---------------------------
# 4) CSVアップロードUI（任意）
# ---------------------------
with st.expander("📥 CSVを読み込む（任意）"):
    up = st.file_uploader("questions.csv を選択（ヘッダー: question,choice1..4,answer）", type=["csv"])
    col_u1, col_u2 = st.columns([1,1])
    with col_u1:
        if st.button("このCSVで開始"):
            if up is not None:
                try:
                    st.session_state.questions = load_questions_from_csv(up)
                    random.shuffle(st.session_state.questions)
                    st.session_state.index = 0
                    st.session_state.correct = 0
                    st.session_state.last_choice = None
                    st.session_state.locked = False
                    st.session_state.choices = None
                    st.session_state.correct_idx = None
                    st.session_state.choices_index = -1
                    st.success("CSVを読み込みました。クイズを開始します。")
                except Exception as e:
                    st.error(str(e))
            else:
                st.warning("CSVファイルを選択してください。")
    with col_u2:
        if st.button("サンプルで開始"):
            st.session_state.questions = get_default_questions()
            random.shuffle(st.session_state.questions)
            st.session_state.index = 0
            st.session_state.correct = 0
            st.session_state.last_choice = None
            st.session_state.locked = False
        # 🔴 これを追加：選択肢の並び情報もリセット
            st.session_state.choices = None
            st.session_state.correct_idx = None
            st.session_state.choices_index = -1
            st.info("サンプル問題で開始しました。")
            st.rerun()
# ---------------------------
# 5) 現在の問題を取り出す
# ---------------------------
q_list = st.session_state.questions
idx = st.session_state.index
total = len(q_list)

# すべて終了したらリザルト画面
if idx >= total:
    st.subheader("🎉 結果")
    rate = st.session_state.correct / total * 100 if total else 0
    st.metric(label="正解数 / 出題数", value=f"{st.session_state.correct} / {total}")
    st.progress(st.session_state.correct / total if total else 0.0)
    st.write(f"正答率: **{rate:.1f}%**")

    if st.button("🔁 最初からもう一度"):
        st.session_state.index = 0
        st.session_state.correct = 0
        st.session_state.last_choice = None
        st.session_state.locked = False
    st.stop()

# 1問分のデータ（選択肢はここでシャッフル＆正解位置追跡）
item = q_list[idx]

# まだこの問題用の選択肢を作っていない場合だけシャッフルする
if st.session_state.choices is None or st.session_state.choices_index != idx:
    base_choices = item["choices"][:]                # 元の4つ
    correct_text = base_choices[item["answer_idx"]]  # 正解のテキスト

    random.shuffle(base_choices)                     # ここで一度だけシャッフル
    correct_idx = base_choices.index(correct_text)   # 並び替え後の正解位置を取得

    # セッションに保存
    st.session_state.choices = base_choices
    st.session_state.correct_idx = correct_idx
    st.session_state.choices_index = idx

# 以降はセッションから取り出して使う
choices = st.session_state.choices
correct_idx = st.session_state.correct_idx

# ---------------------------
# 6) 表示：問題文・進捗
# ---------------------------
st.markdown(f"**Q{idx+1}/{total}. {item['q']}**")
st.progress(idx / total)

# ---------------------------
# 7) 選択肢ボタン
# ---------------------------
def on_select(choice_idx: int):
    # 1回回答したらロックして結果表示だけにする
    if st.session_state.locked:
        return
    st.session_state.last_choice = choice_idx
    st.session_state.locked = True
    if choice_idx == correct_idx:
        st.session_state.correct += 1

cols = st.columns(2)
for i, ch in enumerate(choices):
    with cols[i % 2]:
        # 回答後は色を変えてフィードバック
        if st.session_state.locked:
            if i == correct_idx:
                st.button(f"✅ {i+1}. {ch}", disabled=True, key=f"c{i}")
            elif i == st.session_state.last_choice:
                st.button(f"❌ {i+1}. {ch}", disabled=True, key=f"c{i}")
            else:
                st.button(f"{i+1}. {ch}", disabled=True, key=f"c{i}")
        else:
            st.button(f"{i+1}. {ch}", on_click=on_select, args=(i,), key=f"c{i}")

# 回答フィードバック
if st.session_state.locked:
    if st.session_state.last_choice == correct_idx:
        st.success("正解！🎉")
    else:
        st.error(f"不正解… 正解は **{choices[correct_idx]}**")
else:
    st.info("答えを選んでください。")

# ---------------------------
# 8) ナビゲーション（次の問題へ / スキップ）
# ---------------------------
col_next1, col_next2 = st.columns([1,1])
with col_next1:
    if st.button("▶ 次の問題へ", use_container_width=True):
        # 未回答のまま次へを押したらスキップ扱い
        st.session_state.index += 1
        st.session_state.last_choice = None
        st.session_state.locked = False
        st.rerun()
with col_next2:
    if st.button("⏭ スキップ", use_container_width=True, disabled=st.session_state.locked is False):
        st.session_state.index += 1
        st.session_state.last_choice = None
        st.session_state.locked = False
        st.rerun()

# フッターに現在スコア
st.caption(f"Score: {st.session_state.correct} / {total}")

