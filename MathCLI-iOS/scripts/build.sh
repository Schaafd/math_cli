#!/bin/bash
#
# build.sh - Build MathCLI iOS app from command line
#
# Usage: ./scripts/build.sh [configuration] [destination]
#   configuration: Debug (default) or Release
#   destination: simulator (default), device, or specific destination
#

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
CONFIGURATION="${1:-Debug}"
DESTINATION_TYPE="${2:-simulator}"

# Project settings
PROJECT_NAME="MathCLI"
SCHEME_NAME="MathCLI"
PROJECT_FILE="MathCLI.xcodeproj"

# Check if project file exists
if [ ! -d "$PROJECT_FILE" ]; then
    echo -e "${RED}Error: $PROJECT_FILE not found!${NC}"
    echo -e "${YELLOW}Please create the Xcode project first.${NC}"
    echo "Run this from the project root directory."
    exit 1
fi

# Set destination based on type
case "$DESTINATION_TYPE" in
    "simulator"|"sim")
        DESTINATION="platform=iOS Simulator,name=iPhone 15,OS=latest"
        echo -e "${GREEN}Building for iOS Simulator...${NC}"
        ;;
    "device")
        DESTINATION="generic/platform=iOS"
        echo -e "${GREEN}Building for iOS Device...${NC}"
        ;;
    *)
        DESTINATION="$DESTINATION_TYPE"
        echo -e "${GREEN}Building for custom destination: $DESTINATION${NC}"
        ;;
esac

echo -e "${YELLOW}Configuration:${NC} $CONFIGURATION"
echo -e "${YELLOW}Destination:${NC} $DESTINATION"
echo ""

# Build the project
echo -e "${GREEN}Starting build...${NC}"
xcodebuild \
    -project "$PROJECT_FILE" \
    -scheme "$SCHEME_NAME" \
    -configuration "$CONFIGURATION" \
    -destination "$DESTINATION" \
    clean build \
    | xcpretty 2>/dev/null || xcodebuild \
    -project "$PROJECT_FILE" \
    -scheme "$SCHEME_NAME" \
    -configuration "$CONFIGURATION" \
    -destination "$DESTINATION" \
    clean build

# Check build result
if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✅ Build succeeded!${NC}"
    echo -e "${YELLOW}Build artifacts are in:${NC} build/$CONFIGURATION-iphonesimulator/"
    exit 0
else
    echo ""
    echo -e "${RED}❌ Build failed!${NC}"
    exit 1
fi
