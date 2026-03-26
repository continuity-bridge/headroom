# headroom File Structure

```
headroom/
├── README.md              # Main documentation
├── LICENSE                # Apache 2.0
├── install.sh             # One-command installer
├── headroom.py            # Main GTK4 application
├── headroom.desktop       # Autostart file
│
├── claude-auto-sync       # Automatic API fetcher
├── claude-sync-usage      # Manual sync fallback
├── claude-setup-session   # First-time setup wizard
│
├── docs/
│   ├── INSTALL.md         # Step-by-step beginner guide
│   ├── QUICKSTART.md      # Quick reference for developers
│   ├── TROUBLESHOOTING.md # Common issues and solutions
│   └── ARCHITECTURE.md    # Technical details
│
├── examples/
│   ├── claude-api-sniffer.py       # Network traffic capture
│   ├── claude-scrape-usage         # UI automation approach
│   ├── claude-usage-reader.py      # LevelDB reader (plyvel)
│   └── claude-usage-simple-reader.py # Pure Python parser
│
└── .gitignore
```

## Core Files (Required)

### User-Facing Tools
- `headroom.py` - The main application (system tray monitor)
- `claude-auto-sync` - Fetches usage from Claude API automatically
- `claude-sync-usage` - Manual sync when auto doesn't work
- `claude-setup-session` - Wizard to save API credentials

### Installation & Config
- `install.sh` - Automated installer
- `headroom.desktop` - Desktop entry for autostart
- `README.md` - Project overview and basic usage

### Documentation
- `docs/INSTALL.md` - Detailed beginner-friendly setup
- `docs/QUICKSTART.md` - TL;DR for developers
- `docs/TROUBLESHOOTING.md` - Common problems and fixes

## Optional Files

### Examples (Alternative Approaches)
Files in `examples/` show different ways we tried to solve the problem:
- **API sniffer** - Capturing network traffic
- **UI scraper** - Automating Claude Desktop UI
- **LevelDB readers** - Trying to read local cache

These are educational but not needed for normal use.

## Files to Exclude from Git

- `claude-leveldb-dump.json` - Contains user data
- `*.pyc`, `__pycache__/` - Python bytecode
- `.vscode/`, `.idea/` - Editor configs
- `test-*.json` - Test data files

## Where Things Get Stored

When installed, headroom creates:
```
~/.claude/
├── logs/
│   └── limit-tracker-state.json  # Current usage data
└── config/
    └── claude-session.json        # API credentials (600 perms)
```

And if you enable autostart:
```
~/.config/autostart/
└── headroom.desktop
```

## Why This Structure?

- **Root level** = Core tools users need
- **docs/** = All documentation in one place
- **examples/** = Learning resources, not production
- **Flat structure** = Easy to understand, no deep nesting
