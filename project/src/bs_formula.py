import numpy as np
from scipy.stats import norm

def black_scholes_option(S0, K, T, r, sigma, tipo='call'):
    """
    Calcola il prezzo di un'opzione europea (call o put) usando Black-Scholes
    tipo: 'call' o 'put'
    """
    d1 = (np.log(S0 / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    if tipo == 'call':
        prezzo = S0 * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    elif tipo == 'put':
        prezzo = K * np.exp(-r * T) * norm.cdf(-d2) - S0 * norm.cdf(-d1)
    else:
        raise ValueError("tipo deve essere 'call' o 'put'")
    
    return prezzo

# Test rapido
if __name__ == "__main__":
    S0 = 100
    K = 100
    T = 1
    r = 0.05
    sigma = 0.2
    
    call_price = black_scholes_option(S0, K, T, r, sigma, tipo='call')
    put_price  = black_scholes_option(S0, K, T, r, sigma, tipo='put')
    
    print(f"Prezzo Call BS: {call_price:.4f}")
    print(f"Prezzo Put BS: {put_price:.4f}")


