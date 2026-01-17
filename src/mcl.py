
import numpy as np



from sim import simulate_1d

from models import observation_likelihood_range_1d



def predict_particles(particles, u, sigma_move, rng):

    return particles + u + rng.normal(0.0, sigma_move, size=particles.shape)



def neff(weights):

    return 1.0 / np.sum(weights * weights)



def systematic_resample(particles, weights, rng):

    N = len(particles)

    positions = (rng.random() + np.arange(N)) / N

    cumsum = np.cumsum(weights)

    idx = np.searchsorted(cumsum, positions)

    return particles[idx]



def run_pf_with_resample(

    T=60,

    N=800,

    x0_min=-5.0,

    x0_max=5.0,

    landmark=10.0,

    sigma_move=0.3,

    sigma_obs=0.7,

    seed=0,

    resample_ratio=0.5,   # Neff < resample_ratio*N でリサンプル

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



        n_eff = neff(weights)



        # 退化してたらリサンプル

        if n_eff < resample_ratio * N:

            particles = systematic_resample(particles, weights, rng)

            weights = np.ones(N) / N



        if t % 10 == 0 or t == T - 1:

            print("t=", t, "Neff=", round(n_eff, 1), "/", N)



    return x_true, x_est



if __name__ == "__main__":

    x_true, x_est = run_pf_with_resample()

    rmse = np.sqrt(np.mean((x_true - x_est) ** 2))

    print("RMSE (resample) =", rmse)

