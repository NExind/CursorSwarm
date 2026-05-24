#define MyAppName "CursorSwarm"
#define MyAppVersion "11.0.0"
#define MyAppPublisher "Palugula Tharun Kumar"
#define MyAppExeName "CursorSwarm.exe"

[Setup]
AppId={{8D7E8F0B-3E2A-4D90-9D8A-57C8A9C6B1A4}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={localappdata}\CursorSwarm
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
PrivilegesRequired=lowest
OutputDir=Output
OutputBaseFilename=CursorSwarm_Setup_v11_0
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
Source: "restore_cursor_emergency.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "CursorSwarm_PrivacyPolicy.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "CursorSwarm_TermsAndSafety.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "CursorSwarm_ReleaseNotes.txt"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\CursorSwarm"; Filename: "{app}\CursorSwarm.exe"
Name: "{autodesktop}\CursorSwarm"; Filename: "{app}\CursorSwarm.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\CursorSwarm.exe"; Description: "Launch CursorSwarm"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: files; Name: "{app}\cursor_presets.json"
Type: files; Name: "{app}\cursor_settings.json"
Type: files; Name: "{app}
estore_cursor_emergency.py"
Type: files; Name: "{app}\README.txt"
Type: files; Name: "{app}\CursorSwarm_PrivacyPolicy.txt"
Type: files; Name: "{app}\CursorSwarm_TermsAndSafety.txt"
Type: files; Name: "{app}\CursorSwarm_ReleaseNotes.txt"
Type: dirifempty; Name: "{app}"
