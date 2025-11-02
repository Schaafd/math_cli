#!/bin/bash
#
# run.sh - Build and run MathCLI iOS app in simulator
#
# Usage: ./scripts/run.sh [device_name]
#   device_name: iPhone 15 (default), iPad Pro, etc.
#

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
DEVICE_NAME="${1:-iPhone 15}"
CONFIGURATION="Debug"

# Project settings
PROJECT_NAME="MathCLI"
SCHEME_NAME="MathCLI"
PROJECT_FILE="MathCLI.xcodeproj"
BUNDLE_ID="com.mathcli.MathCLI"  # Update this to match your bundle ID

# Check if project file exists
if [ ! -d "$PROJECT_FILE" ]; then
    echo -e "${RED}Error: $PROJECT_FILE not found!${NC}"
    echo -e "${YELLOW}Please create the Xcode project first.${NC}"
    exit 1
fi

echo -e "${GREEN}MathCLI iOS Runner${NC}"
echo -e "${YELLOW}Device:${NC} $DEVICE_NAME"
echo ""

# Step 1: Boot simulator if needed
echo -e "${BLUE}Step 1: Starting simulator...${NC}"
DEVICE_UDID=$(xcrun simctl list devices | grep "$DEVICE_NAME" | grep -v "unavailable" | head -1 | sed -E 's/.*\(([0-9A-F-]+)\).*/\1/')

if [ -z "$DEVICE_UDID" ]; then
    echo -e "${RED}Error: Device '$DEVICE_NAME' not found!${NC}"
    echo ""
    echo -e "${YELLOW}Available simulators:${NC}"
    xcrun simctl list devices | grep "iPhone\|iPad" | grep -v "unavailable"
    exit 1
fi

echo -e "${GREEN}Found device: $DEVICE_UDID${NC}"

# Boot the simulator
xcrun simctl boot "$DEVICE_UDID" 2>/dev/null || true
open -a Simulator

# Wait for simulator to boot
echo "Waiting for simulator to boot..."
xcrun simctl bootstatus "$DEVICE_UDID" -b

echo ""

# Step 2: Build the app
echo -e "${BLUE}Step 2: Building app...${NC}"
xcodebuild \
    -project "$PROJECT_FILE" \
    -scheme "$SCHEME_NAME" \
    -configuration "$CONFIGURATION" \
    -destination "platform=iOS Simulator,id=$DEVICE_UDID" \
    -derivedDataPath "./build" \
    build \
    | xcpretty 2>/dev/null || xcodebuild \
    -project "$PROJECT_FILE" \
    -scheme "$SCHEME_NAME" \
    -configuration "$CONFIGURATION" \
    -destination "platform=iOS Simulator,id=$DEVICE_UDID" \
    -derivedDataPath "./build" \
    build

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Build failed!${NC}"
    exit 1
fi

echo ""

# Step 3: Find the built app
echo -e "${BLUE}Step 3: Installing app...${NC}"
APP_PATH=$(find ./build/Build/Products/$CONFIGURATION-iphonesimulator -name "*.app" -type d | head -1)

if [ -z "$APP_PATH" ]; then
    echo -e "${RED}Error: Could not find built app!${NC}"
    exit 1
fi

echo -e "${GREEN}Found app: $APP_PATH${NC}"

# Uninstall old version if exists
xcrun simctl uninstall "$DEVICE_UDID" "$BUNDLE_ID" 2>/dev/null || true

# Install the app
xcrun simctl install "$DEVICE_UDID" "$APP_PATH"

echo ""

# Step 4: Launch the app
echo -e "${BLUE}Step 4: Launching app...${NC}"
xcrun simctl launch "$DEVICE_UDID" "$BUNDLE_ID"

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✅ App launched successfully!${NC}"
    echo -e "${YELLOW}Check the Simulator for the running app.${NC}"
    exit 0
else
    echo ""
    echo -e "${RED}❌ Failed to launch app!${NC}"
    exit 1
fi
