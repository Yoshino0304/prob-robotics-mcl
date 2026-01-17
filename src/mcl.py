
import numpy as np



from sim import simulate_1d

from models import observation_likelihood_range_1d



def predict_particles(particles, u, sigma_move, rng):

    """運動モデル（予測ステップ）: x <- x + u + N(0, sigma_move^2)"""

    return particles + u + rng.normal(0.0, sigma_move, size=particles.shape)



def neff(weights):

    """有効サンプルサイズ Neff = 1 / sum(w^2)"""

    return 1.0 / np.sum(np.square(weights))



def run_pf_no_resample(

    T=60,

    N=800,

    x0_min=-5.0,

    x0_max=5.0,

    landmark=10.0,

    sigma_move=0.3,

    sigma_obs=0.7,

    seed=0,

    verbose=True,

):

    rng = np.random.default_rng(seed)



    x_true, u, z = simulate_1d(

        T=T, landmark=landmark, sigma_move=sigma_move, sigma_obs=sigma_obs, seed=seed

    )



    particles = rng.uniform(x0_min, x0_max, size=N)

    weights = np.ones(N) / N



    x_est = np.zeros(T)



    for t in range(T):

        if t > 0:

            particles = predict_particles(particles, u[t], sigma_move, rng)



        w = observation_likelihood_range_1d(z[t], particles, landmark, sigma_obs)

        w = w + 1e-300

        weights = w / np.sum(w)



        x_est[t] = np.sum(particles * weights)



        if verbose and (t % 10 == 0 or t == T-1):

            print(f"t={t:02d}  Neff={neff(weights):.1f}/{N}")



    return x_true, x_est



if __name__ == "__main__":

    x_true, x_est = run_pf_no_resample()

    rmse = np.sqrt(np.mean((x_true - x_est) ** 2))

    print("RMSE (no resample) =", rmse)

