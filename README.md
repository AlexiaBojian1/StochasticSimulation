# StochasticSimulation

A curated collection of compact Python and C++ examples that illustrate core ideas from stochastic simulation, Monte‑Carlo methods and stochastic‑process theory.

---

##  Repository layout

| Folder                                  | Main focus                                                     |  Highlights                                                                                   |
| --------------------------------------- | -------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| **CentralLimitTheorem/**                | Visual & empirical demonstrations of the Central Limit Theorem | Monte‑Carlo estimation of the birthday‑paradox probability, histogram convergence to 𝒩(0, 1) |
| **MonteCarlo/**                         | Generic Monte‑Carlo estimators & variance‑reduction tricks     | Importance sampling, control variates, etc.                                                   |
| **Discrete‑timeStochasticProcesses/**   | Random walks & Markov chains in discrete time                  | Simple & biased random walks, branching processes                                             |
| **Continuous‑timeStochasticProcesses/** | Continuous‑time processes & Itô diffusions                     | Brownian motion path generator, Poisson process skeleton                                      |
| **Discrete‑Event Simulation/**          | Event‑driven simulation framework                              | M/M/1 queue, waiting‑time distribution study                                                  |

> Each directory is intentionally **self‑contained** – jump directly to the topic that interests you without pulling in unnecessary dependencies.

---

##  Quick start

```bash
# Clone the repo
$ git clone https://github.com/AlexiaBojian1/StochasticSimulation.git
$ cd StochasticSimulation

# (Optional) create a virtual environment
$ python -m venv .venv
$ source .venv/bin/activate    # Windows: .venv\Scripts\activate.bat

# Install the minimal scientific‑Python stack
$ pip install -r requirements.txt   # or see below
```

### Minimal requirements

| Package            | Why it’s needed                              |
| ------------------ | -------------------------------------------- |
| Python ≥ 3.9       | language of most examples                    |
| numpy              | fast vectorised numerics                     |
| scipy              | random‑variable generators & stats helpers   |
| matplotlib         | plotting & visualisation                     |
| pandas (optional)  | tabular output for some notebooks            |
| **C++17 compiler** | required only for the `*.cpp` demonstrations |

If a `requirements.txt` file is missing, simply run:

```bash
pip install numpy scipy matplotlib pandas
```

---

## ▶️ Running a demo

```bash
# Central‑Limit‑Theorem demo – histogram of sample means\python CentralLimitTheorem/clt_birthday.py --n-samples 100000
```

Most scripts accept `-h`/`--help` to display their command‑line options.
