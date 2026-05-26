# CursorSwarm v13.12 GitHub Update Checklist

Use this pack when you are ready to publish the v13.12 GitHub repo update.

## Before pushing

- Confirm Partner Center certification is approved.
- When you are ready, click Publish now in Partner Center.
- Replace the README.md Microsoft Store placeholder with the final Store link.
- Keep v14.x experimental files out of `main` for now.
- Do not commit EXE/MSIX/installer binaries into normal source folders.

## Files to copy into the repo

- `.gitignore`
- `README.md`
- `src/cursor_swarm_v13_12.py`
- `docs/README.txt`
- `docs/CursorSwarm_ReleaseNotes.txt`
- `docs/CursorSwarm_PrivacyPolicy.txt`
- `docs/CursorSwarm_TermsAndSafety.txt`
- `docs/CursorSwarm_CertificationNotes_v13_12.txt`
- `docs/Store_And_Repo_Link_Notes_v13_12.md`
- `packaging/cursor_swarm_version_info_v13_12.txt`
- `installer/CursorSwarm_Installer_v13_12.iss`
- `release_notes/GITHUB_RELEASE_DRAFT_v13_12.md`

## Suggested git commands

```powershell
git checkout main
git pull

# Copy the files from this update pack into your repo first.

git status
git add README.md .gitignore src/cursor_swarm_v13_12.py docs packaging/cursor_swarm_version_info_v13_12.txt installer/CursorSwarm_Installer_v13_12.iss release_notes/GITHUB_RELEASE_DRAFT_v13_12.md
git commit -m "Release CursorSwarm v13.12 stable source"
git tag v13.12
git push origin main
git push origin v13.12
```

## Optional cleanup

If you want main to show only the latest stable source, move the old v10.9 source to an archive folder instead of deleting it:

```powershell
mkdir archive10_9
move src\cursor_swarm_v10_9.py archive10_9\cursor_swarm_v10_9.py
git add archive10_9\cursor_swarm_v10_9.py src\cursor_swarm_v10_9.py
git commit -m "Archive CursorSwarm v10.9 source"
```

## GitHub Release

Create a GitHub Release with tag `v13.12`.
Use the body from:

```text
release_notes/GITHUB_RELEASE_DRAFT_v13_12.md
```

Recommended release title:

```text
CursorSwarm v13.12
```

Upload binaries to GitHub Releases only if you want direct downloads there. Do not commit binaries into the repo source tree.
