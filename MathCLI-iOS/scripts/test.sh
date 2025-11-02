#!/bin/bash
#
# test.sh - Run tests for MathCLI iOS app from command line
#
# Usage: ./scripts/test.sh [destination]
#   destination: simulator (default), or specific destination
#

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
DESTINATION_TYPE="${1:-simulator}"

# Project settings
PROJECT_NAME="MathCLI"
SCHEME_NAME="MathCLI"
PROJECT_FILE="MathCLI.xcodeproj"

# Check if project file exists
if [ ! -d "$PROJECT_FILE" ]; then
    echo -e "${RED}Error: $PROJECT_FILE not found!${NC}"
    echo -e "${YELLOW}Please create the Xcode project first.${NC}"
    exit 1
fi

# Set destination
case "$DESTINATION_TYPE" in
    "simulator"|"sim")
        DESTINATION="platform=iOS Simulator,name=iPhone 15,OS=latest"
        echo -e "${GREEN}Running tests on iOS Simulator...${NC}"
        ;;
    *)
        DESTINATION="$DESTINATION_TYPE"
        echo -e "${GREEN}Running tests on: $DESTINATION${NC}"
        ;;
esac

echo ""

# Run tests
echo -e "${BLUE}Starting test run...${NC}"
xcodebuild test \
    -project "$PROJECT_FILE" \
    -scheme "$SCHEME_NAME" \
    -destination "$DESTINATION" \
    -enableCodeCoverage YES \
    | xcpretty --test --color 2>/dev/null || xcodebuild test \
    -project "$PROJECT_FILE" \
    -scheme "$SCHEME_NAME" \
    -destination "$DESTINATION" \
    -enableCodeCoverage YES

# Check test result
if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✅ All tests passed!${NC}"
    echo -e "${YELLOW}Test results are in:${NC} DerivedData/"

    # Show code coverage summary if available
    if command -v xcov &> /dev/null; then
        echo ""
        echo -e "${BLUE}Code Coverage Summary:${NC}"
        xcov --scheme "$SCHEME_NAME" --project "$PROJECT_FILE"
    fi

    exit 0
else
    echo ""
    echo -e "${RED}❌ Tests failed!${NC}"
    exit 1
fi
