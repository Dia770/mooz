## Mooz - API

Mooz est un service permettant de payer de l'essence avec les stations via des services tiers comme Orange Money

## Mise en place du backend

### Installation des dépendances

1. **Python 3.7** - Suivez les instructions pour installer la dernière version de python pour votre plateforme dans la [docs python](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python).

2. **Environnement virtuel**

- Nous vous recommandons de travailler dans un environnement virtuel lorsque vous utilisez Python pour des projets. Cela permet de séparer et d'organiser vos dépendances pour chaque projet. Les instructions pour la mise en place d'un environnement virtuel pour votre plateforme se trouvent dans la [docs python](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).

- Lisez how_to_create_a_virtual_env.txt dans le dossier d'aide pour créer et activer l'environnement virtuel nommé "virtualenv".

3. **Dépendances PIP** - Une fois que votre environnement virtuel est configuré et fonctionne, installez les dépendances requises en exécutant dans ce répertoire :

``bash
pip install -r requirements.txt

``

#### Dépendances Pip clés

- [Flask](http://flask.pocoo.org/) est un framework léger de microservices backend. Flask est nécessaire pour gérer les demandes et les réponses.

- [SQLAlchemy](https://www.sqlalchemy.org/) est la boîte à outils SQL Python et l'ORM que nous utiliserons pour gérer la base de données SQL légère. Vous travaillerez principalement dans `app.py` et pourrez faire référence à `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) est l'extension que nous utiliserons pour gérer les requêtes d'origine croisée de notre serveur frontal.

### Configuration de la base de données

Avec mysql, créez une base de données `tontine_app`. Vous pouvez utiliser un serveur XAMPP, vous pouvez lire [install-mysql-and-phpmyadmin-with-xampp]https://www.jcchouinard.com/install-mysql-and-phpmyadmin-with-xampp/ pour commencer.

### Migration de la base de données

Pour initialiser le fichier de migration, exécutez :

`bash
export FLASK_APP=main.py
flask db init
`

Pour mettre à jour la base de données au dernier état de models.py , exécutez (`export FLASK_APP=main.py` est nécessaire) :

`bash
flask db migrate
flask db upgrade
`

### Exécuter le serveur

Depuis ce répertoire, assurez-vous d'abord que vous travaillez dans l'environnement virtuel que vous avez créé.

Pour exécuter le serveur, exécutez :

```bash
export FLASK_APP=main.py
flask run --reload
```

L'option `--reload` détectera les changements de fichiers et redémarrera le serveur automatiquement.

Le serveur fonctionnera sur `127.0.0.1:5000`.

## Documentation des points de terminaison de l'API

<!-- `POST '/sign-up'``

- Créer un nouvel utilisateur, cet utilisateur represente le service tier.
- Arguments de la requête :

```json
{
  "name": "orange money",
  "password": "orange money"
}
```

- Retourne dans "data" : un jeton qui contient son `user_id:` et qui lui permettra d'utiliser les routes de connexion requises

```json
{
  "code": 200,
  "data": {
    "id": 6,
    "name": "orange money",
    "password": "############"
  },
  "detail": "User created successfully",
  "message": "user_inserted",
  "success": true
}
``` -->

`POST '/login'``

- Se connecter en tant qu'utilisateur
- Arguments de la requête :

```json
{
  "name": "orange money",
  "password": "orange money"
}
```

- Retourne dans "data" : un token qui contient le `user_id:` et qui permettra d'utiliser les routes qui necessitent une authentification

```json
{
  "code": 200,
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiZnk2cWNlemRkaXJzN2RvNyIsImV4cCI6MTY3NTY4ODA1NX0.I340V5pz4L2nlmJJRKmGwpCsB4IBFMZUYHNAW0JFARM"
  },
  "detail": "orange money",
  "message": "user_verified",
  "success": true
}
```

`POST '/generate'``

- Permet au service tier de génerer un ticket à usage unique pour le client qui souhaite acheter de l'essence.
- Arguments de la requête :

```json
{
  "telephone": "+223 80442359",
  "montant": "2000"
}
```

`telephone:` le numéro de telephone du client
`montant:` le montant payé par le client

- Retourne success si l'echange c'est bien passé. Et dans "data" se trouve les informations reçues par le serveur, la date et le code que le client devra utiliser à la station.

```json
{
  "code": 200,
  "data": {
    "code": "3C7076",
    "datetime": "Mon, 06 Feb 2023 20:35:19 GMT",
    "montant": "2000",
    "telephone": "80442359",
    "username": "orange money"
  },
  "detail": "It worked !!",
  "message": "code_created",
  "success": true
}
```

## Tests

Pour déployer les tests, exécutez

``bash
python test_flaskr.py

``
