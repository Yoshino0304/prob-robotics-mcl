# 1D MCL (Particle Filter)
確率ロボティクス課題として、**1次元ロボット**の自己位置推定を **MCL** で実装しました。

## 目的
移動、観測にノイズがある状況で、観測（z）と行動（u）からロボット位置を推定します。

## 補足
- 本実装は **1次元** の簡易設定です
- 出力画像は `src/outputs/` に保存されます

## 実装内容（MCLの流れ）
本実装では以下の手順で自己位置推定を行います。  
1. **予測**：運動モデルで粒子を移動  
2. **計測更新**：観測尤度により粒子の重みを更新  
3. **リサンプリング**：Neffが小さいときにsystematic resamplingを実行

## アルゴリズム解説（数式）

### 問題設定
状態（ロボット位置）を $x_t$、制御入力を $u_t$、観測を $z_t$ とする。  
本実装は1次元なので $x_t \in \mathbb{R}$。

- 運動モデル： $p(x_t \mid x_{t-1}, u_t)$  
- 観測モデル： $p(z_t \mid x_t)$

### ベイズフィルタ（予測・更新）
事後分布 $bel(x_t)=p(x_t \mid z_{1:t}, u_{1:t})$ は以下で更新

**予測（prediction）**
```math
\bar{bel}(x_t) = \int p(x_t \mid x_{t-1}, u_t)\, bel(x_{t-1})\, dx_{t-1}
```

**更新（correction）**
```math
bel(x_t) = \eta \, p(z_t \mid x_t)\, \bar{bel}(x_t)
```
ここで $\eta$ は正規化定数

### 粒子フィルタによる近似（MCL）
ベイズフィルタの分布 $bel(x_t)$ をそのまま計算するのは難しいので、MCLでは **粒子（サンプル）** を用いて近似
$N$ 個の粒子 $\{x_t^{(i)}\}_{i=1}^{N}$ と重み $\{w_t^{(i)}\}$ により、分布を表現

#### 1. 予測（粒子の移動）
各粒子を運動モデルに従って移動

```math
x_t^{(i)} \sim p(x_t \mid x_{t-1}^{(i)}, u_t)
```

#### 2. 計測更新（重み付け）
観測 $z_t$ が得られたとき、各粒子の位置 $x_t^{(i)}$ がどれくらい観測と整合するかを観測尤度 $p(z_t \mid x_t^{(i)})$ で評価して重みを更新

```math
\tilde{w}_t^{(i)} = w_{t-1}^{(i)}\, p(z_t \mid x_t^{(i)})
```
重みは合計が1になるように正規化
```math
w_t^{(i)} = \frac{\tilde{w}_t^{(i)}}{\sum_{j=1}^{N} \tilde{w}_t^{(j)}}
```

### 重みの退化と Neff
粒子フィルタでは、重みが一部の粒子に偏ると（退化）、実質的に有効な粒子数が減少  
その指標として **有効サンプルサイズ** $N_{\mathrm{eff}}$ を用いる

```math
N_{\mathrm{eff}} = \frac{1}{\sum_{i=1}^{N} (w_t^{(i)})^2}
```

本実装では $N_{\mathrm{eff}} < \frac{N}{2}$ のときにリサンプリングを行う。

### リサンプリング（systematic resampling）
リサンプリングでは、確率 $w_t^{(i)}$ に比例して粒子を複製
本実装では systematic resampling を用いている


### systematic resampling の手順（概要）
systematic resampling は、重みに比例した粒子の複製を効率よく行う手法である
累積分布（CDF）を使って、等間隔にサンプルを取る

```math
c_i = \sum_{k=1}^{i} w_t^{(k)}
```

手順は以下のようになっている

1. 重み $w_t^{(i)}$ から累積和 $c_i = \sum_{k=1}^{i} w_t^{(k)}$ を作る  
2. 一様乱数 $r \sim U(0, \frac{1}{N})$ を1つ生成  
3. $u_m$ を順に作る
```math
u_m = r + \frac{m-1}{N}
```
4. $u_m \le c_i$ を満たす最小の $i$ を選び、粒子 $x_t^{(i)}$ を採用する


この方法により、重みの大きい粒子が複製される

### 観測尤度（計測モデル）
本実装の観測モデルは次の式で表される
```math
z_t = |L - x_t| + \mathcal{N}(0, \sigma_{\mathrm{obs}}^2)
```

つまり、位置 $x_t$ にいるときの観測 $z_t$ は、ランドマーク位置 $L$ までの距離 $|L-x_t|$ に
ガウスノイズが加わったものになる

このとき観測尤度は、平均 $|L-x_t|$、分散 $\sigma_{\mathrm{obs}}^2$ の正規分布として表せる

```math
p(z_t \mid x_t) =
\frac{1}{\sqrt{2\pi\sigma_{\mathrm{obs}}^2}}
\exp\left(
-\frac{(z_t - |L - x_t|)^2}{2\sigma_{\mathrm{obs}}^2}
\right)
```

粒子フィルタでは、この $p(z_t \mid x_t^{(i)})$ を用いて各粒子の重みを更新する

#### 3. 推定値（位置の推定）
本実装では推定値を「重み付き平均」で計算

```math
\hat{x}_t = \sum_{i=1}^{N} w_t^{(i)} x_t^{(i)}
```

リサンプリング後は粒子の重みを一様に戻す

```math
w_t^{(i)} = \frac{1}{N}
```

## モデル
- 運動モデル：`x_t = x_{t-1} + u_t + N(0, σ_move^2)`
- 観測モデル：`z_t = |L - x_t| + N(0, σ_obs^2)`

## ファイル構成
- `src/sim.py`：真値と観測の生成
- `src/models.py`：観測尤度（計測モデル）
- `src/mcl.py`：MCL本体（Neff + resampling）
- `src/plot.py`：結果の図を保存

## 参考
- 上田先生『詳解 確率ロボティクス』の第8章、MCL（予測→計測更新→リサンプリング）の流れを参考にしました。
- 上田 隆一『詳解 確率ロボティクス Pythonによる基礎アルゴリズムの実装（KS理工学専門書）』  
  https://www.amazon.co.jp/dp/4065170060

## インストール方法
```bash
git clone https://github.com/Yoshino0304/prob-robotics-mcl.git
cd prob-robotics-mcl
pip3 install -r requirements.txt
```

## MCL実行
```bash
cd prob-robotics-mcl/src
python3 mcl.py
```
## 結果
### 結果の図を生成
```bash
python3 plot.py 
```
### 真値と推定（trajectory）
横軸が時刻 t 、縦軸が1次元位置 x です。  
**true** がシミュレーション上の真値、**estimate** がMCLによる推定値を表します。

<img src="src/outputs/trajectory.png" width="500">

### 推定誤差（error）
推定誤差 **error = estimate - true** の時間変化です。  
0に近いほど推定が正確で、タイトルにRMSE（誤差の平均的な大きさ）を表示します。

<img src="src/outputs/error.png" width="500">

## 必要なソフトウェア
- Python 3.8 以上（動作確認：Python 3.8.10）

## 動作確認済み環境
- Ubuntu 20.04

## ライセンス
- このソフトウェアパッケージは、3条項BSDライセンスの下、再頒布および使用が許可されます。
- © 2026 Taiki Yoshino

