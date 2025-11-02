#!/bin/bash
#
# verify-setup.sh - Verify your MathCLI development environment is ready
#
# Usage: ./scripts/verify-setup.sh
#

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   MathCLI Setup Verification Tool    ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"
echo ""

ERRORS=0
WARNINGS=0

# Check 1: Xcode installed
echo -n "Checking Xcode... "
if command -v xcodebuild &> /dev/null; then
    XCODE_VERSION=$(xcodebuild -version | head -1)
    echo -e "${GREEN}✓${NC} $XCODE_VERSION"
else
    echo -e "${RED}✗ Not installed${NC}"
    echo "  Install from App Store or https://developer.apple.com/xcode/"
    ((ERRORS++))
fi

# Check 2: Xcode Command Line Tools
echo -n "Checking Command Line Tools... "
if xcode-select -p &> /dev/null; then
    CLT_PATH=$(xcode-select -p)
    echo -e "${GREEN}✓${NC} Installed at $CLT_PATH"
else
    echo -e "${RED}✗ Not installed${NC}"
    echo "  Run: xcode-select --install"
    ((ERRORS++))
fi

# Check 3: Swift version
echo -n "Checking Swift... "
if command -v swift &> /dev/null; then
    SWIFT_VERSION=$(swift --version | head -1)
    echo -e "${GREEN}✓${NC} $SWIFT_VERSION"
else
    echo -e "${RED}✗ Not found${NC}"
    ((ERRORS++))
fi

# Check 4: Git
echo -n "Checking Git... "
if command -v git &> /dev/null; then
    GIT_VERSION=$(git --version)
    echo -e "${GREEN}✓${NC} $GIT_VERSION"
else
    echo -e "${RED}✗ Not installed${NC}"
    ((ERRORS++))
fi

# Check 5: iOS Simulators
echo -n "Checking iOS Simulators... "
SIMULATOR_COUNT=$(xcrun simctl list devices | grep -c "iPhone\|iPad")
if [ "$SIMULATOR_COUNT" -gt 0 ]; then
    echo -e "${GREEN}✓${NC} Found $SIMULATOR_COUNT simulators"
else
    echo -e "${YELLOW}⚠${NC} No simulators found"
    echo "  Open Xcode → Window → Devices and Simulators to add"
    ((WARNINGS++))
fi

# Check 6: Project structure
echo -n "Checking project structure... "
if [ -d "Sources" ] && [ -d "Sources/Core" ]; then
    FILE_COUNT=$(find Sources -name "*.swift" | wc -l | tr -d ' ')
    echo -e "${GREEN}✓${NC} Found $FILE_COUNT Swift files"
else
    echo -e "${RED}✗ Sources directory not found${NC}"
    ((ERRORS++))
fi

# Check 7: Xcode project file
echo -n "Checking Xcode project... "
if [ -d "MathCLI.xcodeproj" ]; then
    echo -e "${GREEN}✓${NC} MathCLI.xcodeproj exists"
else
    echo -e "${YELLOW}⚠${NC} MathCLI.xcodeproj not found"
    echo "  You need to create the Xcode project first"
    echo "  See XCODE_SETUP_GUIDE.md for instructions"
    ((WARNINGS++))
fi

# Check 8: Scripts are executable
echo -n "Checking scripts... "
SCRIPT_COUNT=0
for script in scripts/*.sh; do
    if [ -x "$script" ]; then
        ((SCRIPT_COUNT++))
    fi
done
if [ $SCRIPT_COUNT -gt 0 ]; then
    echo -e "${GREEN}✓${NC} Found $SCRIPT_COUNT executable scripts"
else
    echo -e "${YELLOW}⚠${NC} Scripts not executable"
    echo "  Run: chmod +x scripts/*.sh"
    ((WARNINGS++))
fi

# Check 9: Package.swift
echo -n "Checking Swift Package... "
if [ -f "Package.swift" ]; then
    echo -e "${GREEN}✓${NC} Package.swift exists"
else
    echo -e "${YELLOW}⚠${NC} Package.swift not found"
    ((WARNINGS++))
fi

# Check 10: Optional tools
echo ""
echo -e "${BLUE}Optional Tools:${NC}"

echo -n "  xcpretty (prettier build output)... "
if command -v xcpretty &> /dev/null; then
    echo -e "${GREEN}✓${NC} Installed"
else
    echo -e "${YELLOW}⚠${NC} Not installed"
    echo "    Install with: gem install xcpretty"
fi

echo -n "  swiftlint (code linting)... "
if command -v swiftlint &> /dev/null; then
    echo -e "${GREEN}✓${NC} Installed"
else
    echo -e "${YELLOW}⚠${NC} Not installed"
    echo "    Install with: brew install swiftlint"
fi

echo -n "  fswatch (auto-rebuild)... "
if command -v fswatch &> /dev/null; then
    echo -e "${GREEN}✓${NC} Installed"
else
    echo -e "${YELLOW}⚠${NC} Not installed"
    echo "    Install with: brew install fswatch"
fi

# Summary
echo ""
echo -e "${BLUE}═══════════════════════════════════════${NC}"

if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "${GREEN}✅ All checks passed! You're ready to develop!${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. Read DEVELOPMENT_WORKFLOW.md"
    echo "  2. Try: ./scripts/build.sh"
    echo "  3. Try: swift run mathcli-tool"
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo -e "${YELLOW}⚠ Setup complete with $WARNINGS warning(s)${NC}"
    echo ""
    echo "You can continue, but consider fixing the warnings above."
    exit 0
else
    echo -e "${RED}❌ Setup incomplete: $ERRORS error(s), $WARNINGS warning(s)${NC}"
    echo ""
    echo "Please fix the errors above before continuing."
    exit 1
fi
