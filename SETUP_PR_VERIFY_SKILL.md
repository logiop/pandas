# Setup pr-verify as a Skill-like Command

**Quick integration guide for pr-verify verification tool**

---

## 🚀 Quick Start (2 minutes)

```bash
# 1. Source the setup script
source /Users/logio/pandas/.setup-pr-verify.sh --install

# 2. Reload shell
source ~/.zshrc  # or ~/.bashrc

# 3. Test it
pr-verify --help
pr-help-all
```

---

## 📋 What Gets Installed

### Aliases (Quick commands)
```bash
pr-verify              # Main verification command
pr-verify-quick        # Fast check (no tests)
pr-verify-json         # JSON output
pr-verify-ci           # CI mode
pr-verify-fix          # Auto-fix issues
pr-test-array          # Test array module
pr-test-astype         # Test astype
pr-docs                # View docs
```

### Functions (Advanced commands)
```bash
pr-check [--verbose]   # Full check (verify + pre-commit + tests)
pr-quick               # Quick check
pr-report [FILE]       # Generate report
pr-test [PATH] [FUNC]  # Run specific test
pr-fix                 # Auto-fix issues
pr-status              # Show status
pr-docs-open [type]    # Open documentation
pr-help-all            # Show all commands
```

### Auto-completion
- Tab completion for all pr-verify options
- Works in bash and zsh

---

## 📦 Installation Methods

### Method 1: Manual Setup (Recommended for first time)

```bash
# Step 1: Add to ~/.zshrc (or ~/.bashrc)
echo "" >> ~/.zshrc
echo "# pr-verify integration" >> ~/.zshrc
echo "source /Users/logio/pandas/.setup-pr-verify.sh" >> ~/.zshrc

# Step 2: Reload shell
source ~/.zshrc

# Step 3: Verify
pr-verify --help
```

### Method 2: Automated Setup

```bash
# One-liner installation
source /Users/logio/pandas/.setup-pr-verify.sh --install

# Reload
source ~/.zshrc
```

### Method 3: Add to ~/.zprofile (permanent)

```bash
# For zsh users - add to ~/.zprofile for all new terminals
cat >> ~/.zprofile << 'EOF'
# pr-verify skill integration
if [ -f /Users/logio/pandas/.setup-pr-verify.sh ]; then
    source /Users/logio/pandas/.setup-pr-verify.sh
fi
EOF

# Reload
source ~/.zprofile
```

---

## 🎯 Usage Examples

### Basic Verification
```bash
# Full check
pr-verify

# Verbose output
pr-verify --verbose

# JSON format (for CI)
pr-verify --json > report.json

# Quick check
pr-verify-quick
```

### Advanced Usage
```bash
# Full workflow
pr-check --verbose

# Auto-fix issues
pr-fix

# Generate report
pr-report pr_final.json

# Run specific test
pr-test pandas/tests/arrays/test_array.py test_array_str_dtype_preserves_na

# Show status
pr-status
```

### For Your Current PR
```bash
# 1. Verify
pr-verify --verbose

# 2. Fix issues
pr-fix

# 3. Quick check again
pr-quick

# 4. Run tests
pr-test-array

# 5. Generate final report
pr-report final_report.json
```

---

## 🔧 Configuration

### Customize aliases

Edit `~/.zshrc`:
```bash
# Change any alias
alias pr-verify='python /Users/logio/pandas/verify_pr.py --verbose'

# Add new aliases
alias pr-my-command='pr-verify --quick'
```

### Change default behavior

Edit `/Users/logio/pandas/.setup-pr-verify.sh`:
```bash
# Line 35 - Change PANDAS_PATH
PANDAS_PATH="/path/to/your/pandas"

# Line ~180 - Customize pr-check function
pr-check() {
    # Add custom steps here
}
```

---

## 🐚 Shell Integration

### For Zsh (.zshrc)

```bash
# Add this line to ~/.zshrc
source /Users/logio/pandas/.setup-pr-verify.sh

# Optional: customize prompt to show status
PROMPT='%F{blue}pr-verify%f $ '
```

### For Bash (.bashrc)

```bash
# Add this line to ~/.bashrc
source /Users/logio/pandas/.setup-pr-verify.sh

# Optional: alias to favorite shell
alias verify='pr-verify'
```

### For Fish Shell

Create `~/.config/fish/conf.d/pr-verify.fish`:
```fish
# Fish shell integration
set -gx PANDAS_PATH /Users/logio/pandas

# Aliases
alias pr-verify "$PANDAS_PATH/pr-verify"
alias pr-quick "pr-verify --quick --verbose"

# Functions
function pr-check
    echo "Running PR check..."
    pr-verify --verbose
    and echo "✓ Check passed"
end
```

---

## 🎓 Learning Commands

### Get Help
```bash
pr-help           # Show pr-verify help
pr-help-all       # Show all commands
pr-docs           # View full guide
pr-readme         # View tools readme
pr-docs-open guide # Open in editor
```

### View Commands
```bash
# List all aliases
compgen -c | grep '^pr-'

# List all functions
declare -f | grep '^pr_'

# Show completion options
pr-verify --help
```

---

## ✅ Verification Checklist

After installation:

- [ ] Script is executable: `ls -l /Users/logio/pandas/pr-verify`
- [ ] Setup script exists: `cat /Users/logio/pandas/.setup-pr-verify.sh`
- [ ] Shell config updated: `grep 'setup-pr-verify' ~/.zshrc`
- [ ] Shell reloaded: `source ~/.zshrc`
- [ ] Basic test works: `pr-verify --help`
- [ ] Alias works: `which pr-verify`
- [ ] Tab completion works: `pr-verify --<TAB>`

---

## 🚨 Troubleshooting

### Error: "command not found: pr-verify"

**Solution:**
```bash
# 1. Check if setup is sourced
cat ~/.zshrc | grep setup-pr-verify

# 2. Reload shell
source ~/.zshrc

# 3. Verify path
which pr-verify

# 4. Check file exists
ls -l /Users/logio/pandas/pr-verify
```

### Error: "Permission denied"

**Solution:**
```bash
# Make script executable
chmod +x /Users/logio/pandas/pr-verify

# Verify
ls -l /Users/logio/pandas/pr-verify
# Should show: -rwxr-xr-x
```

### Tab completion not working

**Solution:**
```bash
# For zsh
compdef _pr_verify pr-verify

# For bash
complete -F _pr_verify_completion pr-verify

# Reload
source ~/.zshrc  # or ~/.bashrc
```

### Wrong Python version

**Solution:**
```bash
# Check which Python is used
which python3

# Edit /Users/logio/pandas/pr-verify
# Change python3 to full path: /usr/bin/python3
# Or: python3.12
```

---

## 📊 Performance Tips

### Speed up verification
```bash
# Use quick mode (skip slow checks)
pr-verify-quick

# Or specify specific checks
pr-verify --file pandas/tests/arrays/test_array.py
```

### Run in background
```bash
# Run and get notification
pr-verify --json > report.json &
notify-send "PR Verification complete"

# Or with timeout
timeout 60 pr-verify --verbose
```

### Generate reports
```bash
# Save for later review
pr-report final_report.json

# View in pretty format
cat final_report.json | jq '.'
```

---

## 🔄 Integration with Other Tools

### Git Pre-commit Hook

Create `.git/hooks/pre-commit`:
```bash
#!/bin/bash
source /Users/logio/pandas/.setup-pr-verify.sh
pr-verify --quick || exit 1
```

Make executable:
```bash
chmod +x .git/hooks/pre-commit
```

### GitHub Actions

In your workflow:
```yaml
- name: Setup pr-verify
  run: |
    source /Users/logio/pandas/.setup-pr-verify.sh

- name: Run verification
  run: pr-verify --json > report.json
```

### Makefile

Add to `Makefile`:
```makefile
.PHONY: verify test pr-check

verify:
	pr-verify --verbose

test:
	pr-test-array

pr-check: verify test
	@echo "✅ All checks passed!"
```

Then use:
```bash
make verify
make pr-check
```

---

## 📝 Next Steps

1. **Install**: Run `source /Users/logio/pandas/.setup-pr-verify.sh --install`
2. **Reload**: Run `source ~/.zshrc`
3. **Verify**: Run `pr-help-all`
4. **Use**: Run `pr-verify --verbose`
5. **Learn**: Read `PR_VERIFICATION_GUIDE.md`

---

## 📚 Related Files

- `pr-verify` - Main executable script
- `.setup-pr-verify.sh` - Shell integration setup
- `verify_pr.py` - Core verification logic
- `PR_VERIFICATION_GUIDE.md` - Complete guide
- `VERIFICATION_TOOLS_README.md` - Tools reference

---

## 💡 Pro Tips

```bash
# 1. Chain commands for full workflow
pr-verify && pr-fix && pr-quick && pr-test-array

# 2. Use with pipe for advanced usage
pr-verify --json | jq '.issues[] | select(.severity=="ERROR")'

# 3. Create custom aliases in ~/.zshrc
alias my-verify='pr-verify --verbose --json | tee report.json'

# 4. Use with watch for live updates
watch -n 5 'pr-verify --quick'

# 5. Create a cron job for automated checks
# 0 9 * * 1 source ~/.zshrc && pr-verify --json >> verify.log
```

---

## ✨ Summary

You now have:
- ✅ Fast invocable command (`pr-verify`)
- ✅ 10+ convenience functions
- ✅ 8 quick aliases
- ✅ Auto-completion
- ✅ Documentation
- ✅ CI/CD integration
- ✅ Full control

**Start using it now!**

```bash
source /Users/logio/pandas/.setup-pr-verify.sh --install
pr-help-all
```

---

**Created**: 2026-03-09
**Version**: 1.0
**Status**: Production Ready ✅
