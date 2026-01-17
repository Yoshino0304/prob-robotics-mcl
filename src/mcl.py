
import numpy as np

from sim import simulate_1d



def predict_particles(particles, u, sigma_move, rng):

    """

    運動モデル（予測ステップ）

    x <- x + u + N(0, sigma_move^2)

    """

    return particles + u + rng.normal(0.0, sigma_move, size=particles.shape)



def run_pf_predict_only(

    T=60,

    N=500,

    x0_min=-5.0,

    x0_max=5.0,

    sigma_move=0.3,

    seed=0,

):

    rng = np.random.default_rng(seed)



    # 真値生成（まだ使うだけ）

    x_true, u, z = simulate_1d(T=T, sigma_move=sigma_move, seed=seed)



    # 粒子初期化（prior）

    particles = rng.uniform(x0_min, x0_max, size=N)



    # 推定値（とりあえず粒子平均）

    x_est = np.zeros(T)



    for t in range(T):

        if t > 0:

            particles = predict_particles(particles, u[t], sigma_move, rng)



        x_est[t] = np.mean(particles)



    return x_true, x_est



if __name__ == "__main__":

    x_true, x_est = run_pf_predict_only()

    rmse = np.sqrt(np.mean((x_true - x_est) ** 2))

    print("RMSE (predict only) =", rmse)

