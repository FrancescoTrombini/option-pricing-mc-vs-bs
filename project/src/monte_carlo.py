import numpy as np

def monte_carlo_option(S0, K, T, r, sigma, N=100000, tipo='call', seed=None):
    """
    Stima il prezzo di un'opzione europea (call o put) usando simulazione Monte Carlo
    tipo: 'call' o 'put'
    """
    if seed is not None:
        np.random.seed(seed)
    
    # Genera N campioni standard normali
    Z = np.random.randn(N)
    
    # Simula S_T secondo GBM
    S_T = S0 * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z)
    
    # Calcola payoff
    if tipo == 'call':
        X = np.maximum(S_T - K, 0)
    elif tipo == 'put':
        X = np.maximum(K - S_T, 0)
    else:
        raise ValueError("tipo deve essere 'call' o 'put'")
    
    # Prezzo stimato
    MC_price = np.exp(-r*T) * X.mean()
    
    # Errore standard e CI 95%
    SE = np.exp(-r*T) * X.std(ddof=1) / np.sqrt(N)
    CI_lower = MC_price - 1.96*SE
    CI_upper = MC_price + 1.96*SE
    
    return S_T, X, MC_price, SE, (CI_lower, CI_upper)


# Test rapido
if __name__ == "__main__":
    S0 = 100
    K = 100
    T = 1
    r = 0.05
    sigma = 0.2
    N = 100000

    # Call
    S_T_call, X_call, call_price, call_se, call_CI = monte_carlo_option(
        S0, K, T, r, sigma, N, tipo='call', seed=42
    )

    # Put
    S_T_put, X_put, put_price, put_se, put_CI = monte_carlo_option(
        S0, K, T, r, sigma, N, tipo='put', seed=42
    )

    # Stampa risultati
    print(f"Call MC: {call_price:.4f}, SE: {call_se:.4f}, CI 95%: [{call_CI[0]:.4f}, {call_CI[1]:.4f}]")
    print(f"Put MC : {put_price:.4f}, SE: {put_se:.4f}, CI 95%: [{put_CI[0]:.4f}, {put_CI[1]:.4f}]")
