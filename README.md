# CursorSwarm

CursorSwarm is a Windows desktop visual effects app that creates cursor swarm overlays, mirror movement effects, and customizable cursor presets.

## Latest Version

**CursorSwarm v10.9**

CursorSwarm v10.9 is the Microsoft Store-ready release focused on clearer controls, better visibility, and safer user access to the Control Panel.

## Features

- Fake cursor swarm visual effects
- Mirror movement mode
- Customizable cursor presets
- Runtime Control Panel
- Floating **CS** control button
- Global shortcut support
- Cursor visibility toggle and restore support
- Panic/safe mode support
- Local desktop-only functionality

## What’s New in v10.9

- Control Panel opens automatically on launch
- Floating **CS** button appears when the Control Panel is hidden
- Clicking the **CS** button opens the Control Panel
- Right-click menu on the **CS** button with:
  - Open Control Panel
  - Hide Floating Button
- `Ctrl + Alt + C` still toggles the Control Panel
- Only the main CursorSwarm shortcut is exposed in the Start Menu
- Updated certification notes and full-trust desktop explanation

## Important Notes

CursorSwarm is a local Windows desktop app.

It does **not** collect personal data, upload files, record user activity, or send data to a server.

The app may require full desktop access because it uses Windows desktop overlay behavior, local mouse movement handling, global keyboard shortcuts, and cursor visibility control for its core visual effects.

## Safety and Restore Controls

CursorSwarm includes safety controls so users can return the cursor to normal if cursor effects are enabled.

If the Control Panel is hidden, the floating **CS** button can be used to bring it back. The keyboard shortcut `Ctrl + Alt + C` can also be used to toggle the Control Panel.

## Built With

- Python
- Tkinter / Custom UI logic
- Windows APIs
- PyInstaller
- Inno Setup / MSIX packaging tools

## Download

The Windows executable and installer are available from the GitHub Releases section.

## Author

Created by **Palugula Tharun Kumar**.

## License

This project is licensed under the MIT License.
