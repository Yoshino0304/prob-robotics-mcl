
import os

import numpy as np

import matplotlib.pyplot as plt



from mcl import run_pf_with_resample



def ensure_dir(path):

    os.makedirs(path, exist_ok=True)



def main():

    out_dir = "outputs"

    ensure_dir(out_dir)



    x_true, x_est = run_pf_with_resample()



    t = np.arange(len(x_true))

    err = x_est - x_true

    rmse = np.sqrt(np.mean(err**2))



    # trajectory

    plt.figure()

    plt.plot(t, x_true, label="true")

    plt.plot(t, x_est, label="estimate")

    plt.xlabel("t")

    plt.ylabel("x")

    plt.title("1D MCL: True vs Estimate")

    plt.legend()

    plt.tight_layout()

    plt.savefig(os.path.join(out_dir, "trajectory.png"), dpi=200)

    plt.close()



    # error

    plt.figure()

    plt.plot(t, err, label="est - true")

    plt.xlabel("t")

    plt.ylabel("error")

    plt.title(f"Error (RMSE={rmse:.3f})")

    plt.legend()

    plt.tight_layout()

    plt.savefig(os.path.join(out_dir, "error.png"), dpi=200)

    plt.close()



    print("saved:", os.path.join(out_dir, "trajectory.png"))

    print("saved:", os.path.join(out_dir, "error.png"))



if __name__ == "__main__":

    main()

