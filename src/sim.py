
import numpy as np



def simulate_1d(

    T=60,

    x0=0.0,

    landmark=10.0,

    sigma_move=0.3,

    sigma_obs=0.7,

    seed=0,

):

    """

    1次元ロボットの真値シミュレーション

    状態: x_t

    行動: u_t in {+1, -1}

    観測: z_t = |landmark - x_t| + noise

    """

    rng = np.random.default_rng(seed)



    x_true = np.zeros(T)

    u = np.ones(T)

    z = np.zeros(T)



    x_true[0] = x0



    # 行動パターン：基本は右(+1)、たまに左(-1)

    u[::10] = -1.0



    for t in range(T):

        if t > 0:

            x_true[t] = x_true[t-1] + u[t] + rng.normal(0.0, sigma_move)



        z[t] = np.abs(landmark - x_true[t]) + rng.normal(0.0, sigma_obs)



    return x_true, u, z



if __name__ == "__main__":

    x_true, u, z = simulate_1d()

    print("x_true[:5] =", x_true[:5])

    print("u[:5]      =", u[:5])

    print("z[:5]      =", z[:5])

