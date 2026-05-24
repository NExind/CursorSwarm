# CursorSwarm v11.0

CursorSwarm v11.0 is a UI modernization release and matches the current Microsoft Store generation before the upcoming v13.12 update.

## Highlights

- Modern CustomTkinter dark Control Panel UI
- Store-approved v10.9 cursor engine behavior preserved
- Floating CS button retained
- Automatic Control Panel launch retained
- Safe Mode, safe quit, and emergency restore support retained
- Documentation, installer script, certification notes, and version metadata refreshed for v11.0

## Safety

Use Quit Safely or the emergency restore helper if cursor visibility needs to be restored.

## Build notes

Recommended PyInstaller command:

```powershell
python -m PyInstaller --onefile --noconsole --name CursorSwarm --icon=cursor_swarm.ico --version-file=packaging/cursor_swarm_version_info_v11_0.txt --collect-data customtkinter src/cursor_swarm_v11_0.py
```
