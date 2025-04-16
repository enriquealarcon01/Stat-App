import numpy as np
import pandas as pd
import statsmodels as sm

from statsmodels.tsa.arima.model import ARIMA
from statsmodels.stats.diagnostic import acorr_ljungbox
from scipy import stats #(pour le calcul des fonctions de répartition)

#Remarque: ce code s'inspire très largement de ce qu'a été vu dans le TD4 de séries temporelles
def arimafit(p,q, data, max_lag=15):
    print(f"\n ARIMA({p},0,{q})")
    try:
        #Etape 1: estimation du modèle 
        model=ARIMA(data,order=(p,0,q))
        fit=model.fit()

        coef=fit.params
        std_errors=fit.bse
        t_stats=coef/std_errors
        p_values=2*(1-stats.norm.cdf(np.abs(t_stats)))

        #Résumé
        summary_table=pd.DataFrame({
           'Coef': coef,
           'Std Err': std_errors, 
           't-stat': t_stats,
           'p-value':p_values          
        })

        print("\n Coefficients estimés et p-valeurs")
        print(summary_table.round(4))

        #Etape 2: Tests des résidus
        ljung = acorr_ljungbox(fit.resid, lags=range(1, max_lag + 1), return_df=True)
        print(f"\n Test de Ljung-Box (autocorrélation des résidus jusqu'à {max_lag} lags) : ")
        print(ljung.round(4))

        return {
            'fit': fit,
            'coef_summary': summary_table,
            'ljung_box': ljung
        }
    except Exception as e:
        print(f" Problème pour ARIMA({p},0,{q}): {e}")
        return None
