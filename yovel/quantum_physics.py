import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# =========================
# 1. Load data
# =========================
df = pd.read_csv("atom_distributions.csv")

x = df["bin"].values.astype(float)
time_cols = [c for c in df.columns if c != "bin"]

# =========================
# 2. Gaussian model
# =========================
def gaussian(x, delta):
    return (1 / (np.sqrt(2*np.pi) * delta)) * np.exp(-(x**2) / (2 * delta**2))

# =========================
# 3. Plot ALL distributions together + Gaussian fits
# =========================
plt.figure(figsize=(8,6))
colors = plt.cm.viridis(np.linspace(0, 1, len(time_cols)))

times = []
deltas = []

for i, col in enumerate(time_cols):
    y = df[col].values

    # fit Gaussian → Δ(t)
    popt, _ = curve_fit(gaussian, x, y, p0=[1.0])
    delta_fit = popt[0]

    # extract time (t2_us → 2)
    t = float(col.replace("t", "").replace("_us", ""))

    times.append(t)
    deltas.append(delta_fit)

    # smooth curve
    x_fit = np.linspace(min(x), max(x), 400)
    y_fit = gaussian(x_fit, delta_fit)

    # plot raw data + fit
    plt.plot(x, y, 'o', color=colors[i], alpha=0.5)
    plt.plot(x_fit, y_fit, '-', color=colors[i],
             label=f"{col}, Δ={delta_fit:.3f}")

plt.xlabel("Position (μm)")
plt.ylabel("Probability density")
plt.title("Gaussian fits for all times (overlay)")
plt.grid()
plt.legend()
plt.show()

# =========================
# 4. Sort Δ(t)
# =========================
times = np.array(times)
deltas = np.array(deltas)

idx = np.argsort(times)
times = times[idx]
deltas = deltas[idx]

# =========================
# 5. Plot Δ(t)
# =========================
plt.figure()
plt.plot(times, deltas, 'o-', label="Δ(t)")
plt.xlabel("Time (μs)")
plt.ylabel("Δ (μm)")
plt.title("Wavepacket spreading")
plt.grid()
plt.legend()
plt.show()

# =========================
# 6. Linear regression Δ(t)
# =========================
a, b = np.polyfit(times, deltas, 1)

t_fit = np.linspace(min(times), max(times), 200)
delta_fit_line = a * t_fit + b

plt.figure()
plt.plot(times, deltas, 'o', label="data")
plt.plot(t_fit, delta_fit_line, '-', label=f"fit: Δ = {a:.4f} t + {b:.4f}")
plt.xlabel("Time (μs)")
plt.ylabel("Δ (μm)")
plt.title("Linear fit of Δ(t)")
plt.grid()
plt.legend()
plt.show()

print("Slope a =", a)
print("Intercept b =", b)

# =========================
# 7. Mass calculation
# =========================
hbar = 1.054e-34  # J·s
Delta0 = 0.07e-6  # m (given experimentally)

# slope in SI (μm/μs == m/s)
a_SI = a

m = hbar / (a_SI * Delta0)

print("\nEstimated mass (kg):")
print(m)

# =========================
# 8. Convert to amu
# =========================
amu = 1.6605e-27
m_amu = m / amu

print("\nEstimated mass (amu):")
print(m_amu)