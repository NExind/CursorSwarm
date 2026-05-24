# CursorSwarm v11.0 GitHub Update Checklist

Use this pack to update the public GitHub repository to match the current Microsoft Store v11.0 release.

## Files to replace/add

- `README.md`
- `src/cursor_swarm_v11_0.py`
- `docs/README.txt`
- `docs/CursorSwarm_ReleaseNotes.txt`
- `docs/CursorSwarm_PrivacyPolicy.txt`
- `docs/CursorSwarm_TermsAndSafety.txt`
- `docs/CursorSwarm_CertificationNotes_v11_0.txt`
- `packaging/cursor_swarm_version_info_v11_0.txt`
- `packaging/restore_cursor_emergency_version_info_v11_0.txt`
- `installer/CursorSwarm_Setup.iss`
- `release_notes/GITHUB_RELEASE_DRAFT_v11_0.md`

## Suggested commands

```powershell
git status
git pull origin main

# Copy the files from this pack into the repo, preserving folders.

python -m py_compile src\cursor_swarm_v11_0.py

git add README.md src\cursor_swarm_v11_0.py docs installer packaging release_notes
git commit -m "Update CursorSwarm repo to v11.0"
git tag v11.0
git push origin main
git push origin v11.0
```

## Do not commit

- `.exe`
- `.msix`
- `.msixupload`
- `dist/`
- `build/`
- `.venv/`
- `.pfx`, `.cer`, `.key`, `.pem`
