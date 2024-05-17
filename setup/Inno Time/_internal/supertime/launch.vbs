Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "cmd /c py manage.py runserver 0.0.0.0:8000", 0
