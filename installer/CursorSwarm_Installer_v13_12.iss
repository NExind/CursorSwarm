#define MyAppName "CursorSwarm"
#define MyAppVersion "13.12.0"
#define MyAppPublisher "Palugula Tharun Kumar"
#define MyAppExeName "CursorSwarm.exe"

[Setup]
; Keep the same AppId as older CursorSwarm Inno installers so upgrades work correctly.
AppId={{8D7E8F0B-3E2A-4D90-9D8A-57C8A9C6B1A4}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={localappdata}\CursorSwarm
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
PrivilegesRequired=lowest
OutputDir=Output
OutputBaseFilename=CursorSwarm_Setup_v13_12
SetupIconFile=cursor_swarm.ico
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
UninstallDisplayIcon={app}\{#MyAppExeName}
LicenseFile=CursorSwarm_TermsAndSafety.txt
InfoBeforeFile=CursorSwarm_PrivacyPolicy.txt

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional shortcuts:"; Flags: unchecked

[Files]
Source: "CursorSwarm.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "cursor_swarm.ico"; DestDir: "{app}"; Flags: ignoreversion skipifsourcedoesntexist
Source: "restore_cursor_emergency.exe"; DestDir: "{app}"; Flags: ignoreversion skipifsourcedoesntexist
Source: "restore_cursor_emergency.py"; DestDir: "{app}"; Flags: ignoreversion skipifsourcedoesntexist
Source: "README.txt"; DestDir: "{app}"; Flags: ignoreversion skipifsourcedoesntexist
Source: "CursorSwarm_PrivacyPolicy.txt"; DestDir: "{app}"; Flags: ignoreversion skipifsourcedoesntexist
Source: "Privacy_Policy.txt"; DestDir: "{app}"; DestName: "CursorSwarm_PrivacyPolicy.txt"; Flags: ignoreversion skipifsourcedoesntexist
Source: "CursorSwarm_TermsAndSafety.txt"; DestDir: "{app}"; Flags: ignoreversion skipifsourcedoesntexist
Source: "Terms_and_Safety.txt"; DestDir: "{app}"; DestName: "CursorSwarm_TermsAndSafety.txt"; Flags: ignoreversion skipifsourcedoesntexist
Source: "CursorSwarm_ReleaseNotes.txt"; DestDir: "{app}"; Flags: ignoreversion skipifsourcedoesntexist
Source: "Release_Notes.txt"; DestDir: "{app}"; DestName: "CursorSwarm_ReleaseNotes.txt"; Flags: ignoreversion skipifsourcedoesntexist

[Icons]
Name: "{group}\CursorSwarm"; Filename: "{app}\CursorSwarm.exe"
Name: "{autodesktop}\CursorSwarm"; Filename: "{app}\CursorSwarm.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\CursorSwarm.exe"; Description: "Launch CursorSwarm"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: files; Name: "{app}\cursor_presets.json"
Type: files; Name: "{app}\cursor_settings.json"
Type: files; Name: "{app}\cursor_custom_themes.json"
Type: files; Name: "{app}\cursor_custom_multi_presets.json"
Type: files; Name: "{app}\cursor_shape_profiles.json"
Type: files; Name: "{app}\restore_cursor_emergency.py"
Type: files; Name: "{app}\README.txt"
Type: files; Name: "{app}\CursorSwarm_PrivacyPolicy.txt"
Type: files; Name: "{app}\CursorSwarm_TermsAndSafety.txt"
Type: files; Name: "{app}\CursorSwarm_ReleaseNotes.txt"
Type: dirifempty; Name: "{app}"
