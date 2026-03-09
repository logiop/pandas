#!/bin/bash
# Setup script for pr-verify integration
# Add to your ~/.zshrc or ~/.bashrc

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

PANDAS_PATH="/Users/logio/pandas"

# ============================================================================
# ALIAS DEFINITIONS
# ============================================================================

# Quick verification alias
alias pr-verify='$PANDAS_PATH/pr-verify'

# Convenience aliases
alias pr-verify-quick='pr-verify --quick --verbose'
alias pr-verify-json='pr-verify --json'
alias pr-verify-ci='pr-verify --ci'
alias pr-verify-fix='pr-verify --fix --verbose'

# Test-specific aliases
alias pr-test-array='pytest $PANDAS_PATH/pandas/tests/arrays/test_array.py -xvs'
alias pr-test-astype='pytest $PANDAS_PATH/pandas/tests/series/methods/test_astype.py -xvs'
alias pr-test-all='pr-verify && pytest $PANDAS_PATH/pandas/tests/arrays/test_array.py -v'

# Documentation aliases
alias pr-docs='cat $PANDAS_PATH/PR_VERIFICATION_GUIDE.md | less'
alias pr-readme='cat $PANDAS_PATH/VERIFICATION_TOOLS_README.md | less'
alias pr-help='pr-verify --help'

# ============================================================================
# BASH FUNCTIONS
# ============================================================================

# Main verification function
pr-check() {
    """Comprehensive PR check with all steps"""
    local verbose=${1:-""}

    echo -e "${BLUE}=== PR Verification Suite ===${NC}"
    echo ""

    # 1. Verify syntax
    echo -e "${YELLOW}1. Checking Python syntax...${NC}"
    pr-verify ${verbose} || {
        echo -e "${RED}✗ Verification failed${NC}"
        return 1
    }
    echo -e "${GREEN}✓ Syntax OK${NC}"

    # 2. Pre-commit hooks
    echo ""
    echo -e "${YELLOW}2. Running pre-commit hooks...${NC}"
    cd "$PANDAS_PATH"
    pre-commit run --all-files || {
        echo -e "${RED}✗ Pre-commit failed${NC}"
        return 1
    }
    echo -e "${GREEN}✓ Pre-commit OK${NC}"

    # 3. Run tests
    echo ""
    echo -e "${YELLOW}3. Running tests...${NC}"
    pytest "$PANDAS_PATH/pandas/tests/arrays/test_array.py" -v || {
        echo -e "${RED}✗ Tests failed${NC}"
        return 1
    }
    echo -e "${GREEN}✓ Tests OK${NC}"

    echo ""
    echo -e "${GREEN}=== ALL CHECKS PASSED ===${NC}"
    return 0
}

# Quick PR check (no tests)
pr-quick() {
    """Quick verification (syntax + pre-commit only)"""
    echo -e "${BLUE}=== Quick PR Check ===${NC}"

    pr-verify --quick --verbose && \
    cd "$PANDAS_PATH" && \
    pre-commit run --all-files && \
    echo -e "${GREEN}✓ Quick check passed${NC}" || \
    echo -e "${RED}✗ Quick check failed${NC}"
}

# Generate PR report
pr-report() {
    """Generate comprehensive PR report"""
    local output_file="${1:-pr_report.json}"

    echo -e "${BLUE}Generating PR report...${NC}"
    pr-verify --json > "$output_file"

    if [ -f "$output_file" ]; then
        echo -e "${GREEN}✓ Report saved to: $output_file${NC}"
        echo ""
        echo "Summary:"
        cat "$output_file" | jq '{
            total_issues: .total_issues,
            errors: .errors,
            warnings: .warnings,
            passed_checks: (.passed_checks | length),
            failed_checks: (.failed_checks | length)
        }'
    else
        echo -e "${RED}✗ Failed to generate report${NC}"
        return 1
    fi
}

# Run specific test
pr-test() {
    """Run specific test function"""
    local test_path="${1:-pandas/tests/arrays/test_array.py}"
    local test_func="${2:-}"

    if [ -z "$test_func" ]; then
        pytest "$PANDAS_PATH/$test_path" -xvs
    else
        pytest "$PANDAS_PATH/$test_path::$test_func" -xvs
    fi
}

# Fix common issues
pr-fix() {
    """Attempt to fix common issues"""
    echo -e "${YELLOW}Attempting to fix common issues...${NC}"

    cd "$PANDAS_PATH"

    # Run formatters
    echo "Running ruff format..."
    ruff format pandas/tests/ || true

    # Run isort
    echo "Running isort..."
    isort pandas/tests/ || true

    # Run pre-commit with fix
    echo "Running pre-commit --fix..."
    pre-commit run --all-files --fix || true

    echo -e "${GREEN}✓ Fixes applied (verify with pr-verify)${NC}"
}

# Show PR status
pr-status() {
    """Show current PR verification status"""
    echo -e "${BLUE}=== PR Status ===${NC}"
    echo ""

    # Get last report if exists
    if [ -f "pr_report.json" ]; then
        echo "Last Report:"
        jq '{
            timestamp: .timestamp,
            total_files: .total_files_checked,
            issues: .total_issues,
            errors: .errors,
            warnings: .warnings
        }' pr_report.json
    else
        echo "Run 'pr-report' to generate status report"
    fi
}

# Open PR documentation
pr-docs-open() {
    """Open PR documentation in editor"""
    local editor="${EDITOR:-nano}"

    echo "Opening documentation..."

    case "$1" in
        "guide")
            $editor "$PANDAS_PATH/PR_VERIFICATION_GUIDE.md"
            ;;
        "readme")
            $editor "$PANDAS_PATH/VERIFICATION_TOOLS_README.md"
            ;;
        *)
            echo "Usage: pr-docs-open [guide|readme]"
            return 1
            ;;
    esac
}

# ============================================================================
# AUTO-COMPLETION
# ============================================================================

# Bash completion for pr-verify
_pr_verify_completion() {
    local cur="${COMP_WORDS[COMP_CWORD]}"
    local prev="${COMP_WORDS[COMP_CWORD-1]}"

    local options="--help --verbose --json --fix --report --python --quick --ci --file --dir"

    case "$prev" in
        --file|--dir|--report)
            # Suggest files
            COMPREPLY=($(compgen -f -- "$cur"))
            ;;
        --python)
            COMPREPLY=($(compgen -W "3.11 3.12" -- "$cur"))
            ;;
        *)
            COMPREPLY=($(compgen -W "$options" -- "$cur"))
            ;;
    esac
}

# Register completion if bash-completion is available
if command -v complete &> /dev/null; then
    complete -o bashdefault -o default -o nospace -F _pr_verify_completion pr-verify
fi

# ============================================================================
# ZSHRC SPECIFIC (if using zsh)
# ============================================================================

if [ -n "$ZSH_VERSION" ]; then
    # Create completion for zsh
    _pr_verify() {
        local -a options
        options=(
            '--help[Show help]'
            '--verbose[Verbose output]'
            '--json[JSON output]'
            '--fix[Attempt to fix issues]'
            '--report[Save report to file]'
            '--quick[Quick mode]'
            '--ci[CI mode]'
            '--file[Check specific file]'
            '--dir[Check specific directory]'
        )
        _arguments $options
    }

    compdef _pr_verify pr-verify
fi

# ============================================================================
# HELPER: Show all pr-* commands
# ============================================================================

pr-help-all() {
    """Show all available pr-* commands"""
    echo -e "${BLUE}=== Available pr-verify Commands ===${NC}"
    echo ""
    echo -e "${YELLOW}Direct Aliases:${NC}"
    echo "  pr-verify           - Run full verification"
    echo "  pr-verify-quick     - Quick verification (no tests)"
    echo "  pr-verify-json      - JSON output"
    echo "  pr-verify-ci        - CI mode"
    echo "  pr-verify-fix       - Auto-fix issues"
    echo ""
    echo -e "${YELLOW}Convenience Functions:${NC}"
    echo "  pr-check [--verbose]     - Full check (verify + pre-commit + tests)"
    echo "  pr-quick                 - Quick check (verify + pre-commit)"
    echo "  pr-report [FILE]         - Generate comprehensive report"
    echo "  pr-test [PATH] [FUNC]    - Run specific test"
    echo "  pr-fix                   - Attempt to auto-fix issues"
    echo "  pr-status                - Show PR status"
    echo "  pr-docs-open [guide|readme] - Open documentation"
    echo ""
    echo -e "${YELLOW}Test Aliases:${NC}"
    echo "  pr-test-array       - Run array tests"
    echo "  pr-test-astype      - Run astype tests"
    echo "  pr-test-all         - Verify + run array tests"
    echo ""
    echo -e "${YELLOW}Documentation:${NC}"
    echo "  pr-docs             - View PR Verification Guide"
    echo "  pr-readme           - View Tools Readme"
    echo "  pr-help             - Show pr-verify help"
    echo ""
    echo -e "${YELLOW}Example Workflow:${NC}"
    echo "  1. pr-verify                    # Check everything"
    echo "  2. pr-fix                       # Fix common issues"
    echo "  3. pr-quick                     # Quick verification"
    echo "  4. pr-test-array                # Run tests"
    echo "  5. pr-report pr_final.json      # Generate report"
    echo ""
}

# ============================================================================
# INSTALLATION INSTRUCTIONS
# ============================================================================

if [ "$1" = "--install" ]; then
    echo -e "${GREEN}Installing pr-verify integration...${NC}"

    # Detect shell
    if [ -n "$ZSH_VERSION" ]; then
        shell_rc="$HOME/.zshrc"
    else
        shell_rc="$HOME/.bashrc"
    fi

    # Add source line if not already present
    if ! grep -q "source.*setup-pr-verify" "$shell_rc" 2>/dev/null; then
        echo "" >> "$shell_rc"
        echo "# pr-verify integration" >> "$shell_rc"
        echo "source $PANDAS_PATH/.setup-pr-verify.sh" >> "$shell_rc"
        echo -e "${GREEN}✓ Added to $shell_rc${NC}"
    else
        echo -e "${YELLOW}✓ Already installed in $shell_rc${NC}"
    fi

    # Make script executable
    chmod +x "$PANDAS_PATH/pr-verify"
    echo -e "${GREEN}✓ pr-verify made executable${NC}"

    echo ""
    echo -e "${GREEN}Installation complete!${NC}"
    echo "Run: source $shell_rc"
    echo "Then: pr-help-all"
    exit 0
fi

# Show help if requested
if [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
    cat << EOF
$0 - Setup script for pr-verify integration

Usage:
    source $0                  # Load in current shell
    source $0 --install        # Install for future sessions
    source $0 --help          # Show this help

After loading, available commands:
    pr-help-all              # Show all pr-* commands
    pr-verify                # Run verification
    pr-quick                 # Quick check
    pr-check                 # Full check with tests
    pr-report                # Generate report
    pr-test                  # Run specific test
    pr-fix                   # Auto-fix issues
    pr-status                # Show status

EOF
    exit 0
fi

# Auto-run installation hint
echo -e "${GREEN}pr-verify integration loaded!${NC}"
echo -e "${YELLOW}Type 'pr-help-all' to see all commands${NC}"
echo -e "${YELLOW}Or run: source $0 --install${NC}"
