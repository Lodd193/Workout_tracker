' VBScript to create desktop shortcut for Workout Tracker
Set objShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")

' Get desktop path
desktopPath = objShell.SpecialFolders("Desktop")

' Get Python executable path
pythonPath = objShell.ExpandEnvironmentStrings("%LOCALAPPDATA%") & "\Programs\Python\Python313\python.exe"

' If Python313 doesn't exist, try to find python in PATH
If Not objFSO.FileExists(pythonPath) Then
    pythonPath = "python.exe"
End If

' Project directory
projectPath = "C:\Users\lod19\Desktop\workout_tracker"

' Icon path
iconPath = projectPath & "\workout_tracker.ico"

' Create shortcut
Set shortcut = objShell.CreateShortcut(desktopPath & "\Workout Tracker.lnk")
shortcut.TargetPath = pythonPath
shortcut.Arguments = "-m workout_tracker.main"
shortcut.WorkingDirectory = projectPath
shortcut.Description = "Workout Tracker - Fitness Progress Tracker"
shortcut.IconLocation = iconPath
shortcut.Save

' Show success message
MsgBox "Desktop shortcut created successfully!" & vbCrLf & vbCrLf & "Shortcut: " & desktopPath & "\Workout Tracker.lnk", vbInformation, "Workout Tracker"

' Cleanup
Set shortcut = Nothing
Set objFSO = Nothing
Set objShell = Nothing
