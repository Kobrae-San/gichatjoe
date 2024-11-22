# gichatjoe

## Description

`gichatjoe` est une application Flask qui télécharge des fichiers PDF depuis Google Drive, extrait le texte de ces PDF et utilise le modèle de langage `llama3.2:1b` via Ollama pour répondre aux questions basées sur le contenu des PDF.

## Prérequis

- Python 3.7 ou supérieur
- Un compte de service Google avec accès à Google Drive
- Ollama installé et configuré

## Installation

1. Clonez le dépôt :

   ```bash
   git clone
   cd gichatjoe
   python app.py

   ouvrir un deuxième cli
   ollama serve
   ollama pull llama3.2:1b
   ```

2. Creation d'un Environnement Virtuel:

   ```bash
   python -m venv env
   source env/bin/activate

   ```

3. Installation des dépendances:

   ```bash
   pip install -r requirements.txt
   ```

## Fonctionnalités

    - Télécharge des fichiers PDF depuis Google Drive.
    - Utilise le modèle de langage llama3.2:1b via Ollama

## Auteur

    - Djédjé Gboble
