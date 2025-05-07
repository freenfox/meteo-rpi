import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO

# Empêche Matplotlib de démarrer une interface graphique
matplotlib.use('Agg')

def plot_data(exp1_data, exp2_data):
    '''takes data in a zipped form'''

    # Extraction des abscisses et des ordonnées (exp1)
    exp1_xs = [xs for xs,_ in exp1_data]
    exp1_ys = [ys for _,ys in exp1_data]

    # Extraction des abscisses et des ordonnées (exp2)
    exp2_xs = [xs for xs,_ in exp2_data]
    exp2_ys = [ys for _,ys in exp2_data]

    # Graphique
    #plt.figure(figsize=(10, 8))
    plt.plot(exp1_xs, exp1_ys, marker=',', color='b', label='Temperature')
    plt.plot(exp2_xs, exp2_ys, marker=',', color='g', label='humiditee')

    # # Limites des axes
    # plt.xlim(-15,135)
    # plt.ylim(8,24)

    # # Graduation des axes
    # plt.xticks(exp1_xs)
    # plt.yticks([i for i in range(8,26,2)])

    # Etiquette des axes
    plt.xlabel("Temps [s]")
    plt.ylabel("Température [°C]")

    # Titre du graphique
    plt.title("Température en fonction du temps")

    # Légende au graphique
    plt.legend()

    # # Cadrillage
    # plt.grid()

    # Rotation des labels de l'axe X pour une meilleure lisibilité
    plt.xticks(rotation=45)

    # Sauvegarde du graphique en mémoire :
    # Crée un buffer en mémoire pour stocker l’image sous forme de flux binaire
    img = BytesIO()

    # Sauvegarde le graphique dans ce buffer en format PNG au lieu de l'afficher.
    plt.savefig(img, format="png")
    
    # Cela ferme la figure et libère la mémoire utilisée par matplotlib
    plt.close()
    
    # Replace le curseur au début du buffer pour pouvoir relire l'image plus tard
    img.seek(0)

    return img