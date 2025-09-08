# Pricing a European Option: Monte Carlo vs Black–Scholes

This repository contains the code and results for a project comparing
Monte Carlo simulation with the Black–Scholes formula in pricing
European call and put options.

## Structure
- `src/` – Python implementations (Black–Scholes formula, Monte Carlo estimator, experiments runner).
- `data/` – CSV output with results (MC vs BS).
- `figures/` – Generated plots (convergence, payoff histograms).
- `paper/` – LaTeX source and tables for the paper.
- `requirements.txt` – List of Python dependencies.

## How to Reproduce
Install the required libraries:

```bash
pip install -r requirements.txt

Run the experiments:

```bash
python src/run_experiments.py

This generates CSV results in `data/` and figures in `figures/`.

## License
MIT License
