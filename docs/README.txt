CursorSwarm v13.12
===================

CursorSwarm is a Windows cursor effects app for fake cursors, mirror movement, transparent cursor modes, Cursor Lab customization, animated cursor shapes, idle/movement/click effects, presets, and full visual themes.

WHAT IS NEW IN v13.12
---------------------
CursorSwarm v13.12 is a final polish and release-prep checkpoint for the current v13 feature set. It updates version labels, generated documentation, release notes, build references, safety/recovery notes, and Microsoft Store packaging notes while keeping the implemented feature set stable.

CURRENT FEATURE SET
-------------------
Core controls and safety:
- CustomTkinter Control Panel with fixed two-row main tab layout.
- Floating CS button to reopen the Control Panel.
- Ctrl + Alt + C to toggle the Control Panel.
- Ctrl + Alt + Space for Safe Mode / Resume Previous Mode.
- Ctrl + Alt + Q to Quit Safely and restore the Windows cursor.
- Ctrl + Alt + R to toggle the real Windows cursor visible/transparent.
- Emergency restore helper script/exe support.
- Run Stability Check for cursor restore, JSON/settings health, themes, and custom colour preset status.

Cursor Lab:
- Custom image cursor support.
- Manual Cursor Shape Library: Captured System Cursor, Arrow, Hand, I-Beam, Crosshair, resize cursors, Working in Background, Busy / Loading, and Custom Image File.
- Reliable generated fallback I-Beam and Crosshair shapes.
- Real Windows ANI support for Busy / Loading and Working in Background when available.
- Generated fallback spinner support when real ANI files are unavailable.
- Animation source status, real-ANI toggle, and Slow/Normal/Fast animation speed.
- Cursor tint, bright neon tint, single-colour tint, multi-colour neon tint, custom multi-colour presets, black outline, drawn cursor resize, fake cursor size multiplier, and manual hotspot/offset controls.
- Native dialog safety so file/color picker dialogs temporarily restore the normal Windows cursor.

Idle effects:
- Pulse, Glow Ring, Fade, and Wobble idle styles.
- Idle delay and strength controls.
- Neon glow presets and custom neon colours.
- Optional pause of idle effects after long idle.

Movement and click effects:
- Checkbox-stackable movement effects: Motion Trail, Speed Glow, Motion Streak, Spark Particles, Ripple Burst, Comet Tail, Speed Lines, and Magnetic Orbit.
- Per-effect controls and colour modes for supported effects: Cursor Lab Colors, Custom Color, Single Colour Preset, and Multi-Colour Neon Preset.
- Click Effects with left/right click support: Ripple, Burst Ring, Sparks, and Ripple + Sparks.
- Shift + mouse wheel horizontal scrolling in dense Movement/Cursor Lab sections.

Presets, themes, and startup:
- Built-in swarm presets and custom swarm presets.
- Full Cursor Themes with 10 theme slots.
- Save, load, rename, delete/reset, export, import, and reset theme actions.
- Custom Multi-Colour Presets with 10 slots, 3 editable colours, enable/show toggle, import/export/reset, and shared dropdown integration.
- Startup behavior: Fresh Safe Defaults, Last Used Settings, Built-in Preset, Custom Preset, or Selected Theme.
- Full backup support for presets, settings, themes, and custom multi-colour presets.

Performance and stability:
- Target overlay FPS.
- Performance presets.
- Battery Saver Glow Mode.
- Hide Fake Cursors After Long Idle.
- Pause Idle Effects After Long Idle.
- Safer JSON saving/loading with backup handling for broken settings/preset/theme files.

IMPORTANT SAFETY NOTE
---------------------
CursorSwarm can hide the real Windows cursor and intentionally make cursor movement visually confusing. Always keep the recovery controls in mind.

Recovery controls:
Ctrl + Alt + C      = Open / close Control Panel
Floating CS button  = Reopen or focus Control Panel
Ctrl + Alt + Space  = Safe Mode / Resume Previous Mode
Ctrl + Alt + Q      = Quit Safely and restore cursor
Ctrl + Alt + R      = Toggle real system cursor visible / transparent
Hold Shift          = Temporary cursor hint / normal movement in some modes

If your cursor is still hidden after closing the app, run restore_cursor_emergency.exe or restore_cursor_emergency.py.

DEVELOPER BUILD NOTE
--------------------
Required packages:
pip install customtkinter pillow

Example PyInstaller command:
pyinstaller --onefile --noconsole --icon=cursor_swarm.ico --version-file=cursor_swarm_version_info_v13_12.txt --collect-data customtkinter cursor_swarm_v13_12.py

PACKAGING / STORE NOTES
-----------------------
Recommended app description:
CursorSwarm is a local Windows desktop cursor effects app with fake cursor swarms, mirror movement, custom cursor visuals, animated cursor shapes, idle/movement/click effects, presets, themes, startup modes, and safety recovery controls.

MSIX installer arguments:
No special installer arguments are required for the packaged executable unless the packaging tool specifically requires them. CursorSwarm stores writable local settings in a safe app-data folder when installed in a read-only package location.

Microsoft Store runFullTrust explanation:
CursorSwarm is a packaged Win32/Python desktop application. It requires the runFullTrust capability to run its local desktop process, display transparent/topmost cursor overlays, read local mouse state for visual effects, register global hotkeys, use Windows cursor APIs for hide/restore behavior, and provide emergency recovery controls. CursorSwarm does not collect, upload, sell, or share personal data.
