# headroom

**Know your Claude usage before you hit the limit.**

A lightweight system tray monitor that shows your Claude Pro/Max usage in real-time. Named after the audio engineering term for remaining capacity.

![System tray showing 52%](docs/screenshot-tray.png)

---

## What It Does

headroom sits in your system tray and shows you:
- **Current session usage** (5-hour rolling window)
- **Weekly usage** (7-day total)
- **Reset times** (when limits refresh)
- **Desktop notifications** (at 80%, 90%, 95%)

Think of it like your phone's battery indicator, but for Claude.

---

## Quick Install

```bash
git clone https://github.com/UncleTallest/headroom.git
cd headroom
./install.sh
./claude-setup-session
./headroom.py
```

**Need detailed instructions?** → [Step-by-Step Guide](docs/INSTALL.md)

**Just want the TL;DR?** → [Quick Start](docs/QUICKSTART.md)

---

## Features

✅ **System tray icon** - Usage percentage always visible  
✅ **Automatic sync** - Fetches real usage from Claude's API  
✅ **Manual fallback** - Works even if auto-sync fails  
✅ **Desktop notifications** - Alerts at 80%, 90%, 95%  
✅ **Color-coded** - Green/yellow/orange/red based on usage  
✅ **Detailed breakdown** - See chat/code/cowork separately  
✅ **Lightweight** - ~15MB RAM, 0% CPU  
✅ **Works for web users** - Don't need Claude Desktop  

---

## Requirements

- **Linux** (Ubuntu, Debian, Arch, Fedora, etc.)
- **GTK4** desktop environment
- **Python 3.11+**
- **Claude Pro or Max** account (Free doesn't have usage limits)

---

## How It Works

headroom fetches your usage directly from Claude's API - the same endpoint that powers Settings → Usage in claude.ai.

1. You set up API access once (one-time setup wizard)
2. headroom syncs automatically every 5 minutes
3. Your usage appears in the system tray
4. Click for details, right-click for menu

**Is it safe?** Yes. Your session cookie stays on your computer (never sent anywhere except Claude's official API) and is stored with restricted permissions. See [Security](#security) below.

---

## Screenshots

### System Tray
![Tray icon showing 52%](docs/screenshot-tray.png)

### Details Window
![Details showing session and weekly usage](docs/screenshot-window.png)

### Notifications
![Notification: "Claude Usage High - 90%"](docs/screenshot-notification.png)

---

## Documentation

- **[Installation Guide](docs/INSTALL.md)** - Step-by-step for beginners
- **[Quick Start](docs/QUICKSTART.md)** - TL;DR for developers
- **[Troubleshooting](docs/TROUBLESHOOTING.md)** - Common issues
- **[File Structure](docs/STRUCTURE.md)** - What's in this repo

---

## Usage

### Launch headroom

```bash
./headroom.py
```

The tray icon shows your current usage percentage.

### System Tray Menu

- **Show Usage** → Open detailed window
- **Sync Now** → Fetch latest usage manually
- **Quit** → Exit headroom

### Automatic Sync

Set up cron to auto-sync every 5 minutes:

```bash
crontab -e
# Add: */5 * * * * /path/to/headroom/claude-auto-sync
```

### Manual Sync (Fallback)

If auto-sync breaks:

```bash
# Check Claude Desktop Settings → Usage
# See: Session 44%, Weekly 60%
./claude-sync-usage 44 60
```

### Autostart (Optional)

Launch on login:

```bash
cp headroom.desktop ~/.config/autostart/
```

---

## Components

- `headroom.py` - Main GTK4 application
- `claude-auto-sync` - Fetches usage from Claude API
- `claude-sync-usage` - Manual sync fallback
- `claude-setup-session` - First-time setup wizard
- `install.sh` - One-command installer

---

## Security

**Your session cookie is sensitive.** headroom handles it carefully:

✅ Stored locally with 0600 permissions (only you can read)  
✅ Never sent anywhere except Claude's official API  
✅ Expires automatically after ~30 days (same as browser)  
✅ Can be revoked by logging out of claude.ai  
✅ Open source - read the code yourself  

**We never:**
- ❌ Send your cookie to any third party
- ❌ Log your conversations or usage patterns
- ❌ Store anything in the cloud
- ❌ Phone home to any server

---

## FAQ

**Q: Does this work with Claude Free?**  
A: No, Free plan has no usage limits to monitor.

**Q: Will this break if Claude changes their API?**  
A: Possibly. It uses an internal endpoint that could change. Open an issue if it breaks!

**Q: Can I use this with the Claude API (not claude.ai)?**  
A: No, this monitors claude.ai web/desktop usage, not API usage.

**Q: Does this track my conversations?**  
A: No, only aggregate usage numbers (percentages and reset times).

**Q: Why Linux only?**  
A: GTK4 system tray support is best on Linux. Windows/Mac support is possible but not implemented yet.

**Q: My desktop doesn't show system tray icons!**  
A: Some desktops (like GNOME, Cinnamon) don't support AppIndicator by default. headroom will run in window-only mode - just keep the window open! The auto-sync and notifications still work perfectly. See [Troubleshooting](docs/TROUBLESHOOTING.md).

---

## Troubleshooting

**Common issues:**

- **No tray icon** → [Your desktop doesn't support AppIndicator](docs/TROUBLESHOOTING.md#no-system-tray-icon-appears)
- **403 Forbidden** → [Cookie expired, re-run setup](docs/TROUBLESHOOTING.md#403-forbidden-during-claude-auto-sync)
- **Can't find Org ID** → [Check Network tab carefully](docs/TROUBLESHOOTING.md#cant-find-organization-id-in-devtools)
- **Cron not working** → [Check cron service and logs](docs/TROUBLESHOOTING.md#cron-job-not-running)

**Full guide:** [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)

---

## Contributing

Contributions welcome!

1. Fork the repo
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

**Areas that need help:**
- Windows/Mac support
- System tray alternatives for GNOME Wayland
- Better error messages
- Unit tests
- Translations

---

## Roadmap

**v1.0** (current):
- ✅ GTK4 system tray app
- ✅ Automatic API sync
- ✅ Desktop notifications
- ✅ Manual sync fallback

**v1.1** (planned):
- [ ] Better GNOME Wayland support
- [ ] Configurable notification thresholds
- [ ] Usage history graphs
- [ ] Export usage data to CSV

**v2.0** (future):
- [ ] Windows support
- [ ] macOS support
- [ ] Alternative to system tray (menu bar/panel widget)

---

## License

Apache 2.0

---

## Author

**Uncle Tallest** (Jerry Jackson)  
Built with Vector

Part of the [Continuity Bridge](https://github.com/continuity-bridge) ecosystem

---

## Acknowledgments

- Named after the audio engineering term for headroom (remaining capacity)
- Inspired by the need to know usage before starting heavy Claude tasks
- Built because manually checking Settings → Usage got annoying
- API endpoint discovered via Chrome DevTools (thanks Chrome team!)

---

**Remember:** headroom shows you capacity. Use it strategically! 🎯
