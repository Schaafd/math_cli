# MathCLI iOS Development Workflow

This guide explains how to develop MathCLI iOS primarily in Claude Code (or any text editor) while using Xcode only for compilation and iOS-specific tasks.

## Table of Contents

1. [Philosophy](#philosophy)
2. [Initial Setup](#initial-setup)
3. [Daily Workflow](#daily-workflow)
4. [Command-Line Tools](#command-line-tools)
5. [Testing Strategies](#testing-strategies)
6. [Git Workflow](#git-workflow)
7. [Troubleshooting](#troubleshooting)

---

## Philosophy

**Primary Editor: Claude Code (or VS Code, Vim, etc.)**
- Write all Swift code
- Leverage AI assistance for implementation
- Full control over code style and organization
- Use git for version control

**Xcode: Compilation & iOS Tasks Only**
- Build the app
- Run in simulator
- Debug with breakpoints
- Profile performance
- Submit to App Store

This workflow gives you:
✅ AI-assisted development in Claude Code
✅ Fast iteration without Xcode overhead
✅ Command-line automation
✅ CI/CD integration
✅ Better git history (no Xcode metadata noise)

---

## Initial Setup

### 1. Create Xcode Project (One-Time)

```bash
# Open Xcode
open -a Xcode

# In Xcode:
# 1. File → New → Project
# 2. Choose "iOS → App"
# 3. Product Name: MathCLI
# 4. Interface: SwiftUI
# 5. Language: Swift
# 6. Use SwiftData: Yes
# 7. Save location: /path/to/MathCLI-iOS
```

### 2. Add Source Files to Xcode (One-Time)

**IMPORTANT: Add files by reference, not by copying!**

```bash
# In Xcode:
# 1. Right-click on "MathCLI" in Project Navigator
# 2. Select "Add Files to MathCLI..."
# 3. Navigate to Sources/ folder
# 4. Select all Swift files
# 5. ⚠️ UNCHECK "Copy items if needed"
# 6. Check "Create groups"
# 7. Click "Add"
```

This ensures Xcode references your files, so edits in Claude Code are immediately visible in Xcode.

### 3. Configure Build Settings

In Xcode:
```
Target → MathCLI → Build Settings:
- iOS Deployment Target: 17.0
- Swift Language Version: 5.9
- Enable Testability: Yes (Debug only)
```

### 4. Verify Setup

```bash
# Build from command line
./scripts/build.sh

# Should succeed ✅
```

---

## Daily Workflow

### Morning Routine

```bash
# 1. Navigate to project
cd /path/to/MathCLI-iOS

# 2. Pull latest changes (if team project)
git pull origin main

# 3. Start Claude Code (or your editor)
claude-code .
# or: code .
# or: vim .
```

### Development Cycle

```bash
# 1. Edit code in Claude Code
# - Add new operations
# - Fix bugs
# - Update documentation
# - All in your preferred editor!

# 2. Save changes (automatic in most editors)

# 3. Quick build check (optional)
./scripts/build.sh

# 4. Commit frequently
git add Sources/Core/Operations/MyNewOperation.swift
git commit -m "feat: add MyNewOperation"

# 5. Test in simulator (when needed)
./scripts/run.sh

# 6. Full test suite (before push)
./scripts/test.sh
```

### When to Use Xcode

Open Xcode **only** for these tasks:

1. **Build Errors**: If command-line build fails
   ```bash
   # Open Xcode to see detailed error
   open MathCLI.xcodeproj
   ```

2. **Visual Debugging**: When you need breakpoints
   ```bash
   # Set breakpoints in Xcode
   # Run with Cmd+R
   ```

3. **UI Layout**: SwiftUI previews (optional)
   ```bash
   # Xcode has nice SwiftUI previews
   # But you can also just run the app
   ```

4. **Profiling**: Memory leaks, CPU usage
   ```bash
   # Cmd+I in Xcode to launch Instruments
   ```

### Evening Routine

```bash
# 1. Run full test suite
./scripts/test.sh

# 2. Commit all changes
git add .
git commit -m "feat: implemented X, Y, Z features"

# 3. Push to remote
git push origin main

# 4. Close Xcode (if open)
# Keep Claude Code open for tomorrow!
```

---

## Command-Line Tools

### Build Scripts

**Build for Simulator (Debug)**
```bash
./scripts/build.sh
```

**Build for Simulator (Release)**
```bash
./scripts/build.sh Release
```

**Build for Device**
```bash
./scripts/build.sh Debug device
```

### Test Scripts

**Run All Tests**
```bash
./scripts/test.sh
```

**Run Tests with Coverage**
```bash
./scripts/test.sh
# Results in DerivedData/
```

### Run Scripts

**Launch in Simulator (Default: iPhone 15)**
```bash
./scripts/run.sh
```

**Launch on iPad**
```bash
./scripts/run.sh "iPad Pro (12.9-inch) (6th generation)"
```

**List Available Simulators**
```bash
xcrun simctl list devices
```

### Swift Package Manager

**Build the Package**
```bash
swift build
```

**Run Tests**
```bash
swift test
```

**Run CLI Tool (for quick operation testing)**
```bash
swift run mathcli-tool

# Interactive REPL:
mathcli> add 5 3
Result: 8

mathcli> sqrt 16
Result: 4

mathcli> list
All Operations (266):
  1. abs
  2. acos
  ...

mathcli> quit
```

---

## Testing Strategies

### 1. Quick Operation Tests (Command-Line)

```bash
# Test individual operations without full app
swift run mathcli-tool

# Or create test script:
echo "add 5 3" | swift run mathcli-tool
echo "sqrt 16" | swift run mathcli-tool
echo "sin 1.57" | swift run mathcli-tool
```

### 2. Unit Tests

Create tests in `Tests/` directory:

```swift
// Tests/OperationTests/BasicArithmeticTests.swift
import XCTest
@testable import MathCLICore

final class BasicArithmeticTests: XCTestCase {
    func testAddOperation() throws {
        let result = try AddOperation.execute(args: [5, 3])
        XCTAssertEqual(result, .number(8))
    }
}
```

Run tests:
```bash
# Via script
./scripts/test.sh

# Via SPM
swift test

# Via Xcode
Cmd+U in Xcode
```

### 3. Integration Tests

Test in full app:

```bash
# Build and run
./scripts/run.sh

# Manual testing in simulator
# - Type: add 5 3
# - Check result: 8 ✅
```

### 4. CI/CD Testing

GitHub Actions runs automatically:
- On every push to main
- On every pull request
- Tests on iPhone & iPad simulators
- Code coverage reports

---

## Git Workflow

### Branch Strategy

```bash
# Main branch: stable releases
main

# Development branch
develop

# Feature branches
feature/add-new-operation
feature/improve-ui
fix/division-by-zero
```

### Commit Message Format

```bash
# Format: type(scope): description

feat(operations): add hyperbolic functions
fix(ui): correct history scrolling
docs(readme): update installation steps
test(matrix): add determinant tests
refactor(engine): improve error handling
```

### Example Workflow

```bash
# 1. Create feature branch
git checkout -b feature/add-statistics

# 2. Make changes in Claude Code
# Edit Sources/Core/Operations/Statistics/...

# 3. Commit incrementally
git add Sources/Core/Operations/Statistics/
git commit -m "feat(statistics): add variance operation"

git add Sources/Core/Operations/Statistics/
git commit -m "feat(statistics): add standard deviation operation"

# 4. Test
./scripts/test.sh

# 5. Push branch
git push origin feature/add-statistics

# 6. Create Pull Request on GitHub
# GitHub Actions will run tests automatically

# 7. Merge when tests pass
```

### .gitignore Best Practices

The `.gitignore` is already configured to ignore:
- ✅ Xcode user settings (xcuserdata)
- ✅ Build artifacts (DerivedData, build/)
- ✅ macOS files (.DS_Store)
- ❌ Don't ignore: project.pbxproj (needed for Xcode)

---

## Troubleshooting

### Problem: Xcode Doesn't See My Changes

**Solution**: You probably copied files instead of adding by reference.

```bash
# Fix:
# 1. Remove files from Xcode (keep on disk)
# 2. Re-add with "Add Files..."
# 3. UNCHECK "Copy items if needed"
```

### Problem: Build Works in Xcode, Fails in Command-Line

**Solution**: Clear derived data.

```bash
rm -rf ~/Library/Developer/Xcode/DerivedData
./scripts/build.sh
```

### Problem: Simulator Won't Launch

**Solution**: Reset simulator.

```bash
# Kill all simulators
killall Simulator

# Erase simulator data
xcrun simctl erase all

# Try again
./scripts/run.sh
```

### Problem: Code Signing Errors

**Solution**: Disable code signing for command-line builds.

Already handled in build scripts:
```bash
CODE_SIGN_IDENTITY=""
CODE_SIGNING_REQUIRED=NO
```

### Problem: Git Conflicts in project.pbxproj

**Solution**: Accept both changes, rebuild in Xcode.

```bash
# During merge conflict:
git checkout --ours MathCLI.xcodeproj/project.pbxproj
# or
git checkout --theirs MathCLI.xcodeproj/project.pbxproj

# Then let Xcode fix it:
open MathCLI.xcodeproj
# Xcode will auto-update project.pbxproj
```

### Problem: Tests Pass Locally, Fail in CI

**Solution**: Check iOS version in CI.

```yaml
# .github/workflows/ios-build-test.yml
destination: 'platform=iOS Simulator,name=iPhone 15,OS=17.2'
```

Make sure it matches your local environment.

---

## Advanced Tips

### 1. Use Claude Code for Everything Except Building

```bash
# In Claude Code:
# - Write Swift code
# - Read documentation
# - Search codebase
# - Refactor operations
# - Write tests

# In Terminal:
# - Build: ./scripts/build.sh
# - Test: ./scripts/test.sh
# - Run: ./scripts/run.sh

# In Xcode: (rarely)
# - Visual debugging only
```

### 2. Create Aliases

Add to `~/.zshrc` or `~/.bashrc`:

```bash
alias mb="cd /path/to/MathCLI-iOS && ./scripts/build.sh"
alias mt="cd /path/to/MathCLI-iOS && ./scripts/test.sh"
alias mr="cd /path/to/MathCLI-iOS && ./scripts/run.sh"
alias mcli="cd /path/to/MathCLI-iOS && swift run mathcli-tool"
```

Usage:
```bash
mb  # Quick build
mt  # Quick test
mr  # Quick run
mcli  # Quick CLI test
```

### 3. Watch Mode (Auto-build on Save)

Install `fswatch`:
```bash
brew install fswatch
```

Create watch script:
```bash
# scripts/watch.sh
#!/bin/bash
fswatch -o Sources/ | while read; do
    echo "Changes detected, rebuilding..."
    ./scripts/build.sh
done
```

Run in separate terminal:
```bash
./scripts/watch.sh
```

### 4. Pre-commit Hooks

Create `.git/hooks/pre-commit`:
```bash
#!/bin/bash
# Run tests before commit
./scripts/test.sh
if [ $? -ne 0 ]; then
    echo "Tests failed, commit aborted"
    exit 1
fi
```

Make executable:
```bash
chmod +x .git/hooks/pre-commit
```

---

## Summary

**Your Perfect Workflow:**

```
┌─────────────────┐
│  Claude Code    │  ← Primary editor (90% of time)
│  - Write code   │
│  - AI help      │
│  - Git commits  │
└────────┬────────┘
         │
         ├─→ ./scripts/build.sh  (quick check)
         ├─→ ./scripts/test.sh   (before push)
         └─→ ./scripts/run.sh    (manual test)

┌─────────────────┐
│     Xcode       │  ← Only when needed (10% of time)
│  - Debugging    │
│  - Profiling    │
│  - App Store    │
└─────────────────┘
```

**Remember:**
- ✅ Edit in Claude Code
- ✅ Build from command-line
- ✅ Use git liberally
- ✅ Open Xcode only when necessary
- ✅ Automate everything with scripts

Happy coding! 🚀
