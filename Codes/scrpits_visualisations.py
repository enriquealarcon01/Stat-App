import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker
def tracer_evolution(df, columns=None, xlabel= None, ylabel= None, start_date=None, end_date=None):
    """
    Trace l'évolution des colonnes spécifiées d'un DataFrame sur une période donnée.

    :param df: DataFrame contenant les données.
    :param columns: Liste des colonnes à tracer.
    :param xlabel: Titre de l'axe des x.
    :param ylabel: Titre de l'axe des y.
    :param start_date: Date de début de la période (optionnel).
    :param end_date: Date de fin de la période (optionnel).
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


    # Définir les couleurs
    colors = plt.cm.get_cmap("tab10", len(columns))

    # Créer la figure
    plt.figure(figsize=(14, 6))

    # Tracer chaque série de données
    for i, country in enumerate(columns):
        plt.plot(df_filtered.index, df_filtered[country], label=country, color=colors(i))

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