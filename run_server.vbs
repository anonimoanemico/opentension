Set wshShell = WScript.CreateObject("WScript.Shell")
wshShell.CurrentDirectory = "flask"
cmd = "python flaskr.py"
wshShell.Run cmd