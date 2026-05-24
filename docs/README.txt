CursorSwarm v11.0
==================

CursorSwarm is a Windows cursor effects app for fake cursors, mirror movement, transparent cursor modes, presets, and visual cursor camouflage.

It is made for fun, experimentation, and user-controlled visual cursor effects.

--------------------------------------------------
WHAT IS NEW IN v11.0
--------------------------------------------------

CursorSwarm v11.0 modernizes the Control Panel with a CustomTkinter dark UI while keeping the Store-approved cursor engine unchanged.

The cursor overlay, fake cursor drawing, raw input mirror movement, global hotkeys, floating CS button, Safe Mode, safe quit, and emergency restore behavior remain based on the stable v10.9 core.

The external README and release documents have also been updated to v11.0 so they no longer carry old v10.8 text.

--------------------------------------------------
IMPORTANT SAFETY NOTE
--------------------------------------------------

CursorSwarm can hide your real system cursor and make your mouse movement intentionally confusing.

Use stronger modes carefully. Do not use CursorSwarm while doing important work, payments, exams, accessibility-dependent tasks, system configuration tasks, or anything where losing track of your cursor could cause problems.

Before using stronger modes, remember these recovery controls:

Ctrl + Alt + C      = Open / close Control Panel
Floating CS button  = Reopen or focus Control Panel
Ctrl + Alt + Space  = Safe Mode / Resume Previous Mode
Ctrl + Alt + Q      = Quit Safely and restore cursor
Ctrl + Alt + R      = Toggle real system cursor visible / transparent
Hold Shift          = Temporary cursor hint / normal movement in some modes

CursorSwarm v11.0 opens the Control Panel automatically when launched so the main app controls are visible.

A small floating CS control button stays on screen when the Control Panel is hidden. Click it to reopen or focus the Control Panel. You can also drag it to another position.

If the Control Panel is hidden, a temporary on-screen hint shows the shortcut to reopen it.

If your cursor ever gets stuck hidden after the app is closed, run:

restore_cursor_emergency.exe

No Python installation is required for the emergency restore EXE.

A fallback developer script may also be created as restore_cursor_emergency.py.

--------------------------------------------------
PRIVACY SUMMARY
--------------------------------------------------

CursorSwarm does not collect, upload, sell, rent, or share personal data.

CursorSwarm stores settings and presets locally on your device only.

The app does not require an account, server connection, analytics, telemetry, ads, or cloud syncing.

For the full privacy policy, see:

CursorSwarm_PrivacyPolicy.txt

--------------------------------------------------
TERMS AND SAFETY NOTICE
--------------------------------------------------

CursorSwarm is provided as an experimental cursor effects app.

By using CursorSwarm, you understand that it can make the cursor difficult to see or control, especially in Nightmare and Mirror modes.

Use Safe Mode, Quit Safely, the floating CS button, keyboard shortcuts, and the standalone emergency restore EXE if needed.

For the full terms and safety notice, see:

CursorSwarm_TermsAndSafety.txt

--------------------------------------------------
FILES
--------------------------------------------------

CursorSwarm may create or use these support files:

cursor_presets.json
    Stores your custom preset slots.

cursor_settings.json
    Stores startup mode, HUD visibility, and last-used state.

restore_cursor_emergency.exe
    Standalone emergency cursor restore helper included with installer/MSIX builds.

restore_cursor_emergency.py
    Fallback emergency cursor restore script created by the app for development/manual recovery.

README.txt
    Basic usage, safety, recovery, and troubleshooting information.

CursorSwarm_PrivacyPolicy.txt
    Privacy policy for release/distribution.

CursorSwarm_TermsAndSafety.txt
    Terms, safety notice, and user responsibility information.

CursorSwarm_ReleaseNotes.txt
    Current release notes.

In normal portable EXE mode, these files may be created beside CursorSwarm.exe.

In MSIX / Microsoft Store mode, Windows installs the app in a protected package folder, so CursorSwarm stores writable support files in:

%LOCALAPPDATA%\CursorSwarm

--------------------------------------------------
BASIC HOTKEYS
--------------------------------------------------

Ctrl + Alt + C
    Show / hide the Control Panel.

Ctrl + Alt + Space
    Toggle Safe Mode / Resume Previous Mode.

Ctrl + Alt + Q
    Quit safely and restore your system cursor.

Ctrl + Alt + R
    Toggle real system cursor visible / transparent.

Ctrl + Alt + M
    Toggle Mirror Mode.

Ctrl + Alt + X
    Toggle Mirror X direction.

Ctrl + Alt + Y
    Toggle Mirror Y direction.

Ctrl + Alt + P
    Pause / resume fake cursor swarm.

Ctrl + Alt + H
    Hide / show drawn-real cursor.

Ctrl + Alt + D
    Toggle Runtime HUD.

Hold Shift
    Temporary safety hint / normal movement behavior depending on mode.

--------------------------------------------------
CONTROL PANEL AND FLOATING BUTTON
--------------------------------------------------

CursorSwarm opens the Control Panel automatically when launched.

v11.0 uses a modern CustomTkinter dark Control Panel with tabbed sections, card-style controls, clearer action buttons, and better Store-screenshot appearance.

You can open or hide the panel anytime with:

Ctrl + Alt + C

If the panel is hidden, CursorSwarm briefly displays a reminder showing this shortcut.

The floating CS button is a small draggable on-screen control. Click it to reopen or focus the Control Panel. Right-click it to open the Control Panel or hide the floating button for the current session.

Main tabs:

Dashboard
    Quick controls and important safety buttons.

Cursor
    System cursor visibility, drawn-real cursor, cursor scale, manual offset, and Nightmare modes.

Mirror
    Raw input mirror movement controls.

Swarm
    Fake cursor counts, density presets, movement threshold, wobble/randomness, and draw order.

Presets
    Built-in presets and 10 custom preset slots.

Safety
    Startup mode, emergency restore, and recovery options.

Advanced
    Debug/status information, import/export backup tools, app info, and release document helpers.

--------------------------------------------------
RECOMMENDED FIRST TEST
--------------------------------------------------

Before using strong modes, test these:

1. Open app.
2. Confirm the Control Panel appears automatically.
3. Confirm the new CustomTkinter UI is visible.
4. Confirm the floating CS button is visible when the Control Panel is hidden.
5. Press Ctrl + Alt + C to hide/show the Control Panel.
6. Confirm the shortcut hint appears briefly after hiding the panel.
7. Click the floating CS button to reopen the Control Panel.
8. Press Ctrl + Alt + Space for Safe Mode.
9. Press Ctrl + Alt + Q to quit safely.

Make sure the cursor restores normally.

--------------------------------------------------
TROUBLESHOOTING
--------------------------------------------------

If the cursor is hidden:
    Press Ctrl + Alt + R or Ctrl + Alt + Q.

If movement is confusing:
    Press Ctrl + Alt + Space for Safe Mode.

If the Control Panel is hidden:
    Press Ctrl + Alt + C or click the floating CS button.

If the floating CS button was hidden:
    Press Ctrl + Alt + C to open the Control Panel.

If the app is closed but the cursor is still hidden:
    Run restore_cursor_emergency.exe.

If config files are broken:
    Delete cursor_settings.json and restart the app.
    The app will recreate it.

If presets are broken:
    Use Reset All Custom Presets from the app,
    or delete cursor_presets.json and restart.

--------------------------------------------------
DEVELOPER BUILD NOTE
--------------------------------------------------

CursorSwarm v11.0 uses CustomTkinter for the Control Panel UI.

Install the dependency before running/building from source:

pip install customtkinter pillow

For PyInstaller builds, include CustomTkinter package data, for example:

pyinstaller --onefile --noconsole --icon=cursor_swarm.ico --version-file=cursor_swarm_version_info_v11_0.txt --collect-data customtkinter cursor_swarm_v11_0.py

--------------------------------------------------
VERSION
--------------------------------------------------

CursorSwarm v11.0

v10.7
    Release-readiness polish, privacy policy, terms/safety notice, and final pre-publishing documents.

v10.8
    Certification fix and recovery polish: visible Control Panel on launch, temporary shortcut hint, Store-friendly Start Menu packaging, and standalone emergency restore EXE support.

v10.9
    Added a draggable floating CS control button so users can reopen or focus the Control Panel without relying only on a keyboard shortcut.

v11.0
    Modernized the Control Panel with CustomTkinter while keeping the cursor engine, floating CS button, hotkeys, Safe Mode, and emergency recovery behavior unchanged. Updated the external README and release documents to v11.0.

Copyright (C) 2026 Palugula Tharun Kumar.
