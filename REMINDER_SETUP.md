# Automatic pr-verify Reminders Setup

**Automatic reminders to use pr-verify - never forget again!**

---

## 🔔 What's Included

### **1. Git Hooks (Automatic)**
Already installed! They trigger when you use git:

```bash
# When you do: git commit
→ Shows reminder message
→ Suggests pr-verify commands

# When you do: git push
→ Shows reminder to run pr-check
→ Lists what it verifies
```

**Installed hooks:**
- `.git/hooks/prepare-commit-msg` - Commit-time reminder
- `.git/hooks/pre-push` - Push-time reminder

**Status:**
```bash
ls -la .git/hooks/prepare-commit-msg
ls -la .git/hooks/pre-push
```

---

## 📝 Option 1: Git Hook Reminders (Already Active!)

### How it works:
```bash
$ git commit -m "TST: Add test"

# OUTPUT:
# ════════════════════════════════════════════════════════════
# ⚡ REMINDER: Did you run pr-verify?
# ════════════════════════════════════════════════════════════
#
# Quick checks before commit:
#   ✓ pr-verify --verbose      (Full verification)
#   ✓ pr-quick                 (Quick check only)
#   ✓ pr-fix && pr-quick       (Fix issues and re-verify)
#
# ...continues with commit...
```

### To customize:
Edit `.git/hooks/prepare-commit-msg` or `.git/hooks/pre-push`

---

## ⏰ Option 2: Scheduled Reminders (Cron)

### Setup (macOS):

```bash
# 1. Create reminder script
cat > ~/scripts/pr-verify-reminder.sh << 'EOF'
#!/bin/bash
osascript -e 'display notification "Run pr-verify before git operations!" with title "pandas PR Reminder"'
EOF

chmod +x ~/scripts/pr-verify-reminder.sh

# 2. Add to crontab (runs every hour)
crontab -e

# Add line:
# 0 * * * * /Users/logio/scripts/pr-verify-reminder.sh

# 3. Test it
/Users/logio/scripts/pr-verify-reminder.sh
```

### Setup (Linux):

```bash
# Use notify-send instead
cat > ~/scripts/pr-verify-reminder.sh << 'EOF'
#!/bin/bash
notify-send "pandas PR Reminder" "Run pr-verify before git operations!"
EOF

chmod +x ~/scripts/pr-verify-reminder.sh

# Add to crontab:
# 0 * * * * /home/logio/scripts/pr-verify-reminder.sh
```

---

## 🔔 Option 3: System Notifications

### macOS Notification Center:

```bash
# One-liner to send notification
osascript -e 'display notification "Run pr-verify!" with title "Pandas Reminder"'

# Or create an alias
alias pr-remind='osascript -e "display notification \"Run pr-verify before git!\" with title \"Pandas\""'

# Use:
pr-remind
```

### Create a persistent reminder:

```bash
# Add to ~/.zshrc
function pr-remind-loop() {
    while true; do
        sleep 3600  # Every hour
        osascript -e 'display notification "Run pr-verify before git operations!" with title "Pandas Reminder"'
    done &
}

# Start it:
pr-remind-loop
```

---

## 📱 Option 4: Desktop Popup Reminders

### Using Alfred (macOS):

```
1. Open Alfred
2. Create Workflow
3. Add trigger: "Hotkey" (e.g., Cmd+Opt+P)
4. Add action: "Run Script"
5. Script:
   osascript << EOF
   display notification "Run pr-verify!" with title "Pandas PR"
   EOF
6. Done!
```

### Using Automator (macOS):

```
1. Open Automator
2. New → Quick Action
3. Add: Run Shell Script
4. Script:
   osascript -e 'display notification "Run pr-verify!" with title "Pandas PR"'
5. Save as: pr-verify-reminder
6. Assign Hotkey in System Preferences
```

---

## 🖥️ Option 5: Terminal Watch (While Working)

### Live reminder in terminal:

```bash
# Watch for changes and remind
watch -n 300 'echo "⏰ Run pr-verify before committing!"; date'

# Or in background
while true; do
    sleep 1800  # Every 30 min
    echo "⏰ REMINDER: Use pr-verify!"
done &
```

### Add to ~/.zshrc:

```bash
# Auto-start reminder when in pandas repo
function cd() {
    builtin cd "$@"
    if [[ $PWD == *"/pandas"* ]]; then
        echo "📝 Tip: Remember to run pr-verify before git operations!"
        echo "   Quick: pr-quick | Full: pr-verify --verbose | Auto-fix: pr-fix"
    fi
}
```

---

## 📧 Option 6: Email Reminders

### Using terminal-notifier (macOS):

```bash
# Install
brew install terminal-notifier

# Create script
cat > ~/scripts/pr-email-reminder.sh << 'EOF'
#!/bin/bash
terminal-notifier \
    -title "Pandas PR Reminder" \
    -subtitle "Before Git Operations" \
    -message "Run: pr-verify --verbose" \
    -open "https://github.com/pandas-dev/pandas"
EOF

chmod +x ~/scripts/pr-email-reminder.sh

# Add to crontab:
# 0 9 * * 1-5 /Users/logio/scripts/pr-email-reminder.sh
```

---

## 🎯 Option 7: IDE Notifications (VSCode/Claude Code)

### VSCode Task Reminders:

Create `.vscode/tasks.json`:
```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "pr-verify Reminder",
      "type": "shell",
      "command": "echo",
      "args": ["💡 Did you run pr-verify?"],
      "presentation": {
        "reveal": "always",
        "panel": "new"
      }
    }
  ]
}
```

Then in your workflow:
```bash
# Before commit, press Cmd+Shift+B to run task
# Shows reminder
```

---

## ✨ Option 8: Zsh Prompt Integration

Add to ~/.zshrc:

```bash
# Show pr-verify reminder in prompt
PROMPT='$(pr_verify_reminder)%F{blue}➜%f '

pr_verify_reminder() {
    if [[ $PWD == *"/pandas"* ]]; then
        echo -n "%F{yellow}[pr-verify?]%f "
    fi
}
```

---

## 🎨 Option 9: Custom Banner

Add to ~/.zshrc:

```bash
# Show banner when entering pandas directory
cd() {
    builtin cd "$@"
    if [[ $PWD == *"/pandas"* ]]; then
        cat << 'EOF'
╔═══════════════════════════════════════════════════════════╗
║  Welcome to pandas repo!                                  ║
║                                                           ║
║  Remember to use pr-verify:                              ║
║    • After modifying tests: pr-verify --verbose          ║
║    • Before commit: pr-quick                             ║
║    • Before push: pr-check                               ║
║    • Before PR: pr-report FILE                           ║
║                                                           ║
║  Quick command: pr-help-all                              ║
╚═══════════════════════════════════════════════════════════╝
EOF
    fi
}
```

---

## 🤖 Option 10: Claude Code Integration

Since you use Claude Code, I will:
1. ✅ **Remember to ask you** about pr-verify in my responses
2. ✅ **Suggest commands** when you mention pandas PRs
3. ✅ **Remind in conversation** - Like this one! 😊

I've saved this to my memory:
```
💾 Saved: "User wants reminders to use pr-verify"
💾 Saved: "Always suggest pr-verify when working on pandas"
💾 Saved: "Use pr-verify BEFORE every git operation"
```

Now I'll:
- 🔔 Remind you in chat when discussing pandas
- 📝 Suggest commands proactively
- ✅ Check if you've used pr-verify

---

## 🎯 RECOMMENDED SETUP

### For your workflow:

```bash
# 1. Git hooks (automatic, already installed!)
#    ✓ Remind on git commit
#    ✓ Remind on git push

# 2. Zsh prompt (add to ~/.zshrc)
PROMPT='[pr-verify?] %F{blue}➜%f '  # Shows reminder in prompt

# 3. Claude Code
#    ✓ I'll remind you in responses
#    ✓ You'll see suggestions for pr-verify

# 4. Desktop notification (optional)
#    Every 30 min: osascript reminder
```

---

## ✅ Quick Setup (Copy-Paste)

### Add to ~/.zshrc:

```bash
# pr-verify reminders
function cd() {
    builtin cd "$@"
    if [[ $PWD == *"/pandas"* ]]; then
        echo "💡 Reminder: Use pr-verify before git operations!"
        echo "   pr-verify --verbose  or  pr-quick"
    fi
}

# Optional: Every hour reminder
# pr-remind-loop() {
#     while true; do
#         sleep 3600
#         osascript -e 'display notification "Run pr-verify!" with title "Pandas"'
#     done &
# }
# pr-remind-loop  # Uncomment to enable
```

---

## 🔍 Verify Reminders Are Working

```bash
# Test git hook
cd /Users/logio/pandas
git commit --allow-empty -m "test"
# Should show reminder ✓

# Test zsh prompt
cat ~/.zshrc | grep "pr-verify"
# Should show your reminder ✓

# Check my memory
# I will remember to ask: "Did you use pr-verify?"
```

---

## 📊 Summary: How You'll Be Reminded

| When | How | Method |
|------|-----|--------|
| Making changes | I'll suggest it | Claude Code chat |
| Before commit | Automatic pop-up | Git hook |
| Before push | Automatic pop-up | Git hook |
| In prompt | Every time | Zsh integration |
| Hourly (optional) | Notification | Cron + osascript |

---

## 💬 From Now On...

Whenever you mention:
- "I'm working on a pandas PR"
- "Need to test my changes"
- "About to commit/push"
- Any pandas contribution

I will automatically respond with:
```
🔔 Reminder: Have you run pr-verify?

Quick commands:
  pr-verify --verbose    # Full check
  pr-quick              # Fast check
  pr-fix                # Auto-fix
  pr-check              # Before push
```

---

## 🎉 You're All Set!

Now you have:
✅ Git hook reminders (automatic)
✅ Zsh prompt reminders (if set up)
✅ Claude Code reminders (I'll do this!)
✅ Optional notifications (cron/osascript)

**You won't forget to use pr-verify again!** 🚀

---

**Status:** ✅ READY
**Reminders:** 🔔 ACTIVE
**Your feedback:** 💙 Appreciated!

If you want to add more reminders, just ask! 📝
