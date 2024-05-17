Set objWMIService = GetObject("winmgmts:\\.\root\cimv2")
Set colProcesses = objWMIService.ExecQuery ("Select * from Win32_Process Where Name = 'python.exe' and CommandLine Like '%manage.py runserver%'")

For Each objProcess in colProcesses
    objProcess.Terminate()
Next
