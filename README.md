# INF6405 - TP2: Méthodes Heuristiques


## Structure du Projet

```
TP2/
├── data/                  # Fichiers de données JSON
├── RecuitSimule/          # Code pour Glouton et Recuit Simulé
├── Genetique/             # Code pour l'Algorithme Génétique
├── Tabu/                  # Code pour la Recherche Taboue
├── results/               # (Créé automatiquement) Contient les fichiers CSV de résultats
├── run_experiments.py     # Script principal pour lancer toutes les simulations
├── analyze_results.ipynb  # Notebook Jupyter pour l'analyse et la visualisation
├── requirements.txt       # Dépendances Python
└── README.md              # Ce fichier
```

## Instructions d'Installation et d'Exécution

L'environnement de test est Linux Fedora Workstation 42 avec Python 3.11.9

### 1. Prérequis

- Python 3.11 ou plus récent
- `pip` (le gestionnaire de paquets Python)

### 2. Création d'un Environnement Virtuel


Cloner le projets et créer un environnement virtuel
```bash
# Créez un environnement virtuel nommé 'venv'
python3 -m venv venv

# Activez l'environnement virtuel
source venv/bin/activate
```

### 3. Installation des Dépendances


```bash
pip install -r requirements.txt
```

### 4. Exécution des Expériences

Le script `run_experiments.py` automatise l'exécution de toutes les simulations et sauvegarde les résultats dans des fichiers CSV dans le dossier `results/`.

```bash
# Pour lancer toutes les expériences de toutes les sections
python run_experiments.py --section all

# Pour ne lancer que les expériences d'une section spécifique (ex: 4.1)
python run_experiments.py --section 4.1

# Pour ne lancer qu'une sous-section (ex: 4.2.3)
python run_experiments.py --section 4.2.3
```

Les sections disponibles sont : `4.1`, `4.1.1`, `4.1.2`, `4.2`, `4.2.1`, `4.2.2`, `4.2.3`, `4.3`, `4.3.1`, `4.3.2`, et `all`.

Le script affichera la progression dans la console et indiquera quand chaque fichier CSV est sauvegardé.

### 5. Graphiques

Les graphiques pour le rapport du TP2 peuvent être générés dans le notebook Jupyter `analyze_results.ipynb`.