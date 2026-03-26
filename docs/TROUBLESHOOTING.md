# Troubleshooting Guide

Common issues and solutions for headroom.

---

## Installation Issues

### "command not found: git"

**Solution:** Install git first:

```bash
# Ubuntu/Debian
sudo apt install git

# Arch/Manjaro
sudo pacman -S git

# Fedora
sudo dnf install git
```

### "Permission denied" when running install.sh

**Solution:** Make it executable:

```bash
chmod +x install.sh
```

### Installer fails with package errors

**Solution:** Update your package manager first:

```bash
# Ubuntu/Debian
sudo apt update

# Arch/Manjaro
sudo pacman -Syu

# Fedora
sudo dnf update
```

---

## Setup Issues

### "Cannot locate INSTANCE_HOME"

**Cause:** headroom can't find where to store data.

**Solution:** Create the directory:

```bash
mkdir -p ~/.claude/logs
```

Or set the environment variable:

```bash
export INSTANCE_HOME=~/.claude
# Add to ~/.bashrc to make permanent
```

### "403 Forbidden" during claude-auto-sync

**Cause:** Session cookie expired or invalid.

**Solution:** Re-run setup with fresh cookies:

```bash
./claude-setup-session
```

Get new cookies from Chrome DevTools (see INSTALL.md step 5).

### Can't find Organization ID in DevTools

**Cause:** You might be looking at the wrong request.

**Solution:**
1. Clear the Network tab (click the ⃠ icon)
2. Refresh Claude Settings → Usage page
3. Look for the request named just `usage` (not other requests)
4. The Organization ID is in the URL

---

## Runtime Issues

### No system tray icon appears

**Cause:** Your desktop environment doesn't support AppIndicator.

**Solution:** The window still works! Just keep it open:

```bash
./headroom.py
```

Minimize it if you want. It will still update in the background.

**Affected desktops:**
- GNOME (without extension)
- Some tiling window managers
- Wayland sessions (sometimes)

**Workaround:** Install GNOME Shell extension "AppIndicator Support"

### Window shows "No usage data available"

**Cause:** No sync has run yet or state file is empty.

**Solution:** Run a sync:

```bash
./claude-auto-sync
```

Or manual sync:

```bash
./claude-sync-usage 44 60
```

### Percentage shows 0% but I've used Claude

**Cause:** Usage hasn't synced recently.

**Solution:** Right-click tray icon → "Sync Now"

Or run manually:

```bash
./claude-auto-sync
```

### "Failed to fetch usage: 403" repeatedly

**Cause:** Cookie expired (they expire after ~30 days).

**Solution:** Get a fresh cookie:

```bash
./claude-setup-session
```

### Notifications not appearing

**Cause:** Desktop notifications might be disabled.

**Check:**
1. System Settings → Notifications
2. Make sure notifications are enabled
3. Check if "headroom" is in the allowed apps list

**Test notifications:**

```bash
notify-send "Test" "If you see this, notifications work"
```

---

## Auto-Sync Issues

### Cron job not running

**Check if cron is running:**

```bash
systemctl status cron
# OR
systemctl status cronie
```

**Check cron logs:**

```bash
grep CRON /var/log/syslog
```

**Verify your crontab:**

```bash
crontab -l
```

Make sure the path is absolute:

```
*/5 * * * * /home/tallest/headroom/claude-auto-sync
```

**Test the script manually:**

```bash
/home/tallest/headroom/claude-auto-sync
```

### Auto-sync runs but data doesn't update

**Cause:** Script might be failing silently.

**Solution:** Check for errors:

```bash
# Run manually and look for errors
./claude-auto-sync

# Check if state file is updating
ls -lh ~/.claude/logs/limit-tracker-state.json
```

---

## Performance Issues

### High CPU usage

**Cause:** Probably not headroom (it uses ~0% CPU).

**Check:**

```bash
top
# Look for "headroom" process
```

If headroom is using >1% CPU constantly, something's wrong.

**Solution:** Restart it:

```bash
pkill -f headroom
./headroom.py
```

### High memory usage

**Normal:** ~15-20MB RAM

**If higher:** Restart the app:

```bash
pkill -f headroom
./headroom.py
```

---

## Display Issues

### Progress bar not colored correctly

**Cause:** GTK theme might not support color classes.

**Solution:** This is cosmetic only. Usage numbers are still accurate.

### Window too small/too big

**Cause:** DPI scaling or theme settings.

**Temporary fix:** Resize the window manually. It will remember the size.

### Text hard to read

**Cause:** Dark theme + dark window or vice versa.

**Solution:** Check your system theme settings. headroom follows your system theme.

---

## Getting Help

### Check logs

headroom doesn't keep logs by default, but you can run it with debug output:

```bash
./headroom.py 2>&1 | tee headroom-debug.log
```

### Still stuck?

1. Check the GitHub Issues: https://github.com/UncleTallest/headroom/issues
2. Open a new issue with:
   - Your Linux distribution
   - Desktop environment (GNOME, KDE, etc.)
   - Error messages
   - Output of `./claude-auto-sync`

### Security Concerns

**"Is it safe to give headroom my cookie?"**

Yes. Your cookie:
- Stays on your computer (never sent anywhere except Claude's official API)
- Is stored with restricted permissions (only you can read it)
- Expires automatically after ~30 days (same as browser)
- Can be revoked by logging out of claude.ai

headroom is open source - you can read the code to verify this.

---

## Advanced Troubleshooting

### Manually inspect state file

```bash
cat ~/.claude/logs/limit-tracker-state.json | python3 -m json.tool
```

### Check session file

```bash
cat ~/.claude/config/claude-session.json | python3 -m json.tool
```

**Don't share this file** - it contains your session cookie!

### Test API call manually

```bash
# Extract from your session file
ORG_ID="your-org-id-here"
COOKIES="your-cookies-here"

curl "https://claude.ai/api/organizations/$ORG_ID/usage" \
  -H "Cookie: $COOKIES"
```

You should get JSON back with usage data.

---

**If nothing here helps:** Open an issue on GitHub with details!
