# Pipeline PostgreSQL -> PostgreSQL (Chinook)

Projet: copie des tables de la base **Chinook** (source PostgreSQL) vers une base **target** PostgreSQL,
avec transformation minimale, validation et dashboard Dash pour visualiser le résultat.

## Contenu
- `config/` : configuration (config.json) et mapping (mapping.json)
- `src/` : scripts Python (extracteur, mapping, validation, insertion, dashboard)
- `data/` : CSV extraits depuis la base source (générés par extractor.py)
- `.env.example` : exemple de variables d'environnement (NE PAS COMMITER de vraies credentials)

## Installation
1. Copier `.env.example` en `.env` et compléter les variables.
2. Charger le schéma Chinook dans la base source (voir https://github.com/lerocha/chinook-database).
3. Créer et activer un environnement Python, puis:
   ```bash
   pip install -r requirements.txt
   ```

## Utilisation
1. Extraire les tables depuis la base source vers des CSV:
   ```bash
   python src/extractor.py
   ```
2. Charger les CSV transformés dans la base cible:
   ```bash
   python -m src.main
   ```
3. Lancer le dashboard:
   ```bash
   python src/dashboard.py
   ```

## Remarques et conseils
- Les scripts sont écrits pour être simples et modulaires : vous pouvez ajouter de la transformation ou du nettoyage.
- `config/config.json` liste les tables à copier ; modifiez si nécessaire.
- Ne laissez jamais de vraies credentials dans le dépôt public. Utilisez des secrets GitHub Actions ou un vault pour CI/CD.

## Licence
MIT
