# 1D MCL (Particle Filter)
確率ロボティクス課題として、**1次元ロボット**の自己位置推定を **MCL** で実装しました。

## 目的
移動、観測にノイズがある状況で、観測（z）と行動（u）からロボット位置を推定します。

## 補足
- 本実装は **1次元** の簡易設定です
- 出力画像は `src/outputs/` に保存されます

## インストール方法
```bash
git clone https://github.com/Yoshino0304/prob-robotics-mcl.git
```

## MCL実行
```bash
cd src
python3 mcl.py
```
## 結果
### 結果の図を生成
```bash
python3 plot.py 
```
### 真値と推定（trajectory）
横軸が時刻 `t`、縦軸が1次元位置 `x` です。  
`true` がシミュレーション上の真値、`estimate` がMCLによる推定値を表します。

![](src/outputs/trajectory.png)

### 推定誤差（error）
推定誤差 `error = estimate - true` の時間変化です。  
0に近いほど推定が正確で、タイトルにRMSE（誤差の平均的な大きさ）を表示します。

![](src/outputs/error.png)