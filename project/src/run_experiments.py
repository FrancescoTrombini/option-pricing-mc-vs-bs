import sys 
import os 
# Aggiunge la cartella src al path di Python 

sys.path.append(os.path.join(os.path.dirname(__file__), 'src')) 
from bs_formula import black_scholes_option 
from monte_carlo import monte_carlo_option 
import pandas as pd 
import matplotlib.pyplot as plt 
import numpy as np 

S0 = 100 
K = 100 
T = 1 
r = 0.05 
sigma = 0.2 
Ns = [10**3, 2*10**3, 3*10**3, 
      10**4, 2*10**4, 3*10**4, 
      10**5, 2*10**5, 3*10**5, 
      10**6, 2*10**6, 3*10**6, 
      10**7] # diversi N 

BS_call = black_scholes_option(S0, K, T, r, sigma, tipo='call') 
BS_put = black_scholes_option(S0, K, T, r, sigma, tipo='put') 

results = [] 

for N in Ns: 
    S_T_call, X_call, call_price, call_se, call_CI = monte_carlo_option(S0, K, T, r, sigma, N, tipo='call', seed=42) 
    S_T_put, X_put, put_price, put_se, put_CI = monte_carlo_option(S0, K, T, r, sigma, N, tipo='put', seed=42) 
    
    # Errori 
    call_abs_err = abs(call_price - BS_call) 
    call_rel_err = call_abs_err / BS_call 
    put_abs_err = abs(put_price - BS_put) 
    put_rel_err = put_abs_err / BS_put 
    results.append({ "N": N, "Call_MC": call_price, 
                    "Call_SE": call_se, 
                    "Call_CI_lower": call_CI[0], 
                    "Call_CI_upper": call_CI[1], 
                    "Call_abs_err": call_abs_err, 
                    "Call_rel_err": call_rel_err, 
                    "Put_MC": put_price, 
                    "Put_SE": put_se, 
                    "Put_CI_lower": put_CI[0], 
                    "Put_CI_upper": put_CI[1], 
                    "Put_abs_err": put_abs_err, 
                    "Put_rel_err": put_rel_err }) 
    
df_results = pd.DataFrame(results) 
print(df_results)
    
df_results.to_csv("results_mc_vs_bs.csv", index=False) 

# Assicurati che la cartella figures esista 
os.makedirs("figures", exist_ok=True)

# Convergenza MC vs BS 

# Errori

Ns = df_results['N'] 
call_error = df_results['Call_abs_err'] 
put_error = df_results['Put_abs_err'] 
plt.figure(figsize=(6,4)) 
plt.loglog(Ns, call_error, marker='o', label='Call') 
plt.loglog(Ns, put_error, marker='s', label='Put') 
plt.xlabel('Number of simulations N') 
plt.ylabel('Absolute error MC vs BS')
plt.title('Monte Carlo vs Black–Scholes Convergence') 
plt.grid(True, which="both", ls="--") 
plt.legend() 
plt.tight_layout() 
plt.savefig('figures/Monte Carlo vs Black–Scholes Convergence.png', dpi=300) 
plt.show() 

# prezzi

plt.figure(figsize=(6,4))
plt.plot(Ns, df_results['Call_MC'], marker='o', label='Call MC')
plt.plot(Ns, df_results['Put_MC'], marker='s', label='Put MC')
plt.axhline(BS_call, color='blue', linestyle='--', label='Call BS')
plt.axhline(BS_put, color='red', linestyle='--', label='Put BS')
plt.xscale('log')
plt.xlabel('Number of simulations N')
plt.ylabel('Price')
plt.title('Monte Carlo price convergence to Black–Scholes')
plt.grid(True, which='both', ls='--')
plt.legend()
plt.tight_layout()
plt.savefig('figures/Monte Carlo price convergence to Black–Scholes.png', dpi=300) 
plt.show()
 
# Istogramma payoff (Call e Put)  

N_hist = 1_000_000
_, X_call_h, _, _, _ = monte_carlo_option(S0, K, T, r, sigma, N_hist, tipo='call', seed=0)
_, X_put_h,  _, _, _ = monte_carlo_option(S0, K, T, r, sigma, N_hist, tipo='put',  seed=0)
plt.figure(figsize=(6,4))
plt.hist(X_call_h, bins=50, alpha=0.7, edgecolor='black', label='Call')
plt.hist(X_put_h,  bins=50, alpha=0.7, edgecolor='black', label='Put')
plt.xlabel('Payoff'); plt.ylabel('Frequenza'); plt.legend(); plt.title('payoff histogram'); plt.grid(True, ls='--'); plt.tight_layout()

plt.savefig('figures/histogram_payoff.png', dpi=300); plt.show()

#Tabella finale

final_table_call = df_results[['N',
    'Call_MC','Call_SE','Call_CI_lower','Call_CI_upper','Call_abs_err','Call_rel_err'
]].copy()

final_table_put = df_results[['N',
    'Put_MC','Put_SE','Put_CI_lower','Put_CI_upper','Put_abs_err','Put_rel_err'
]].copy()

# Arrotonda per leggibilità

final_table_call_rounded = final_table_call.round({
    'Call_MC':6, 'Call_SE':6, 'Call_CI_lower':6, 'Call_CI_upper':6, 'Call_abs_err':6, 'Call_rel_err':6
})

final_table_put_rounded = final_table_put.round({
    'Put_MC':6,  'Put_SE':6,  'Put_CI_lower':6,  'Put_CI_upper':6,  'Put_abs_err':6,  'Put_rel_err':6
})

final_table_call_rounded.to_csv('C:/Users/franc/Documents/project/data/final_table_call_mc_vs_bs.csv', index=False)

final_table_put_rounded.to_csv('C:/Users/franc/Documents/project/data/final_table_put_mc_vs_bs.csv', index=False)

# LaTeX per inserirla nel paper
final_table_call_rounded.rename(columns={
    'N':'N',
    'Call_MC':'Call MC', 'Call_SE':'Call SE', 'Call_CI_lower':'Call CI low', 'Call_CI_upper':'Call CI up',
    'Call_abs_err':'Call |err|', 'Call_rel_err':'Call rel err'
}, inplace=True)

final_table_put_rounded.rename(columns={
    'N':'N',
    'Put_MC':'Put MC', 'Put_SE':'Put SE', 'Put_CI_lower':'Put CI low', 'Put_CI_upper':'Put CI up',
    'Put_abs_err':'Put |err|', 'Put_rel_err':'Put rel err'
}, inplace=True)

with open('C:/Users/franc/Documents/project/paper/tab_call_mc_vs_bs.tex','w', encoding='utf-8') as f:
    f.write(final_table_call_rounded.to_latex(index=False, escape=True))
    
with open('C:/Users/franc/Documents/project/paper/tab_put_mc_vs_bs.tex','w', encoding='utf-8') as f:
    f.write(final_table_put_rounded.to_latex(index=False, escape=True))  
    
    
    