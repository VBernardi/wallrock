<img src="wallrock.png" width="100" style="margin-left:50%"/>

## WallRock 

WallRock est une application bureau pour trier et changer ces fonds d'écran d'ordinateur

## OS Vérifiés ✅ ❌

> Windows 
> - 10 ?
>
> Mac OS 
> - Sonoma 14.4.1 ✅
> 
> Linux 
> - Ubuntu ?

## Utilisation

### Lancement de l'application
Cliquer deux fois sur le fichier **2** dans le dossier **dist**

Une fois l'application lancée, choisissez le dossier dans le lequel vous avez téléchargé ce projet 
<!-- images pour expliciter la chose -->

### Fonctionnalités

- Parcourir les dossiers
- Revenir dans le dossier précédent en cliquant sur la flèche
- Glisser une image dans un dossier pour déplacer l'image dans le dossier en question
- Glisser une image sur la fleche pour déplacer l'image dans le dossier précédent
- Ajouter une image au dossier en cours

### Fonctionnalités futur
- Changer le fond d'écran (mdr)
- Créer un dossier
- Supprimer une image

## Accès au code (pour développeur)
### Installation
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 wallrock.py
```
### Créer un nouveau fichier exécutable
Dans l'environnement virtuel faire:
```
pyinstaller --onefile wallrock.py
```