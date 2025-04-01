import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker
import numpy as np 
import pandas as pd
from scipy.signal import savgol_filter
def tracer_evolution(df, columns=None, xlabel= None, ylabel=None, start_date=None, end_date=None, log=False, base=None, lissage=False):
    """
    Trace l'évolution des colonnes spécifiées d'un DataFrame sur une période donnée.

    :param df: DataFrame contenant les données.
    :param columns: Liste des colonnes à tracer.
    :param xlabel: Titre de l'axe des x.
    :param ylabel: Titre de l'axe des y.
    :param start_date: Date de début de la période (optionnel).
    :param end_date: Date de fin de la période (optionnel).
    :param log: valeur logarithmique (optionel).
    :param base: indice de base (optionel).
    :param lissage: lissage des courbes selon le lissage de Savitzky-Golay (optionel). 
    """
    # Filtrer les données par période si des dates sont spécifiées
    if start_date and end_date:
        date = (df.index >= start_date) & (df.index <= end_date)
        df_filtered = df.loc[date]
    else:
        df_filtered = df

    # Sélectionner uniquement les colonnes spécifiées
    if columns:
        df_filtered = df_filtered[columns]
    else :
        columns = df_filtered.columns

    # Trier les individus par valeur moyenne décroissante sur la période
    mean_values = df_filtered.mean().sort_values(ascending=False)
    sorted_columns = mean_values.index

    # Réorganiser le DataFrame selon cet ordre
    df_filtered = df_filtered[sorted_columns]

    if log:
        df_filtered = df_filtered.applymap(lambda x: np.log(x) if x > 0 else np.nan)
    
    if base:
        df_filtered = df_filtered / df.loc[base]-1

    if lissage:
        for col in df_filtered.columns:
            df_filtered[col] = savgol_filter(df_filtered[col], window_length=10, polyorder=3)


    # Liste de couleurs personnalisées
    custom_colors = [
    'yellow', 'blue', 'red', 'green', 'orange', 'pink', 'purple', 'cyan', 'brown', 'lime',
    'magenta', 'indigo', 'violet', 'teal', 'navy', 'olive', 'maroon', 'gray', 'gold', 'turquoise',
    'aqua', 'fuchsia', 'darkgreen', 'darkorange', 'darkblue', 'crimson', 'lightcoral', 'khaki', 'slateblue', 'deepskyblue'
]

    # Répéter les couleurs si nécessaire
    colors = [custom_colors[i % len(custom_colors)] for i in range(len(sorted_columns))]

    # Créer la figure
    plt.figure(figsize=(14, 6))

    # Tracer chaque série de données
    for i, country in enumerate(sorted_columns):
        plt.plot(df_filtered.index, df_filtered[country], label=country, color=colors[i])

    # Personnalisation du graphique
    if xlabel :
        plt.xlabel(xlabel)
    if ylabel :
        plt.ylabel(ylabel)

    # Indicage
    num_ticks = 8
    indices = np.linspace(0, len(df_filtered.index) - 1, num_ticks, dtype=int)
    plt.xticks(df_filtered.index[indices], rotation=45)

    # Affichage
    plt.legend(loc="upper left", bbox_to_anchor=(1, 1), ncol=2)  # Légende en dehors du graphique
    plt.grid(True)
    plt.gca().yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:,.0f}"))  # Éviter l'écriture scientifique
    plt.tight_layout()
    plt.show()

def camembert(df, période, variables=None, titre=None):
    """
    Crée un diagramme camembert montrant la répartition des valeurs d'une liste de variables à une certaine période.
    
    Args:
        df (DataFrame): Le DataFrame contenant les données.
        période (str/int): La période (index du DataFrame) pour laquelle générer le camembert.
        variables (list, optional): Liste des variables à inclure. Si None, toutes les colonnes sont utilisées.
        titre (str, optional): Titre du graphique.
    """
    plt.close('all')
    
    # Sélection des variables
    if variables is None:
        variables = df.columns
    
    # Extraction des valeurs pour la période donnée sort les valeurs nulles
    data = df.loc[période, variables]
    data = data.dropna()

    # Trier les valeurs par ordre croissant
    data = data.sort_values(ascending = False)
    
    # Création du camembert
    plt.figure(figsize=(10, 6))
    wedges, texts, autotexts = plt.pie(data, labels=None, autopct='%1.1f%%',
                                       pctdistance=1.2, explode=[0.05] * len(data))
    
    # Apparence du camembert
    plt.setp(autotexts, size=10, weight='bold')
    
    # Positionner correctement les noms des pays
    for text in texts:
        text.set_fontsize(10)
    
    # Ajuster la légende pour être plus à droite
    plt.legend(wedges, [f"{index} ({val:,})" for index, val in data.items()],
               title=titre, loc="center left", bbox_to_anchor=(1.2, 0.5))
    
    plt.axis('equal')
    plt.gca().set_axis_off()
    plt.tight_layout()
    plt.show()

def comparer_periodes(df, periode_1, periode_2, percent = True):
    """
    Compare les valeurs de chaque variable entre deux périodes spécifiques dans un DataFrame.
    
    :param df: DataFrame avec les périodes comme index et les variables comme colonnes.
    :param periode_1: Première période à comparer 
    :param periode_2: Deuxième période à comparer 
    
    :return: DataFrame contenant les résultats de la comparaison.
    """
        
    # Extraire les données pour chaque période
    data_periode_1 = df.loc[periode_1]
    data_periode_2 = df.loc[periode_2]
    
    # Calculer la différence entre les deux périodes (tu peux aussi faire d'autres comparaisons)
    if percent :
        comparaison = (data_periode_2 - data_periode_1)/data_periode_1*100
    else:
        comparaison = data_periode_2 - data_periode_1
    
    # Créer un nouveau DataFrame avec les résultats de la comparaison
    comparaison_df = pd.DataFrame({
        'Période 1': data_periode_1,
        'Période 2': data_periode_2,
        'Différence de %': comparaison
    })
    
    return comparaison_df