Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = "C:\Users\sai rithvik\.gemini\antigravity\scratch\unifolio"
WshShell.Run "powershell.exe -ExecutionPolicy Bypass -WindowStyle Hidden -File ""C:\Users\sai rithvik\.gemini\antigravity\scratch\unifolio\run_persistent.ps1""", 0, True
WScript.Sleep 1000
WshShell.Run "http://127.0.0.1:5000", 1, False
