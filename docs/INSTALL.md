# Installing headroom - Step by Step Guide

**For people who are comfortable with computers but new to command-line tools.**

This guide assumes you:
- Know how to open a terminal/command prompt
- Can copy and paste commands
- Are comfortable with basic file operations

---

## What You're Installing

**headroom** is a small program that sits in your system tray (the bar at the top/bottom of your screen) and shows you how much of your Claude usage limit you've used.

Think of it like your phone's battery indicator, but for Claude usage.

---

## Step 1: Check Your System

headroom works on **Linux only** (for now). Specifically:
- Ubuntu, Debian, Linux Mint
- Arch Linux, Manjaro
- Fedora

**Windows/Mac users:** Sorry, not supported yet! You can still use the manual sync method.

---

## Step 2: Open Terminal

**Ubuntu/Debian/Mint:**
- Press `Ctrl+Alt+T`
- Or search for "Terminal" in your applications

**Other Linux:**
- Search for "Terminal" or "Console" in your application menu

You should see a window with text and a cursor.

---

## Step 3: Download headroom

**If you have git installed:**

```bash
cd ~
git clone https://github.com/UncleTallest/headroom.git
cd headroom
```

**If you don't have git:**

1. Go to https://github.com/UncleTallest/headroom
2. Click the green "Code" button
3. Click "Download ZIP"
4. Extract the ZIP file somewhere (like your home folder)
5. Open terminal and navigate to it:

```bash
cd ~/headroom
```

---

## Step 4: Run the Installer

The installer will:
- Install system packages (will ask for your password)
- Install Python requirements
- Make scripts executable

**Copy and paste this into your terminal:**

```bash
chmod +x install.sh
./install.sh
```

**What you'll see:**
- Password prompt (type your password - you won't see it as you type)
- Some text scrolling by as packages install
- "Installation complete!" message

**If you get errors:**
- Write down the error message
- Skip to "Troubleshooting" at the bottom

---

## Step 5: Set Up Your Claude Access

headroom needs permission to check your Claude usage. This is a one-time setup.

**Run the setup wizard:**

```bash
./claude-setup-session
```

**You'll be asked for two things:**

### Part A: Organization ID

1. Open **Google Chrome** (Firefox/Edge won't work for this)
2. Go to https://claude.ai
3. Log in if you aren't already
4. Press `F12` on your keyboard (opens Developer Tools)
5. Click the **Network** tab at the top
6. In Claude.ai, click your name (bottom left) → Settings → Usage
7. Look in the Network tab for a line that says `usage`
8. Click on it
9. Look for the URL at the top - it will look like:
   ```
   https://claude.ai/api/organizations/f7d63567-c0b6-4e6a-9358-8bd0ead8af9b/usage
   ```
10. Copy the long code between `/organizations/` and `/usage`
    - In the example above: `f7d63567-c0b6-4e6a-9358-8bd0ead8af9b`
11. Paste it into the terminal when asked

### Part B: Cookie String

1. Still in Chrome DevTools, with the `usage` request selected
2. Click the **Headers** tab
3. Scroll down to **Request Headers**
4. Find the line that starts with `cookie:`
5. The value is VERY LONG - it looks like:
   ```
   anthropic-device-id=abc123...; sessionKey=sk-ant-sid02-...; __cf_bm=...; ...
   ```
6. Click at the start of the value, hold Shift, click at the end
7. Copy it (Ctrl+C)
8. Paste into the terminal when asked (Ctrl+Shift+V in terminal)

**You should see:** "✓ Session saved!"

**If something went wrong:** Don't worry, you can run `./claude-setup-session` again.

---

## Step 6: Test It!

Let's see if it works:

```bash
./claude-auto-sync
```

**You should see:**
```
Claude Auto-Sync
==================================================
Fetching usage for organization f7d63567...

✓ Auto-sync complete!
  Session: 52.0% (resets in 5h 16m)
  Weekly: 61.0% (resets Fri 6:59 PM)

  headroom will now show this usage
```

**If you got that, it's working!** 🎉

---

## Step 7: Run headroom

Now launch the actual monitor:

```bash
./headroom.py
```

**What you should see:**
- A window opens showing your usage
- An icon appears in your system tray showing a percentage

**Click the tray icon** to open the detailed window.

**Right-click the tray icon** for the menu (Sync Now / Quit).

---

## Step 8: Make It Start Automatically (Optional)

If you want headroom to launch every time you log in:

```bash
mkdir -p ~/.config/autostart
cp headroom.desktop ~/.config/autostart/
```

Now headroom will start automatically when you log in.

---

## Step 9: Set Up Automatic Syncing (Optional)

Make headroom check for updates every 5 minutes:

```bash
crontab -e
```

**First time?** You'll be asked to choose an editor. Pick `nano` (usually option 1).

**Add this line at the bottom:**

```
*/5 * * * * /home/YOUR_USERNAME/headroom/claude-auto-sync
```

**Replace `YOUR_USERNAME` with your actual username!**

Press `Ctrl+X`, then `Y`, then `Enter` to save.

---

## You're Done! 🎉

headroom is now installed and running!

**What it does:**
- Shows your Claude usage percentage in your system tray
- Updates automatically every 5 minutes (if you set up cron)
- Sends notifications at 80%, 90%, 95% usage
- Color-coded: green (safe), yellow (watch it), red (almost full)

**Daily use:**
- Just look at your system tray to check usage
- Click for details
- Right-click → "Sync Now" to update immediately

---

## Troubleshooting

### "There was an error launching the application"

**Your desktop environment might not support system trays.** The window will still work:

```bash
./headroom.py
```

Just bookmark this window - it'll still update and work fine.

### "403 Forbidden" when running claude-auto-sync

Your session cookie expired. Re-run the setup:

```bash
./claude-setup-session
```

And grab a fresh cookie from Chrome DevTools.

### "Cannot locate INSTANCE_HOME"

Create the directory structure:

```bash
mkdir -p ~/.claude/logs
```

### "ModuleNotFoundError: No module named 'gi'"

The installer didn't work. Install manually:

**Ubuntu/Debian:**
```bash
sudo apt install python3-gi gir1.2-gtk-4.0 gir1.2-adw-1 gir1.2-appindicator3-0.1
```

**Arch/Manjaro:**
```bash
sudo pacman -S python-gobject gtk4 libadwaita libappindicator-gtk3
```

### Need More Help?

1. Check the full README.md
2. Open an issue on GitHub
3. Ask in r/ClaudeAI on Reddit

---

## Manual Sync Method (If Auto-Sync Doesn't Work)

If you can't get automatic syncing to work, you can still update manually:

1. Open Claude Desktop or claude.ai
2. Go to Settings → Usage
3. Note the two percentages (Session % and Weekly %)
4. Run:

```bash
./claude-sync-usage 44 60
```

(Replace 44 and 60 with your actual percentages)

headroom will update immediately.

---

**That's it! You're all set.** Enjoy knowing your Claude headroom! 🎯
