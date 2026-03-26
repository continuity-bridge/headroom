# Installing headroom - Simple Guide

**For people who don't use GitHub and just want it to work.**

---

## What You're Installing

**headroom** shows your Claude usage in your system tray (the bar at the bottom of your screen). Think of it like your phone's battery indicator, but for Claude.

---

## Step 1: Download

1. Go to: https://github.com/continuity-bridge/headroom
2. Click the green **"Code"** button
3. Click **"Download ZIP"**
4. Save it somewhere (like your Downloads folder)

---

## Step 2: Extract

1. Find the ZIP file you downloaded (`headroom-main.zip`)
2. Right-click it
3. Choose **"Extract Here"** or **"Extract to..."**
4. You'll get a folder called `headroom-main`
5. Move this folder somewhere easy to find (like your home folder)

---

## Step 3: Open Terminal

1. Open your file browser
2. Go into the `headroom-main` folder
3. Right-click in the empty space
4. Choose **"Open in Terminal"** (or similar)

A black window with text should appear.

---

## Step 4: Install

**Copy and paste this into the terminal:**

```bash
chmod +x install.sh
./install.sh
```

**What happens:**
- You'll be asked for your password (type it - you won't see it, that's normal)
- Some text will scroll by
- You'll see "Installation complete!"

**If you get errors:**
- Take a screenshot
- Ask for help

---

## Step 5: Setup Your Claude Account

**Copy and paste this:**

```bash
./claude-setup-session
```

**You'll need two things from Chrome:**

### Part A: Organization ID

1. Open **Google Chrome** (must be Chrome, not Firefox)
2. Go to https://claude.ai
3. Log in
4. Press **F12** on your keyboard
5. Click the **"Network"** tab at the top
6. In Claude, click your name (bottom left) → **Settings** → **Usage**
7. Look in the Network tab for a line called `usage`
8. Click on it
9. The URL at the top looks like:
   ```
   https://claude.ai/api/organizations/abc123.../usage
   ```
10. Copy the long code between `/organizations/` and `/usage`
11. Paste it when asked

### Part B: Cookie

1. Still in Chrome DevTools, with the `usage` request selected
2. Click the **"Headers"** tab
3. Scroll down to **"Request Headers"**
4. Find the line starting with `cookie:`
5. The value is VERY LONG - select it all and copy
6. Paste it when asked

**You should see:** "✓ Session saved!"

---

## Step 6: Test It

**Copy and paste this:**

```bash
./headroom.py
```

**What you should see:**
- A window opens showing your usage
- An icon appears in your system tray showing a percentage

**Click the tray icon** to show the window  
**Right-click the tray icon** for the menu

---

## Step 7: Make It Start Automatically (Optional)

**Copy and paste this:**

```bash
cp headroom.desktop ~/.config/autostart/
```

Now headroom will start every time you log in!

---

## Step 8: Automatic Updates (Optional)

To make headroom check for usage updates every 5 minutes:

**Copy and paste this:**

```bash
crontab -e
```

**First time?** Pick `nano` (usually option 1)

**Add this line at the bottom:**

```
*/5 * * * * /home/YOUR_USERNAME/headroom-main/claude-auto-sync
```

**IMPORTANT:** Replace `YOUR_USERNAME` with your actual username!

Press **Ctrl+X**, then **Y**, then **Enter** to save.

---

## You're Done! 🎉

headroom is now running!

**What it does:**
- Shows your Claude usage percentage in the system tray
- Updates automatically every 5 minutes (if you set up cron)
- Warns you when you're getting close to your limit

**Daily use:**
- Just look at the system tray to check usage
- Click for details
- Right-click for menu

---

## Troubleshooting

### "There was an error launching the application"

Your desktop might not support system trays. The window still works though! Just keep it open.

### "403 Forbidden" when syncing

Your session cookie expired. Run `./claude-setup-session` again and get a fresh cookie from Chrome.

### Can't find the headroom-main folder

Look in your home folder or Downloads folder. You might have extracted it somewhere else.

### Nothing works

1. Take a screenshot of the error
2. Write down exactly what you did
3. Ask for help

---

**That's it! Simple as that.** 🚀
