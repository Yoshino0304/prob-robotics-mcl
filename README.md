# 1D MCL (Particle Filter)
確率ロボティクス課題として、**1次元ロボット**の自己位置推定を **MCL** で実装しました。

## 目的
移動、観測にノイズがある状況で、観測（z）と行動（u）からロボット位置を推定します。

## 補足
- 本実装は **1次元** の簡易設定です
- 出力画像は `src/outputs/` に保存されます

## インストール方法
` git clone https://github.com/Yoshino0304/prob-robotics-mcl.git` 

## MCL実行
```bash
cd src
python3 mcl.py


## 結果の図を生成
` python3 plot.py` 


