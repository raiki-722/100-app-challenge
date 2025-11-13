# Day05 - テキストクイズ
- 目的: CSV読み込み/ユーザー入力/採点/シャッフルを体験
- 使い方:
  1) questions.csv を編集
  2) python app.py
- 拡張アイデア: 4択化、カテゴリ出題、結果保存、Streamlit化

ここで学べる
csv.DictReader でヘッダー付きCSVを読む
random.shuffle() で出題をランダム化
ちょい発展の制限時間計測（time.time()）

さらに一歩（任意の拡張案）
機能	学べること
選択肢式（4択）	CSVを「question,choice1,choice2,choice3,answer」に拡張し表示
カテゴリ出題	CSVに「category」列を追加→選択したカテゴリだけ出題
スコア保存	csv で「日付, 正答率, 平均時間」をresults.csvへ追記
Streamlit版	フォームUI・ボタン・正解アニメーション（Day06候補）