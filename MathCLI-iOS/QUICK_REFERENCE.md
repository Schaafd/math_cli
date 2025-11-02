# MathCLI iOS - Quick Reference Card

## 🚀 Daily Commands

### Build & Test
```bash
./scripts/build.sh              # Build for simulator
./scripts/build.sh Release      # Release build
./scripts/test.sh               # Run all tests
./scripts/run.sh                # Launch in simulator
./scripts/run.sh "iPad Pro"     # Launch on iPad
```

### Swift Package Manager
```bash
swift build                     # Build package
swift test                      # Run tests
swift run mathcli-tool          # Interactive CLI tool
```

### Verification
```bash
./scripts/verify-setup.sh       # Check your setup
```

---

## 📁 Project Structure

```
MathCLI-iOS/
├── Sources/
│   ├── Core/                   # 266 operations + engine
│   │   ├── Engine/            # OperationRegistry, Executor
│   │   └── Operations/        # All 20 categories
│   ├── UI/                     # SwiftUI views
│   └── Tool/                   # CLI testing tool
├── Tests/                      # Unit tests (create these)
├── scripts/                    # Build automation
│   ├── build.sh               # Build script
│   ├── test.sh                # Test script
│   ├── run.sh                 # Run in simulator
│   └── verify-setup.sh        # Setup verification
├── Package.swift              # Swift Package Manager
└── MathCLI.xcodeproj/        # Xcode project (create this)
```

---

## 🎯 Workflow

### Development Cycle
1. **Edit** in Claude Code (or any editor)
2. **Save** changes
3. **Build** with `./scripts/build.sh`
4. **Test** with `./scripts/test.sh`
5. **Commit** with git
6. **Repeat**

### When to Open Xcode
- ⚠️ Build errors (detailed diagnostics)
- 🐛 Visual debugging (breakpoints)
- 📊 Performance profiling
- 📱 App Store submission
- 🎨 UI layout tweaking (optional)

---

## 📚 Operations (266 Total)

### Categories
- **Basic Arithmetic** (14): add, subtract, multiply, divide, power, sqrt, factorial, abs, log, sin, cos, tan, toRadians, toDegrees
- **Trigonometry** (10): asin, acos, atan, atan2, sinh, cosh, tanh, asinh, acosh, atanh
- **Advanced Math** (8): ceil, floor, round, trunc, gcd, lcm, mod, exp
- **Statistics** (15): mean, median, mode, variance, stddev, min, max, sum, count, etc.
- **Constants** (7): pi, e, golden_ratio, speed_of_light, planck, avogadro, boltzmann
- **Unit Conversions** (38): temperature, distance, weight, volume, speed, time, data, energy, pressure
- **Geometry** (15): distance, area_circle, volume_sphere, pythagorean, etc.
- **Combinatorics** (10): combinations, permutations, fibonacci, is_prime, etc.
- **Number Theory** (15): prime_factors, euler_phi, catalan, etc.
- **Complex Numbers** (18): cadd, csub, cmul, cdiv, magnitude, phase, etc.
- **Variables** (6): set, get, persist, vars, unset, clear_vars
- **Control Flow** (13): eq, neq, gt, lt, and, or, not, if, etc.
- **Functions** (3): def, funcs, undef
- **Scripts** (2): run, eval
- **Export** (6): export_session, import_session, export_vars, etc.
- **Matrix** (12): det, transpose, eigenvalues, inverse, etc.
- **Calculus** (12): derivative, integrate, limit, taylor, solve_ode, etc.
- **Data Analysis** (12): load_data, describe_data, correlation_matrix, etc.
- **Data Transform** (11): filter_data, normalize_data, sort_data, etc.
- **Plotting** (8): plot_hist, plot_scatter, plot_line, etc.

---

## 🧪 Testing Operations

### Interactive CLI Tool
```bash
swift run mathcli-tool

# In the tool:
mathcli> add 5 3
Result: 8

mathcli> sqrt 16
Result: 4

mathcli> list
All Operations (266): ...

mathcli> search sin
Search Results for 'sin': ...

mathcli> help
Available Commands: ...

mathcli> quit
```

### Quick Tests
```bash
# Test specific operation
echo "add 5 3" | swift run mathcli-tool

# Test multiple
cat << EOF | swift run mathcli-tool
add 5 3
sqrt 16
sin 1.57
EOF
```

---

## 🔧 Git Commands

### Standard Workflow
```bash
git status                      # Check status
git add Sources/                # Stage changes
git commit -m "feat: add X"     # Commit
git push origin main            # Push to remote
```

### Branch Workflow
```bash
git checkout -b feature/new-op  # Create branch
# ... make changes ...
git add .
git commit -m "feat: new operation"
git push origin feature/new-op
# Create PR on GitHub
```

### Commit Types
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `test:` Tests
- `refactor:` Code refactoring
- `style:` Formatting
- `chore:` Maintenance

---

## ⚡ Power User Tips

### Aliases (Add to ~/.zshrc)
```bash
alias mb="cd ~/MathCLI-iOS && ./scripts/build.sh"
alias mt="cd ~/MathCLI-iOS && ./scripts/test.sh"
alias mr="cd ~/MathCLI-iOS && ./scripts/run.sh"
alias mcli="cd ~/MathCLI-iOS && swift run mathcli-tool"
```

### Watch Mode (Auto-build on save)
```bash
brew install fswatch
fswatch -o Sources/ | while read; do ./scripts/build.sh; done
```

### Pre-commit Hook
```bash
# .git/hooks/pre-commit
#!/bin/bash
./scripts/test.sh || exit 1
```

---

## 📖 Documentation Files

- **README.md** - Project overview and setup
- **DEVELOPMENT_WORKFLOW.md** - Detailed workflow guide (⭐ Read this!)
- **XCODE_SETUP_GUIDE.md** - Step-by-step Xcode setup
- **IMPLEMENTATION_ROADMAP.md** - Development phases and timeline
- **PROJECT_SUMMARY.md** - Current status and metrics
- **QUICK_REFERENCE.md** - This file!

---

## 🆘 Troubleshooting

### Build Fails
```bash
# Clear derived data
rm -rf ~/Library/Developer/Xcode/DerivedData
./scripts/build.sh
```

### Simulator Issues
```bash
# Kill simulator
killall Simulator

# Erase all simulators
xcrun simctl erase all

# Try again
./scripts/run.sh
```

### Xcode Not Seeing Changes
- Make sure files were added by **reference**, not copied
- Close and reopen Xcode
- Clean build folder: Product → Clean Build Folder (Cmd+Shift+K)

### License Agreement
```bash
sudo xcodebuild -license accept
```

---

## 🎓 Learning Resources

### Swift & SwiftUI
- [Swift.org](https://swift.org)
- [SwiftUI Tutorials](https://developer.apple.com/tutorials/swiftui)
- [Hacking with Swift](https://hackingwithswift.com)

### iOS Development
- [Apple Developer](https://developer.apple.com)
- [iOS Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/ios)

### Our Codebase
- Start with: `Sources/Core/Operations/BasicArithmetic/BasicOperations.swift`
- Study pattern in: `Sources/Core/Engine/MathOperation.swift`
- See execution: `Sources/Core/Engine/OperationExecutor.swift`

---

## ✅ First Time Setup Checklist

- [ ] Run `./scripts/verify-setup.sh`
- [ ] Read `DEVELOPMENT_WORKFLOW.md`
- [ ] Create Xcode project (see `XCODE_SETUP_GUIDE.md`)
- [ ] Add files to Xcode by **reference**
- [ ] Build with `./scripts/build.sh`
- [ ] Test with `./scripts/test.sh`
- [ ] Run with `./scripts/run.sh`
- [ ] Try CLI tool: `swift run mathcli-tool`
- [ ] Commit initial setup to git
- [ ] Set up git aliases (optional)
- [ ] Install optional tools: xcpretty, swiftlint, fswatch

---

## 💡 Key Concepts

### Operation Pattern
```swift
struct MyOperation: MathOperation {
    static var name = "my_op"
    static var arguments = ["arg1", "arg2"]
    static var help = "Description: my_op arg1 arg2"
    static var category = OperationCategory.basic

    static func execute(args: [Any]) throws -> OperationResult {
        let val1 = try parseDouble(args[0], argumentName: "arg1")
        let val2 = try parseDouble(args[1], argumentName: "arg2")
        return .number(val1 + val2)
    }
}
```

### Register Operation
```swift
// In OperationRegistry.swift
register(MyOperation.self)
```

### Use in App
```
User types: my_op 5 3
Result: 8
```

---

## 📞 Support

- **Issues**: Check GitHub Issues
- **Questions**: Read `DEVELOPMENT_WORKFLOW.md`
- **Setup**: See `XCODE_SETUP_GUIDE.md`
- **Architecture**: See `README.md`

---

**Last Updated**: 2025-01-11
**Version**: 1.0.0 (266 operations complete!)
