
import numpy as np



def observation_likelihood_range_1d(z, x, landmark, sigma_obs):

    """

    観測モデル:

      z = |landmark - x| + N(0, sigma_obs^2)

    戻り値: p(z | x)  (粒子ごとの尤度)

    """

    pred = np.abs(landmark - x)



    # Gaussian pdf

    coef = 1.0 / (np.sqrt(2.0 * np.pi) * sigma_obs)

    p = coef * np.exp(-0.5 * ((z - pred) / sigma_obs) ** 2)



    return p

