# UE-AD-A1-REST

## Nos choix techniques

Nous avons mis en place un système d'admin/user dans notre application de manière la plus maintenable et performante que nous pouvions. Ainsi, nous avons donc opté pour le processus suivant :

- Toutes les routes (endpoints) de chaque microservice commencent par `/<user_id>/....`

- Chaque appel (route) vérifie si l'utilisateur est admin en interrogeant le microservice User `/users/<user_id>/is_admin`).

- On garde un cache en mémoire (un dictionnaire `user_admin_cache`) pour éviter de spammer le service User à chaque requête.

- On stocke le booléen is_admin avec un timestamp.

- Si la donnée est trop vieille (variable `CACHE_TTL` qui vaut 60 secondes), on recharge depuis User.

- Ensuite, nous gérons manuellement dans certains endpoints qui peuvent nécessiter d'être admin (ajout, suppression), sinon nous avons choisi de retourner `403 Forbidden`.

---

## Prérequis

### Pour Docker (Recommandé)

- **Docker** installé et en fonctionnement
- **Docker Compose** (généralement inclus avec Docker Desktop)

### Pour exécution locale (sans Docker)

- **Python 3.10+** installé
- Le fichier `requirements.txt` à jour

> **Important** : Le microservice `User` doit toujours être lancé, car il est utilisé par tous les autres pour la gestion admin/user.

---

## Option 1 : Lancement avec Docker Compose (Recommandé)

### Démarrage rapide

La méthode la plus simple pour lancer l'ensemble de l'architecture :
```bash
docker-compose up -d --build
```

- `--build` : Force la reconstruction des images Docker
- `-d` : Lance les conteneurs en arrière-plan (mode détaché)

### Vérification des services

Pour voir l'état des conteneurs :
```bash
docker-compose ps
```

### Logs des services

Pour consulter les logs de tous les services :
```bash
docker-compose logs -f
```

Pour un service spécifique :
```bash
docker-compose logs -f user
docker-compose logs -f movie
docker-compose logs -f booking
docker-compose logs -f schedule
```

### Arrêt des services

Pour arrêter les services sans supprimer les conteneurs :
```bash
docker-compose stop
```

Pour arrêter et supprimer l'ensemble des conteneurs et réseaux :
```bash
docker-compose down
```

### URLs d'accès (avec Docker Compose)

- **User** : http://localhost:3201
- **Movie** : http://localhost:3200
- **Booking** : http://localhost:3203
- **Schedule** : http://localhost:3202

---

## Option 2 : Lancement local (sans Docker)

Cette option permet d'exécuter les microservices directement sur votre machine, utile pour le développement et le débogage.

### Environnement virtuel Python

Créez d'abord un environnement virtuel Python pour isoler les dépendances :
```bash
# Créer l'environnement virtuel
python3 -m venv venv

# Activer l'environnement virtuel
# Sur macOS/Linux :
source venv/bin/activate

# Sur Windows :
venv\Scripts\activate

# Installer les dépendances pour tous les services
pip install -r requirements.txt
```

**Note :** L'environnement virtuel doit rester activé pendant l'utilisation locale des services. Pour le désactiver :
```bash
deactivate
```

### Lancement des microservices en local

Ouvrez **4 terminaux différents** (un par microservice) et assurez-vous que l'environnement virtuel est activé dans chacun.

**Terminal 1 - User Service :**
```bash
cd user
pymon user.py
```

**Terminal 2 - Movie Service :**
```bash
cd movie
pymon movie.py
```

**Terminal 3 - Schedule Service :**
```bash
cd schedule
pymon schedule.py
```

**Terminal 4 - Booking Service :**
```bash
cd booking
pymon booking.py
```

### URLs d'accès (exécution locale)

- **User** : http://localhost:3201
- **Movie** : http://localhost:3200
- **Booking** : http://localhost:3203
- **Schedule** : http://localhost:3202

---

## Documentation OpenAPI

Les fichiers de spécification OpenAPI (format YAML) se trouvent dans les dossiers respectifs de chaque microservice :

- **User** : `user/user.yaml`
- **Movie** : `movie/movie.yaml`
- **Booking** : `booking/booking.yaml`
- **Schedule** : `schedule/schedule.yaml`

Ces fichiers peuvent être importés dans des outils comme Swagger UI ou Postman pour une documentation interactive.

---

## Tests via Insomnia

Pour faciliter les tests de l'ensemble de l'architecture, nous fournissons un fichier de configuration Insomnia.

### Import du fichier

1. Ouvrez **Insomnia**
2. Cliquez sur **Import/Export** dans le menu
3. Sélectionnez **Import Data**
4. Choisissez le fichier `Insomnia.yaml` à la racine du projet
5. Tous les endpoints seront automatiquement configurés

---

## Dépannage

### Les services ne démarrent pas

Vérifiez que les ports ne sont pas déjà utilisés :
```bash
# Sur macOS/Linux
lsof -i :3200
lsof -i :3201
lsof -i :3202
lsof -i :3203

# Sur Windows
netstat -ano | findstr :3200
netstat -ano | findstr :3201
netstat -ano | findstr :3202
netstat -ano | findstr :3203
```

### Erreurs de communication entre microservices

Assurez-vous que tous les services sont bien démarrés et accessibles. Avec Docker Compose, vérifiez que tous les conteneurs sont sur le même réseau :
```bash
docker network inspect ue-ad-a1-rest_default
```

### Problèmes de cache admin

Si vous rencontrez des problèmes avec le cache admin, redémarrez le microservice User :
```bash
# Avec Docker Compose
docker-compose restart user

# En local
# Arrêtez et relancez user.py dans son terminal
```

---

## Auteurs

**BOURREAU Quentin / KOWALSKI Damien** - FIL A1