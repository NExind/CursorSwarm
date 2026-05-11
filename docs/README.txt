CursorSwarm v10.8
==================

CursorSwarm is a Windows cursor effects app for fake cursors, mirror movement, transparent cursor modes, presets, and visual cursor camouflage.

It is made for fun, experimentation, and user-controlled visual cursor effects.

--------------------------------------------------
IMPORTANT SAFETY NOTE
--------------------------------------------------

CursorSwarm can hide your real system cursor and make your mouse movement intentionally confusing.

Use stronger modes carefully. Do not use CursorSwarm while doing important work, payments, exams, accessibility-dependent tasks, or anything where losing track of your cursor could cause problems.

Before using stronger modes, remember these recovery controls:

Ctrl + Alt + C      = Open / close Control Panel
Ctrl + Alt + Space  = Safe Mode / Resume Previous Mode
Ctrl + Alt + Q      = Quit Safely and restore cursor
Hold Shift          = Temporary cursor hint / normal movement in some modes

CursorSwarm v10.8 opens the Control Panel automatically when launched so the main app controls are visible.

If the Control Panel is hidden, a temporary on-screen hint shows the shortcut to reopen it.

If your cursor ever gets stuck hidden after the app is closed, run:

restore_cursor_emergency.exe

No Python installation is required for the emergency restore EXE.

A fallback developer script may also be created as restore_cursor_emergency.py.

--------------------------------------------------
PRIVACY SUMMARY
--------------------------------------------------

CursorSwarm does not collect, upload, sell, or share personal data.

CursorSwarm stores settings and presets locally on your device only.

The app does not require an account, server connection, analytics, telemetry, ads, or cloud syncing.

For the full privacy policy, see:

CursorSwarm_PrivacyPolicy.txt

--------------------------------------------------
TERMS AND SAFETY NOTICE
--------------------------------------------------

CursorSwarm is provided as an experimental cursor effects app.

By using CursorSwarm, you understand that it can make the cursor difficult to see or control, especially in Nightmare and Mirror modes.

Use Safe Mode, Quit Safely, and the standalone emergency restore EXE if needed.

For the full terms and safety notice, see:

CursorSwarm_TermsAndSafety.txt

--------------------------------------------------
FILES
--------------------------------------------------

CursorSwarm may create these support files if they are missing:

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

In normal portable EXE mode, these files are created beside CursorSwarm.exe.

In MSIX mode, Windows may install the app in a read-only package folder, so CursorSwarm stores support files in:

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
CONTROL PANEL
--------------------------------------------------

CursorSwarm opens the Control Panel automatically when launched.

You can also open or hide it anytime with:

Ctrl + Alt + C

If the panel is hidden, CursorSwarm briefly displays a reminder showing this shortcut.

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
3. Press Ctrl + Alt + C to hide the Control Panel.
4. Confirm the shortcut hint appears briefly.
5. Press Ctrl + Alt + C again to reopen the Control Panel.
6. Press Ctrl + Alt + Space for Safe Mode.
7. Press Ctrl + Alt + Q to quit safely.

Make sure the cursor restores normally.

--------------------------------------------------
TROUBLESHOOTING
--------------------------------------------------

If the cursor is hidden:
    Press Ctrl + Alt + R or Ctrl + Alt + Q.

If movement is confusing:
    Press Ctrl + Alt + Space for Safe Mode.

If the app is closed but the cursor is still hidden:
    Run restore_cursor_emergency.exe.

If config files are broken:
    Delete cursor_settings.json and restart the app.
    The app will recreate it.

If presets are broken:
    Use Reset All Custom Presets from the app,
    or delete cursor_presets.json and restart.

--------------------------------------------------
VERSION
--------------------------------------------------

CursorSwarm v10.8

v10.7
    Release-readiness polish, privacy policy, terms/safety notice, and final pre-publishing documents.

v10.8
    Certification fix and recovery polish: visible Control Panel on launch, temporary shortcut hint, Store-friendly Start Menu packaging, and standalone emergency restore EXE support.

Copyright (C) 2026 Palugula Tharun Kumar.
