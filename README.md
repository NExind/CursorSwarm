# CursorSwarm

CursorSwarm is a Windows desktop cursor effects app for fake cursor swarms, mirror movement, transparent cursor modes, presets, and visual cursor camouflage.

It is made for fun, experimentation, and user-controlled visual cursor effects.

## Latest Version

**CursorSwarm v11.0**

CursorSwarm v11.0 is the current Microsoft Store release. It modernizes the Control Panel with a CustomTkinter dark UI while keeping the Store-approved v10.9 cursor engine behavior unchanged.

## Download

[Download CursorSwarm on the Microsoft Store](https://apps.microsoft.com/detail/9MSN2VZMJVMW?hl=en-us&gl=US&ocid=pdpshare)

For source code, release notes, and development updates, see this GitHub repository.

## Features

- Fake cursor swarm visual effects
- Mirror movement mode
- Transparent real cursor modes
- Runtime Control Panel
- Modern CustomTkinter dark UI
- Floating **CS** control button
- Global keyboard shortcuts
- Cursor presets
- Safe Mode and safe quit support
- Emergency cursor restore support
- Local desktop-only functionality

## What’s New in v11.0

- Redesigned the Control Panel using a modern CustomTkinter dark UI
- Kept the Store-approved v10.9 cursor engine behavior unchanged
- Kept the floating **CS** button for reopening/focusing the Control Panel
- Kept automatic Control Panel launch on startup
- Kept `Ctrl + Alt + C` for showing/hiding the Control Panel
- Kept Safe Mode, safe quit, mirror controls, presets, and emergency restore support
- Updated README, release notes, privacy policy, terms/safety notice, certification notes, installer script, and version metadata to v11.0

## Safety and Restore Controls

CursorSwarm can make the cursor harder to see or control. Stronger modes should not be used during important work, payments, exams, accessibility-dependent tasks, system configuration, or anything where cursor accuracy matters.

Important controls:

```text
Ctrl + Alt + C      = Open / close Control Panel
Floating CS button  = Reopen or focus Control Panel
Ctrl + Alt + Space  = Safe Mode / Resume Previous Mode
Ctrl + Alt + Q      = Quit Safely and restore cursor
Ctrl + Alt + R      = Toggle real system cursor visible / transparent
```

If the cursor is still hidden after closing the app, use the emergency restore helper included with the packaged release.

## Privacy

CursorSwarm is a local Windows desktop app. It does **not** collect, transmit, sell, rent, or share personal data.

The app stores settings and preset files locally on the user’s device. It does not use user accounts, cloud syncing, analytics, telemetry, advertising trackers, or remote servers.

## Repository Structure

```text
src/                         Main Python source files
docs/                        README, release notes, privacy, and safety documents
installer/                   Inno Setup installer script
packaging/                   PyInstaller version metadata
release_notes/               GitHub release draft notes
```

## Built With

- Python
- Tkinter / CustomTkinter
- Windows APIs
- PyInstaller
- Inno Setup / MSIX Packaging Tool

## Author

Created by **Palugula Tharun Kumar**.

## License

This project is licensed under the MIT License.
