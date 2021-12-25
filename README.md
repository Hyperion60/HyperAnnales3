# HyperAnnales3
Fichers source de la dernière version d'HA 3.0

## Liste des fonctionnalités

### Cores
- DEFAULT_AUTO_FIELD (Django 3.2) [FIXED]
- Modification des catégories [FIXED]
- Bulletin d'information [FIXED]
  - Ajout d'un bulletin [FIXED]
  - Modification d'un bulletin [FIXED]
  - Suppression d'un bulletin [FIXED]
  - Ajout d'un media [FIXED]
  - Suppression d'un media [FIXED]
- Ajout d'un fichier [FIXED]
- Refactor fonction git
- Affichages fichiers [BEGIN]
  - Ré-ajouter les classes pour la catégorie [FIXED]
  - Liste les extensions supportées
    - .pdf,.doc,.docx
      - Sendfile
    - .png,.jpg,.jpeg
      - Sendfile + Materialize
    - Code interprété
      - Coloration syntaxique
      - Execution (skulpt)
    - Code compilé
      - Coloration syntaxique
    - Code inerte
      - Coloration syntaxique
  - Jetons d'authentifications [FIXED]
  - Template d'affichage du fichier (polymorphe)
  - Méthodes d'affichage en fonction de l'extension
  - Template d'affichage de la liste de la matière [FIXED]
- Méthode d'affichage de la liste
- Ajout d'un conteneur Nginx pour servir les fichiers statiques
- Etudier l'optimisation par cache
  - Temps de cache
  - Méthode de révocation
- Pages d'erreurs customisées
    - 404
    - 403
    - 498
- Analyse des traffics
  - Compteur des instances (vues)
  - Affichage des informations
  - Exploitation des informations
  - Affinage des paramètrages de fail2ban
- Migrations de la base de données de production
  - Méthode d'élimination des comptes non activée
- Sauvegarde des fichiers statiques
  - Réplication des fichiers
  - Accès local ou distante
- Migration de docker-compose vers Kubernetes

### Utiles
- Moteur de recherche
  - Filtrage
  - Mots-clés
- Interpreteur de code
  - Python
    - Skulpt
- Indexation par les moteurs de recherche
  - sitemap.xml complet (avec le nom des fichiers et mots-clés)
  - robots.txt

### Inutiles
- Ajout de logs dans la page 'À propos'

## Liste des bugs détectés
- Template mobile : Les liens des matières ne sont pas déclarées [FAIT]
- Template mobile : Dépassement dans le breadcrumbs [FAIT]
- Problème de gestion des informations (création, rafraichissment, suppression)
- Affichage du PDF non responsif [FAIT]
- Problème de relation des formulaires d'ajout de fichier (entre l'extension et la couleur)
- Pouvoir modifier un fichier (envoyer un nouveau fichier)

## Liste des améliorations du code

- Transformer le `context['errors']` en liste pour faciliter la gestion des erreurs multiples.
- Ajouter une classe pour la couleur du bouton [FAIT]
- Vérifier la sureté des URL
- Créer une page de mise en garde de sortie du site en cas de redirection URL
- Verifier les droits dans les fonctions post formulaire
- Gestion des erreurs dans les formulaires multiétapes
- Verifier les fonctions de déplacement des objets (place)
- Ajouter `max-length` dans les inputs des formulaires
- Remplacer les labels par des `placeholder`
- Ajouter une fonction pour nettoyer les dépots git en fonction de la base de données
- Ajouter des templates pour les différents codes d'erreurs (404, 403, 500)
- Organiser les variables pour les dépots Git (préfixes d'url d'accès...)
- Merge test template and definitive template
- Nettoyage du git media
- Creer un switch pour les différentes méthodes accès au fichier en fonction
  d'une variable global dans `settings.py`
- Réorganiser les variables global (pour les chemins d'accès notamment)
