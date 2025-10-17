# Changelog

All notable changes to Math CLI will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Phase 1: Foundation & Visual Enhancement - 2025-10-16

#### Added
- **Visual Enhancement System** (`utils/visual.py`)
  - Rich library integration for terminal formatting
  - Animated welcome banner with ASCII art
  - Color-coded output for inputs, results, and errors
  - Success indicators with checkmarks
  - Loading spinners for long operations (framework ready)
  - Smart error messages with contextual suggestions

- **Enhanced Interactive Mode**
  - Beautiful color-highlighted prompts showing previous results
  - Rich-formatted help system with panels and tables
  - Visual history display in table format
  - Animated chain calculation steps with arrows
  - Contextual tips and helpful messages
  - Friendly goodbye messages

- **Accessibility Features**
  - `--no-color` flag to disable colored output
  - `--no-animations` flag to disable animations
  - Graceful degradation to plain text mode
  - Visual preferences system for user customization

- **Error Handling Improvements**
  - Rich-formatted error panels with borders
  - Suggestion system for unknown operations
  - Clear, friendly error messages
  - Contextual help for common mistakes

- **Number Formatting**
  - Comma separators for large numbers
  - Scientific notation for very large/small numbers
  - Intelligent rounding and precision display

- **Documentation**
  - requirements.txt for dependency management
  - Updated README with visual enhancement examples
  - Accessibility documentation
  - Installation guide with virtual environment setup

#### Changed
- Interactive mode now features colorful, animated interface by default
- History display upgraded from plain text to rich formatted tables
- Error messages now use rich panels instead of plain text
- Help command now displays beautifully formatted tables and panels
- Prompts now show previous results with visual formatting

#### Technical Details
- **Dependencies Added**:
  - rich >= 14.0.0 (terminal rendering library)
  - markdown-it-py (for markdown help content)
  - pygments (for syntax highlighting)

- **New Modules**:
  - `utils/visual.py` - Visual formatting utilities
  - Comprehensive color scheme system
  - Visual preferences management

- **Modified Files**:
  - `cli/interactive_mode.py` - Integrated visual enhancements
  - `math_cli.py` - Added accessibility flags
  - `README.md` - Updated with Phase 1 features

#### Testing
- All visual features tested and verified
- Accessibility mode (--no-color --no-animations) tested
- Interactive mode with colors and animations tested
- History display tested with formatted tables
- Error handling tested with rich panels

---

## [0.2.0] - 2025-09-28

### Added
- Comprehensive plugin system with 110+ mathematical operations
- 8 specialized plugin modules (statistics, geometry, complex numbers, etc.)
- Extended functionality across multiple mathematical domains

---

## [0.1.0] - Initial Release

### Added
- Basic mathematical operations (add, subtract, multiply, divide)
- Interactive mode with history and chain calculations
- Plugin architecture for extensibility
- Command-line interface
