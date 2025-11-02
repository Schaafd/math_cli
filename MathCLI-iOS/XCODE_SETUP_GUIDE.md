# Xcode Project Setup Guide

This guide walks you through setting up the Math CLI iOS project in Xcode from the provided source files.

## Prerequisites

- macOS Sonoma 14.0 or later
- Xcode 15.0 or later
- Apple Developer Account (for device testing, optional for simulator)

## Step-by-Step Setup

### Step 1: Create New Xcode Project

1. **Launch Xcode**

2. **Create new project**:
   - Click "Create a new Xcode project" or File → New → Project
   - Select **iOS** platform
   - Choose **App** template
   - Click **Next**

3. **Configure project settings**:
   - **Product Name**: `MathCLI`
   - **Team**: Select your development team (or None for simulator only)
   - **Organization Identifier**: `com.yourname` (use your identifier)
   - **Bundle Identifier**: Will auto-generate as `com.yourname.MathCLI`
   - **Interface**: **SwiftUI**
   - **Storage**: **SwiftData** ⚠️ Important!
   - **Language**: **Swift**
   - **Include Tests**: Check this box
   - Click **Next**

4. **Choose location**:
   - Select where to save the project
   - **Do NOT check** "Create Git repository" (already exists)
   - Click **Create**

### Step 2: Configure Project Settings

1. **Set deployment target**:
   - Select project in navigator (blue MathCLI icon)
   - Select **MathCLI** target
   - Go to **General** tab
   - Set **Minimum Deployments** to **iOS 17.0**

2. **Configure app info**:
   - Display Name: `Math CLI`
   - Category: Utilities or Productivity
   - Supports multiple windows: No (for now)
   - Device Orientation: Portrait (recommended)

3. **Enable capabilities** (optional for Phase 1):
   - Go to **Signing & Capabilities** tab
   - Click **+ Capability**
   - Add **iCloud** (for future sync feature)
   - Check **CloudKit**

### Step 3: Organize Project Structure

1. **Delete default files**:
   - Right-click on `ContentView.swift` → Delete → Move to Trash
   - Right-click on `Item.swift` (if exists) → Delete → Move to Trash
   - Keep `MathCLIApp.swift` (we'll replace it)

2. **Create folder structure**:

   Right-click on **MathCLI** folder → **New Group** and create these groups:

   ```
   MathCLI
   ├── App
   ├── Core
   │   ├── Engine
   │   └── Operations
   │       ├── BasicArithmetic
   │       ├── Trigonometry
   │       ├── AdvancedMath
   │       ├── Statistics
   │       ├── ComplexNumbers
   │       ├── Matrix
   │       ├── Calculus
   │       ├── NumberTheory
   │       ├── Combinatorics
   │       ├── Geometry
   │       ├── Constants
   │       ├── Conversions
   │       ├── Variables
   │       ├── ControlFlow
   │       ├── UserFunctions
   │       ├── Scripts
   │       ├── DataAnalysis
   │       ├── DataTransform
   │       ├── Plotting
   │       └── Export
   ├── Variables
   ├── Functions
   ├── Features
   │   ├── Calculator
   │   ├── History
   │   ├── Settings
   │   └── DataAnalysis
   ├── Models
   ├── Services
   ├── UI
   │   ├── Components
   │   ├── Themes
   │   └── Styles
   └── Utils
   ```

### Step 4: Add Source Files

#### Option A: Drag and Drop (Easiest)

1. Open Finder and navigate to:
   ```
   /path/to/math_cli/MathCLI-iOS/Sources/
   ```

2. Drag files into Xcode groups:
   - **App/**: Drag `MathCLIApp.swift` into the **App** group
   - **Core/Engine/**: Drag `OperationRegistry.swift` and `OperationExecutor.swift` into **Engine**
   - **Core/Operations/**: Drag `MathOperation.swift` into **Operations**
   - **Core/Operations/BasicArithmetic/**: Drag `BasicArithmeticOperations.swift` into **BasicArithmetic**
   - **Core/Operations/Trigonometry/**: Drag `ExtendedTrigOperations.swift` into **Trigonometry**
   - **Core/Operations/AdvancedMath/**: Drag `AdvancedMathOperations.swift` into **AdvancedMath**
   - **Core/Operations/Statistics/**: Drag `StatisticsOperations.swift` into **Statistics**
   - **Variables/**: Drag `VariableStore.swift` into **Variables**
   - **Functions/**: Drag `FunctionRegistry.swift` into **Functions**
   - **Features/Calculator/**: Drag all calculator Swift files
   - **Features/History/**: Drag `HistoryView.swift`
   - **Features/Settings/**: Drag `SettingsView.swift`
   - **Models/**: Drag `HistoryEntry.swift`

3. **Important**: When the dialog appears:
   - ✅ Check "Copy items if needed"
   - ✅ Select "Create groups"
   - ✅ Add to target: MathCLI
   - Click **Finish**

#### Option B: Add Files Menu (More Control)

1. Right-click on each group (e.g., **App**)
2. Select **Add Files to "MathCLI"...**
3. Navigate to corresponding source folder
4. Select Swift files
5. Ensure:
   - ✅ "Copy items if needed" is checked
   - ✅ "Create groups" is selected
   - ✅ Target "MathCLI" is checked
6. Click **Add**

### Step 5: Verify Project Structure

Your Xcode navigator should look like this:

```
MathCLI
├── App
│   └── MathCLIApp.swift
├── Core
│   ├── Engine
│   │   ├── OperationRegistry.swift
│   │   └── OperationExecutor.swift
│   ├── Operations
│   │   ├── MathOperation.swift
│   │   ├── BasicArithmetic
│   │   │   └── BasicArithmeticOperations.swift
│   │   ├── Trigonometry
│   │   │   └── ExtendedTrigOperations.swift
│   │   ├── AdvancedMath
│   │   │   └── AdvancedMathOperations.swift
│   │   └── Statistics
│   │       └── StatisticsOperations.swift
│   ├── Variables
│   │   └── VariableStore.swift
│   └── Functions
│       └── FunctionRegistry.swift
├── Features
│   ├── Calculator
│   │   ├── CalculatorView.swift
│   │   ├── CalculatorViewModel.swift
│   │   └── OperationBrowserView.swift
│   ├── History
│   │   └── HistoryView.swift
│   └── Settings
│       └── SettingsView.swift
├── Models
│   └── HistoryEntry.swift
├── Services (empty for now)
├── UI (empty for now)
├── Utils (empty for now)
└── Assets.xcassets
```

### Step 6: Build the Project

1. **Select target device**:
   - Choose **iPhone 15 Pro** simulator (or any iOS 17+ simulator)
   - Or connect a physical device with iOS 17+

2. **Build the project**:
   - Press `Cmd + B` or Product → Build
   - Wait for compilation to complete

3. **Fix any errors**:
   - Most errors will be about missing imports or types
   - Ensure all files are in the correct groups
   - Check that SwiftData is imported where needed

### Step 7: Run the App

1. **Run the app**:
   - Press `Cmd + R` or Product → Run
   - The simulator will launch

2. **Test basic functionality**:
   - Type `add 5 10` and press return
   - Should see `15` as output
   - Try `help` to see commands
   - Navigate to History, Operations, and Settings tabs

### Common Build Errors and Fixes

#### Error: "Cannot find type 'HistoryEntry' in scope"

**Fix**: Ensure `HistoryEntry.swift` is in the Models group and added to the target.

#### Error: "Type 'HistoryManager' has no member 'addEntry'"

**Fix**: Check that `HistoryEntry.swift` includes the `HistoryManager` class definition.

#### Error: "Cannot find 'ModelContainer' in scope"

**Fix**: Add `import SwiftData` at the top of `MathCLIApp.swift`.

#### Error: "Ambiguous reference to member 'max'"

**Fix**: Check for naming conflicts in operation implementations. Use `Darwin.max` or specify the correct `max`.

#### Warning: "Immutable property will not be decoded"

**Fix**: This is expected for some computed properties. Can be ignored.

### Step 8: Test Key Features

#### Test 1: Basic Calculator
- Input: `add 5 10`
- Expected: `15`

#### Test 2: Variables
- Input: `set x 42`
- Input: `multiply $x 2`
- Expected: `84`

#### Test 3: Chain Operations
- Input: `add 10 20 | multiply 2 | sqrt`
- Expected: `7.745967`

#### Test 4: Statistics
- Input: `mean 10 20 30 40 50`
- Expected: `30`

#### Test 5: History
- Navigate to **History** tab
- Should see all previous calculations
- Swipe left to delete
- Swipe right to bookmark

#### Test 6: Operations Browser
- Navigate to **Operations** tab
- Browse categories
- Tap on operations to see details

### Step 9: Enable iCloud (Optional)

1. **Sign in with Apple ID**:
   - Xcode → Settings → Accounts
   - Add your Apple ID

2. **Enable iCloud capability**:
   - Select project → MathCLI target
   - Signing & Capabilities tab
   - Click **+ Capability**
   - Add **iCloud**
   - Check **CloudKit**

3. **Create CloudKit container**:
   - Container will be auto-created as `iCloud.com.yourname.MathCLI`
   - Or specify custom container

### Step 10: Add Remaining Operations

To complete the full 266 operations, follow these steps:

1. **Create operation files** for each category (see README.md for list)

2. **Follow the pattern**:
   ```swift
   struct YourOperation: MathOperation {
       static var name: String = "operation_name"
       static var arguments: [String] = ["arg1"]
       static var help: String = "Description"
       static var category: OperationCategory = .category

       static func execute(args: [Any]) throws -> OperationResult {
           let arg = try parseDouble(args[0], argumentName: "arg1")
           return .number(result)
       }
   }
   ```

3. **Register in `OperationRegistry.swift`**:
   ```swift
   register(YourOperation.self)
   ```

4. **Build and test** each operation

## Project Configuration

### Info.plist Additions

Add these if needed:

```xml
<key>UIApplicationSupportsIndirectInputEvents</key>
<true/>
<key>UILaunchScreen</key>
<dict/>
<key>UISupportedInterfaceOrientations</key>
<array>
    <string>UIInterfaceOrientationPortrait</string>
</array>
```

### Build Settings

Recommended settings:

- **Swift Language Version**: Swift 5.9
- **iOS Deployment Target**: 17.0
- **Build Active Architecture Only**: Yes (Debug)
- **Enable Testability**: Yes (Debug)

## Debugging Tips

### Enable Console Output

In Xcode:
- View → Debug Area → Activate Console (Cmd + Shift + Y)
- See print statements and errors

### Breakpoints

- Click line number to add breakpoint
- Run in debug mode
- Inspect variables when paused

### SwiftData Debugging

View SwiftData database:
- Open simulator
- Go to app documents directory
- Find `.sqlite` file
- Use DB Browser for SQLite

## Next Steps

1. ✅ Complete Phase 1 (Current)
2. 🚧 Implement remaining 219 operations
3. 🚧 Add iCloud sync
4. 🚧 Implement data analysis features
5. 🚧 Add plotting with Swift Charts
6. 🚧 Create widgets
7. 🚧 Build Mac app with Catalyst

## Resources

- [SwiftUI Documentation](https://developer.apple.com/documentation/swiftui)
- [SwiftData Documentation](https://developer.apple.com/documentation/swiftdata)
- [Swift Language Guide](https://docs.swift.org/swift-book/)
- [Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/)

## Troubleshooting

### Simulator Issues

**Problem**: Simulator won't launch
**Solution**:
```bash
# Reset simulator
xcrun simctl erase all
# Restart Xcode
```

### Build Errors

**Problem**: "Command CodeSign failed"
**Solution**: Go to Signing & Capabilities → Select "Automatically manage signing"

**Problem**: "Module not found"
**Solution**: Product → Clean Build Folder (Cmd + Shift + K), then rebuild

### Runtime Errors

**Problem**: App crashes on launch
**Solution**:
- Check console for error messages
- Ensure SwiftData model is properly configured
- Verify all view files are correctly imported

## Support

If you encounter issues:
1. Check the README.md
2. Review code comments
3. Consult Swift/SwiftUI documentation
4. File an issue on GitHub

## Success Checklist

- [ ] Xcode project created
- [ ] iOS 17.0 deployment target set
- [ ] All source files added to project
- [ ] Project builds without errors
- [ ] App runs in simulator
- [ ] Basic calculations work
- [ ] Variables work
- [ ] History persists
- [ ] All tabs functional
- [ ] Settings save correctly

Congratulations! Your Math CLI iOS app is now set up and ready for development! 🎉
