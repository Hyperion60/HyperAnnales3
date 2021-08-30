# HyperAnnales3
Sources files from the last version of HA 3.0

## Liste des fonctionnalités

### Cores
- DEFAULT_AUTO_FIELD (Django 3.2) [FIXED]
- Ajout d'un fichier
- Affichages fichiers
  - Ré-ajouter les classes pour la categorie
  - Jetons d'authentifications
  - Template d'affichage du fichier (polymorphe)
  - Méthodes d'affichage en fonction de l'extension
  - Template d'affichage de la liste de la matière
- Méthode d'affichage de la liste
- Etudier l'optimisation par cache
  - Temps de cache
  - Méthode de révocation
- Analyse des traffics
  - Affichage des informations
  - Exploitation des informations
  - Affinage des paramètrages de fail2ban
- Migrations de la base de données de production
  - Méthode d'élimination des comptes non-activé
- Sauvegarde des fichiers statiques
  - Réplication des fichiers
  - Accès local ou distante
- Migration de docker-compose vers Kubernetes

### Utiles
- Moteur de recherche
  - Filtrage
  - Mots-clés

### Inutiles

## Liste des bugs détectés

## Liste des améliorations du code

- Transformer le `context['error']` en liste pour faciliter la gestion des erreurs multiples.
- Ajouter une classe pour la couleur du bouton
- Vérifier la sureté des URL