# Quick Start (For Developers)

**TL;DR:** Claude usage monitor. GTK4 tray app. Auto-syncs from claude.ai API.

## Install

```bash
git clone https://github.com/UncleTallest/headroom.git
cd headroom
./install.sh
```

## Setup

```bash
./claude-setup-session  # Follow wizard
./claude-auto-sync       # Test it
./headroom.py            # Launch
```

## Autostart

```bash
cp headroom.desktop ~/.config/autostart/
```

## Auto-Sync (Cron)

```bash
crontab -e
# Add: */5 * * * * /path/to/headroom/claude-auto-sync
```

## Manual Sync Fallback

```bash
./claude-sync-usage 44 60  # session% weekly%
```

## Requirements

- Linux (GTK4 desktop environment)
- Python 3.11+
- Claude Pro or Max account

Done.
