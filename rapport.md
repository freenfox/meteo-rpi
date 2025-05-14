Voici ton texte corrigé :

# Rapport de projet d'info

# Meteo\_rpi, par Florent Oppikofer, 3m7

## [Voir sur GitHub.](https://github.com/freenfox/meteo-rpi)

## Installation :

Un système Unix, avec Python3 installé, est requis. Pour utiliser le logger, un Raspberry Pi avec un capteur DHT22 sur le GPIO4 et alimenté en 3,3V est nécessaire. Une LED témoin peut être installée sur le GPIO17.

![Schéma](cirquit.png)

Pour utiliser la fonctionnalité d'IA, Ollama doit être installé, ainsi que Qwen2.5:0.5b.

Il suffit alors de copier le init.sh dans le HOME de l'utilisateur admin, et de l'exécuter. Tout le reste devrait s'installer. Une installation et activation manuelle est aussi possible.

Le témoin LED devrait briller pendant 10s pour indiquer que le logger a bien démarré, puis clignotera pendant 1 seconde à chaque mesure effectuée avec succès.

Le serveur web devrait alors tourner sur le port 80 (celui par défaut de HTTP).

Il est nécessaire de mettre le chemin absolu pour la base de données.

## Mesure et récupération des données :

Les données mesurées (à savoir l'humidité et la température) sont stockées dans une base de données, avec leur timestamp. Cela est effectué toutes les 30 secondes.

La base de données a le schéma suivant :

```sql
CREATE TABLE IF NOT EXISTS mesurments (
Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
temperature REAL NOT NULL,
humidity REAL NOT NULL
);
```

Pour avoir la dernière donnée enregistrée (idéalement la plus actuelle), on fait la requête :

```sql
SELECT temperature, humidity, Timestamp  
FROM measurements  
ORDER BY Timestamp DESC  
LIMIT 1;
```

De la même façon, on peut aussi en récupérer à tout point dans le passé déterminé, par exemple :

```sql
SELECT temperature, humidity, Timestamp  
FROM measurements  
ORDER BY datetime(Timestamp, '-1 hour') DESC  
LIMIT 1;
```

Pour une suite de données sur une période donnée par l'utilisateur, on utilise :

```sql
SELECT temperature, humidity, unixepoch(Timestamp)  
FROM measurements  
WHERE Timestamp >= datetime('now', ?)  
ORDER BY Timestamp DESC
```

avec l'intervalle donné comme paramètre.

## Création du graphique

Étant donné que le temps a été récupéré en millisecondes UNIX, il est facile de mettre cette donnée sur un axe du graphique.

Il est important de noter que la plupart des formes de graphique sont, à l'état actuel, cassées étant donné que je n'ai pas de données continues sur une longue période.

La façon dont il est envoyé : l'utilisateur remplit un formulaire avec ce qu'il veut. Ce formulaire recharge ensuite la même page (index.html), mais avec ces données en paramètres. Ces données sont ensuite mises dans l'URL de l'image, et la route qui fournit l'image les utilise enfin pour faire le graphique.

## Fonctionnalité d'IA

Pour ma touche personnelle, je me suis dit que je pourrais me moquer de toutes ces start-up dont le produit consiste en une chose toute simple et absolument pas nouvelle, ni qui ait besoin d'être améliorée, et la rendre inutilisable en ajoutant une IA mal implémentée, qui a tendance à bien halluciner. J'avais aussi envie de tester les limites du matériel. Une requête est donc faite à un modèle local minimal sur le Raspberry Pi, en utilisant Ollama. La réponse est ensuite mise dans la page.

La raison pour laquelle c'est un iframe est que si j'attendais la réponse pour envoyer la page, cela prendrait bien trop de temps.

## Déploiement

Les services sont démarrés automatiquement à l'aide de fichiers .service (démons). L'état peut être vérifié à l'aide de `systemctl status <nom_du_service>`. Un serveur Gunicorn est utilisé. Une autre possibilité que systemd aurait été de le mettre dans un conteneur Docker que l'on peut juste démarrer. Ce serait l'option que j'aurais préférée, étant donné qu'elle évite de toucher aux fichiers internes de la machine.

## Conclusion
Le project fonctionne, mais le systemd pas. J'aurait prefere utiliser docker pour pouvoir tester le tout a la maison.
