# UE-AD-A1-REST

Pour la première partie ne vous souciez pas des fichiers Docker, cela sera abordé par la suite en séance 4.


Toutes les routes commencent par /<user_id>/....

Chaque appel vérifie si l’utilisateur est admin en interrogeant le microservice User (/users/<user_id>/is_admin).

On garde un cache en mémoire (ex: un dictionnaire user_admin_cache) pour éviter de spammer le service User à chaque requête.

On stocke le booléen is_admin avec un timestamp.

Si la donnée est trop vieille (par ex. CACHE_TTL = 60 secondes), on recharge depuis User.

Certains endpoints nécessitent d’être admin (ajout, suppression), sinon retour 403 Forbidden.