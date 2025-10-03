# UE-AD-A1-REST

## Nos choix techniques

Nous avons mis en place un système d'admin/user dans notre application de manière la plus maintenable et performante que nous pouvions. Ainsi, nous avons donc opté pour le processus suivant :

- Toutes les routes (endpoints) de chaque microservice commencent par `/<user_id>/....`

- Chaque appel (route) vérifie si l’utilisateur est admin en interrogeant le microservice User (`/users/<user_id>/is_admin`).

- On garde un cache en mémoire (un dictionnaire `user_admin_cache`) pour éviter de spammer le service User à chaque requête.

- On stocke le booléen is_admin avec un timestamp.

- Si la donnée est trop vieille (variable `CACHE_TTL` qui vaut 60 secondes), on recharge depuis User.

- Ensuite, nous gérons manuellement dans certains endpoints qui peuvent nécessiter d’être admin (ajout, suppression), sinon nous avons choisi de retourner `403 Forbidden`.


## Lancement des microservices

WARNING : Vous êtes obligé de lancer le microservice `User` tout le temps car il est obligatoire pour la gestion admin/user présente sur chaque endpoint.

### Préalables

Veuillez lancer le projet dans un environnement virtuel avec la commande suivante :

```bash
python3 -m venv venv
```

Puis, vous devez lancer l'environnement virtuel : 

```bash
source venv/bin/activate
```

Enfin, vous devez installer les packages nécessaires depuis le fichier `requirements` : 

```bash
pip install -r requirements.txt
```

### Microservice User

Pour lancer le microservice, il vous suffit de faire les 2 commandes suivantes depuis la racine du projet : 

```bash
cd user
```

```bash
pymon user.py
```

### Microservice Movie

Pour lancer le microservice, il vous suffit de faire les 2 commandes suivantes depuis la racine du projet : 

```bash
cd movie
```

```bash
pymon movie.py
```

### Microservice Schedule

Pour lancer le microservice, il vous suffit de faire les 2 commandes suivantes depuis la racine du projet : 

```bash
cd schedule
```

```bash
pymon schedule.py
```

### Microservice Booking

Pour lancer le microservice, il vous suffit de faire les 2 commandes suivantes depuis la racine du projet : 

```bash
cd booking
```

```bash
pymon booking.py
```


## Lancement de la documentation OpenAPI

Pour trouver la documentation OpenAPI, elle se trouve dans le dossier du microservice cible. Par exemple, pour `Booking`, on retrouve le fichier `booking.yaml`.


## Lancement de tests de l'application sur Insomnia

Vous avez uniquement à importer le fichier `Insomnia.yaml` à la racine du projet dans Insomnia.


# 

BOURREAU Quentin / KOWALSKI Damien - FIL A1