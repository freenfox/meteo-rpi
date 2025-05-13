# Rapport de project d'info

# Meteo_rpi, par Florent Oppikofer, 3m7
[Voir sur github.](https://github.com/freenfox/meteo-rpi)
---




## Instalation:
Un systeme unix, avec python3 installe est requis. Pour utiliser le logger, un rasberry py avec un capteur dht22 sur le GPIO3 et alimante en 3,3v est nesessaire. Une LED temoin peut etre installee sur le GPIO4.

Pour utiliser la fonctionalite d'IA, ollama doit etre installe, anci que qwen2.5:0.5b.

Il suffi alors de copier le init.sh au HOME de l'utilisateur admin, et de l'executer, et tout le reste devrait s'installer. Une installation et activation manuelle est aussi possible.

Le temoin LED devrait briller pendent 10s pour indiquer que le logger a bien demmarre, pui cligniotera pour 1 seconde a chaque mesure effectuee avec succes.

Le serveur web devrait alors tourner sur le port 80 (celui par defaut de http).

Il est nesessaire de mettre le chemain absolut pour la base de donnee.

## Mesure et recuperation des donnees:
Les donnees mesurees (a savoire l'humidite et la temperature) sont stoquees dans une base de donee, avec leurs Timestamp. Cela est effectue toutes les 30 secondes. 

Pour avoir la derniere donnee enrejistree (dans l'ideale l'actuelle), on fait la requete:
```sql
SELECT temperature, humidity, Timestamp
FROM mesurments
ORDER BY Timestamp DESC
LIMIT 1;
```

De la meme facon on peut aussi en recuperer a tout point dans le passe determine, p.ex. :
```sql
SELECT temperature, humidity, Timestamp
FROM mesurments
ORDER BY datetime(Timestamp, '-1 hour') DESC
LIMIT 1;
```

Pour une suite de donees sur une periode donnee par l'utilisateur, on utilise
```sql
SELECT temperature, humidity, unixepoch(Timestamp)
FROM mesurments
WHERE Timestamp >= datetime('now', ?)
ORDER BY Timestamp DESC
```

avec l'interval donnee comme parametre.

## Creation du graph

Etent donne que le temps a ete recupere en milisecondes UNIX, il est facile de mettre cette donnee sur un axe du graphique.

Il est importent de noter que la pluspart des formes de graphique sont en l'etat actuelle casse etent donne que je n'ai pas des donnees continues sur une longue periode.

La facon dont il est envoye: l'utilisateur rempli un form avec ce qu'il veut. Ce form recharge ensuite la meme page (index.html), mais avec ces donnees en parametres. ces donnees sont ensuite mise dans l'url de l'image, et la route qui fourni l'image les utilise enfin et fait le graphique.

## Fonctionalite d'IA
Pour ma touche personelle, je me suis dit que je pourrais me moquer de toutes ces start up dont le produit consite en une chose toute simple et absolument pas nouvelle, ni qui ai besoin d'etre ameilloree, et la rend inutilisable en ajoutent une IA mal implementee, et qui a tendence a bien haluciner. J'avais aussi envie de tester les limites du materielle. Une requete est donc fait a un model local minimal sur le rasberrypi, en utilisent ollama. La reponse est ensuite mise dans la page. 

La raison que ce soit un iframe est que si j'attendais la reponse pour envoyer la page, cela prendrait bien trop de temps.

## Deploiment
Les services sont demare automatiquement a l'aide de fichirs .service (deamons). L'etat peut etre verifie a l'aide de `systemctl status <nom_du_service>`. Un serveur gunicorn est utilise. Une autre possibilite que systemd aurait ete de le mettre dans un conteneur docker que l'on peut juste demarre. Ce serait l'option que j'aurait prefere, etent donne qu'elle evite de toucher aux fichiers internes de la machine.