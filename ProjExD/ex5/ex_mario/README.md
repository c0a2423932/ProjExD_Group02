Mini Mario (簡易マリオ風プラットフォーマー)

このフォルダには pygame を使った最小限のマリオ風ゲームサンプルが入っています。
外部の画像や音は使わず、矩形でプレイヤー／敵／コイン／足場を表現しています。

ファイル
- mario.py: メイン実装
- requirements.txt: 依存（pygame）

操作方法（Windows / PowerShell）
1. 仮想環境を作る（任意）
   python -m venv venv
   .\venv\Scripts\Activate.ps1
2. 依存をインストール
   pip install -r requirements.txt
3. 実行
   python .\mario.py

操作キー
- ← / → / A / D: 左右移動
- Space / Z / ↑: ジャンプ

メモ
- 敵に当たるとリスポーン（スコアリセット）
- 敵を上から踏むと倒せる
- 追加機能（音、スプライト、スクロール、レベル読み込み）は希望があれば追加します
