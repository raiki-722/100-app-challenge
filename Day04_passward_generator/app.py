# app.py
import secrets
import string
import streamlit as st

AMBIGUOUS = "Il1O0"  # 紛らわしい文字

def build_pool(use_upper, use_lower, use_digits, use_symbols, exclude_ambiguous):
    pools = []
    if use_upper:
        pools.append(string.ascii_uppercase)
    if use_lower:
        pools.append(string.ascii_lowercase)
    if use_digits:
        pools.append(string.digits)
    if use_symbols:
        pools.append("!@#$%^&*()-_=+[]{};:,<.>/?")

    pool = "".join(pools)
    if exclude_ambiguous:
        pool = "".join(ch for ch in pool if ch not in AMBIGUOUS)
    return pools, pool

def generate_password(length, use_upper, use_lower, use_digits, use_symbols, exclude_ambiguous):
    pools, pool = build_pool(use_upper, use_lower, use_digits, use_symbols, exclude_ambiguous)
    # 安全チェック
    if not pool:
        raise ValueError("文字の種類を1つ以上選んでください。")
    need = len([p for p in (use_upper, use_lower, use_digits, use_symbols) if p])
    if length < need:
        raise ValueError(f"長さが短すぎます。選んだ種類の数（{need}）以上にしてください。")

    # 各カテゴリから最低1文字ずつ
    required = []
    if use_upper:  required.append(secrets.choice(string.ascii_uppercase))
    if use_lower:  required.append(secrets.choice(string.ascii_lowercase))
    if use_digits: required.append(secrets.choice(string.digits))
    if use_symbols: required.append(secrets.choice("!@#$%^&*()-_=+[]{};:,<.>/?"))

    if exclude_ambiguous:
        required = [c for c in required if c not in AMBIGUOUS] or [secrets.choice(pool)]

    remain = [secrets.choice(pool) for _ in range(length - len(required))]
    chars = required + remain

    # シャッフル（secretsで安全に）
    for i in range(len(chars) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        chars[i], chars[j] = chars[j], chars[i]
    return "".join(chars)

def score_password(pwd):
    """超シンプル強度スコア（0〜4）"""
    score = 0
    if any(c.islower() for c in pwd): score += 1
    if any(c.isupper() for c in pwd): score += 1
    if any(c.isdigit() for c in pwd): score += 1
    if any(c in "!@#$%^&*()-_=+[]{};:,<.>/?"
           for c in pwd): score += 1
    # 長さボーナス
    if len(pwd) >= 16: score += 1
    return min(score, 5)

# ===== Streamlit UI =====
st.set_page_config(page_title="パスワード生成器", page_icon="🔐", layout="centered")
st.title("🔐 パスワード生成器（Streamlit）")
st.caption("長さと文字種を選んで「生成」ボタンを押すだけ。secretsモジュールで安全に生成。")

with st.form("generator"):
    length = st.slider("長さ", min_value=8, max_value=64, value=16, step=1)
    col1, col2 = st.columns(2)
    with col1:
        use_upper = st.checkbox("大文字 A-Z", value=True)
        use_lower = st.checkbox("小文字 a-z", value=True)
        use_digits = st.checkbox("数字 0-9", value=True)
    with col2:
        use_symbols = st.checkbox("記号 !@#$...", value=False)
        exclude_ambiguous = st.checkbox("紛らわしい文字(I l 1 O 0)を除外", value=True)
    submitted = st.form_submit_button("生成する")

if submitted:
    try:
        pwd = generate_password(length, use_upper, use_lower, use_digits, use_symbols, exclude_ambiguous)
        st.success("パスワードを生成しました")
        st.code(pwd)  # コードブロックはコピーしやすい
        s = score_password(pwd)
        labels = ["弱い", "やや弱い", "普通", "やや強い", "強い", "とても強い"]
        st.progress(s / 5)
        st.write(f"強度の目安: **{labels[s]}**")
        st.download_button("テキストとして保存", data=pwd, file_name="password.txt")
    except ValueError as e:
        st.error(str(e))

with st.expander("使い方メモ"):
    st.markdown(
        "- **長さは16以上**がおすすめ\n"
        "- **記号**を入れると強度UP\n"
        "- **紛らわしい文字を除外**で読みやすさUP\n"
        "- 生成したパスワードは**その場限りの表示**がおすすめ（保存は慎重に）"
    )
