' Créer un objet WshShell
Set WshShell = CreateObject("WScript.Shell")

' Lancer l'installation de Python
WshShell.Popup "L'installation de Python va commencer. Veuillez patienter...", 5, "Installation de Python", vbInformation

WshShell.Run "cmd /c cd app && python-3-11-2.exe /quiet InstallAllUsers=1 PrependPath=1", 0, True

' Attendre que le processus Python se termine
Do
    WScript.Sleep(100)
Loop Until WshShell.AppActivate("Installation de Python") = False

WshShell.Popup "L'installation de Python est terminée !", 5, "Installation de Python", vbInformation

' Lancer l'installation de PostgreSQL
WshShell.Popup "L'installation de PostgreSQL va commencer. Veuillez patienter...", 5, "Installation de PostgreSQL", vbInformation

WshShell.Run "cmd /c cd app && start /wait /min postgresql.exe --optionfile config.txt", 0, True

WshShell.Popup "L'installation de PostgreSQL est terminée !", 5, "Installation de PostgreSQL", vbInformation

' Lancer le programme de configuration
WshShell.Run "cmd /c ..\..\config.exe", 0, False

' Libérer l'objet WshShell
Set WshShell = Nothing
