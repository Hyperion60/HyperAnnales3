# HyperAnnales3
Sources files from the last version of HA 3.0

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
- Affichages fichiers [BEGIN]
  - Ré-ajouter les classes pour la categorie [FIXED]
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
  - Jetons d'authentifications
  - Template d'affichage du fichier (polymorphe)
  - Méthodes d'affichage en fonction de l'extension
  - Template d'affichage de la liste de la matière [FIXED]
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
- Interpreteur de code
  - Python
    - Skulpt

### Inutiles

## Liste des bugs détectés
- Template mobile : Les liens des matières ne sont pas déclarées [FAIT]

## Liste des améliorations du code

- Transformer le `context['errors']` en liste pour faciliter la gestion des erreurs multiples.
- Ajouter une classe pour la couleur du bouton [FAIT]
- Vérifier la sureté des URL
- Verifier les droits dans les fonctions post formulaire
- Gestion des erreurs dans les formulaires multi-étapes
- Verifier les fonctions de déplacement des objets (place)
- Ajouter `max-length` dans les inputs des formulaires
- Remplacer les labels par des `placeholder`
- Ajouter une fonction pour nettoyer les dépots git en fonction de la base de données
- Ajouter des templates pour les différents codes d'erreurs (404, 403, 500)
- Organiser les variables pour les dépots Git (préfixes d'url d'accès...)
- Merge test template and definitive template
- Nettoyage du git media
