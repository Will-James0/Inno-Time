@echo off
rem Activez l'environnement virtuel
call ..\..\inno\Scripts\activate

rem Vérifier si l'environnement virtuel est activé
if defined VIRTUAL_ENV (
    echo Environnement virtuel activé : %VIRTUAL_ENV%
) else (
    echo Environnement virtuel non activé. Veuillez l'activer avant d'exécuter le script.
    exit /b 1
)

rem installer les bibliothèques

pip install --no-index --find-links=..\..\inno\download_folder -r req.txt

if errorlevel 1 (
    echo Erreur lors de l'exécution de la commande 'install'
    exit /b 1
)


rem Exécuter la commande 'py config.pyc'
py config.pyc

if errorlevel 1 (
    echo Erreur lors de l'exécution de la commande 'py config.pyc'
    exit /b 1
)