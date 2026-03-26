# Moving headroom to Standalone Repo

Quick commands to set up headroom as its own project:

```bash
# Create new repo directory
mkdir ~/Devel/headroom
cd ~/Devel/headroom

# Initialize git
git init
git branch -M main

# Copy files from limit-monitor
cp ~/Devel/UncleTallest/organizations/continuity-bridge/limit-monitor/headroom/* .

# Create .gitignore
cat > .gitignore << 'EOF'
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.so
*.egg-info/
dist/
build/
*.log
.vscode/
.idea/
*.swp
*~
EOF

# Initial commit
git add .
git commit -m "Initial commit: headroom v1.0

- GTK4 system tray usage monitor
- Automatic API sync
- Desktop notifications
- Manual sync fallback
- Full README and install script"

# Create GitHub repo (if gh cli installed)
gh repo create headroom --public --source=. --remote=origin
git push -u origin main

# Or manually:
# 1. Create repo on GitHub: https://github.com/new
# 2. git remote add origin git@github.com:UncleTallest/headroom.git
# 3. git push -u origin main
```

## Files to include:

- ✅ headroom.py (main app)
- ✅ claude-auto-sync (API fetcher)
- ✅ claude-sync-usage (manual sync)
- ✅ claude-setup-session (wizard)
- ✅ headroom.desktop (autostart)
- ✅ README.md (docs)
- ✅ install.sh (installer)
- ✅ .gitignore
- ⬜ LICENSE (Apache 2.0)
- ⬜ docs/screenshot.png (take screenshot)
- ⬜ CONTRIBUTING.md (optional)

## Post-publish:

1. Add topics: `claude`, `usage-monitor`, `gtk4`, `system-tray`, `linux`
2. Create release: v1.0.0
3. Add screenshot to README
4. Share on r/ClaudeAI, HN, etc.
