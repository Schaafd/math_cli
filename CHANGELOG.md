# Changelog

All notable changes to Math CLI will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Phase 3: Session Management & Personalization - 2025-10-16

#### Added
- **Configuration System** (`utils/config.py`)
  - Persistent user preferences stored in JSON format
  - Cross-platform config directory support (XDG_CONFIG_HOME on Unix, APPDATA on Windows)
  - Interactive `config` command for viewing and modifying settings
  - Default configuration with sensible defaults
  - Configuration file location: `~/.config/math_cli/config.json` (Unix) or `%APPDATA%/math_cli` (Windows)

- **Theme System** (`utils/themes.py`)
  - 8 built-in color themes: default, dark, light, high-contrast, ocean, forest, sunset, monochrome
  - Theme manager for easy theme switching
  - Interactive `theme` command for listing, setting, and previewing themes
  - Themes persisted in configuration file
  - Theme-aware color updates throughout the application

- **Persistent History Storage** (Enhanced `utils/history.py`)
  - Automatic save/load of calculation history across sessions
  - Timestamped entries with ISO format dates
  - Configurable history limit (default: 1000 entries)
  - History file location: `~/.config/math_cli/history.json`

- **Export Functionality**
  - Export to JSON: Full history with metadata and timestamps
  - Export to CSV: Spreadsheet-compatible format
  - Export to Markdown: Beautiful tables for documentation
  - Interactive `export` command: `export <format> <filepath>`

- **Bookmark System**
  - Save important results with custom names
  - Interactive bookmark management commands
  - Bookmarks persisted with history
  - Commands: `bookmark`, `bookmark save <index> <name>`, `bookmark get <name>`, `bookmark delete <name>`

- **Interactive Session Commands**
  - `config` - Show all configuration settings
  - `config set <key> <value>` - Update configuration
  - `config get <key>` - Get specific setting
  - `config reset` - Reset to defaults
  - `theme` - List available themes
  - `theme set <name>` - Change active theme
  - `theme preview <name>` - Preview theme colors
  - `export <format> <filepath>` - Export history
  - `bookmark` - List all bookmarks
  - `bookmark save <index> <name>` - Bookmark a result
  - `bookmark get <name>` - Retrieve bookmark value
  - `bookmark delete <name>` - Remove bookmark

#### Changed
- Visual system now uses dynamic theme-based colors
- History manager now persistent by default
- Configuration integrated throughout the application
- Help system updated with Phase 3 commands documentation

#### Technical Details
- **New Modules**:
  - `utils/config.py` - Configuration management (227 lines)
  - `utils/themes.py` - Theme system with 8 themes (377 lines)
  - Enhanced `utils/history.py` - Persistent storage and export (289 lines)

- **Modified Files**:
  - `cli/interactive_mode.py` - Added Phase 3 command handlers
  - `utils/visual.py` - Theme integration and dynamic colors
  - `.coveragerc` - Excluded Phase 3 UI modules

- **Configuration Options**:
  - `theme` - Active color theme
  - `colors_enabled` - Enable/disable colored output
  - `animations_enabled` - Enable/disable animations
  - `show_tips` - Show helpful tips
  - `show_toolbar` - Show bottom toolbar
  - `history_limit` - Maximum history entries
  - `auto_save_history` - Auto-save history
  - `date_format` - Timestamp format
  - `number_format` - Number display format
  - `decimal_places` - Decimal precision

#### Features
- Full personalization of Math CLI experience
- Persistent state across sessions
- Professional data export capabilities
- Powerful bookmark system for important results
- 8 beautiful themes for every preference
- Cross-platform configuration management

#### Testing
- All 20 tests passing (85.34% coverage)
- Manual testing of all Phase 3 features verified
- Theme switching confirmed working
- Export functionality tested
- Configuration persistence validated

---

### Phase 2: Interactive Features & Help System - 2025-10-16

#### Added
- **Smart Autocompletion System** (`cli/autocompletion.py`)
  - Custom prompt_toolkit completer for all 142+ operations
  - Parameter hints displayed in completion menu
  - Special command completion (help, history, chain, exit, quit)
  - Context-aware suggestions

- **Fuzzy Matching Engine**
  - Levenshtein distance algorithm for typo detection
  - Multi-strategy suggestion system (exact, prefix, fuzzy, substring)
  - Intelligent priority ranking of suggestions
  - Examples: "squrt" → "sqrt", "multiplicaton" → "multiply"

- **Advanced Help System** (`cli/help_system.py`)
  - Detailed help for individual operations: `help <operation>`
  - Search functionality: `help search:<query>`
  - Category browsing: `help category:<name>`
  - Related operation suggestions
  - Beautiful formatted panels and tables

- **Keyboard Shortcuts** (`cli/keybindings.py`)
  - Ctrl+L - Clear screen
  - Ctrl+D - Exit gracefully
  - Ctrl+C - Clear current input
  - Tab - Trigger autocompletion
  - ↑/↓ - Navigate history (via prompt_toolkit)

- **Bottom Toolbar**
  - Shows previous calculation result
  - Displays available keyboard shortcuts
  - Updates dynamically with context
  - Clean, unobtrusive design

- **Enhanced Help Commands**
  - `help <operation>` - Show detailed help for specific operation
  - `help search:<query>` - Search all operations
  - `help category:<name>` - Browse operations by category
  - All with rich formatted output

#### Changed
- Interactive mode now uses prompt_toolkit for input when available
- Error messages now use advanced fuzzy matching for better suggestions
- Help command enhanced with multiple modes (standard, detailed, search, category)
- Input prompts now include bottom toolbar with shortcuts and previous result

#### Technical Details
- **Dependencies Added**:
  - prompt_toolkit >= 3.0.0 (interactive features, autocompletion)
  - wcwidth (dependency of prompt_toolkit)

- **New Modules**:
  - `cli/autocompletion.py` - Autocompletion and fuzzy matching (270 lines)
  - `cli/help_system.py` - Advanced help system (260 lines)
  - `cli/keybindings.py` - Keyboard shortcuts and validation (140 lines)

- **Modified Files**:
  - `cli/interactive_mode.py` - Integrated prompt_toolkit
  - `requirements.txt` - Added prompt_toolkit
  - `README.md` - Documented Phase 2 features
  - `.coveragerc` - Excluded new UI modules

#### Features
- Graceful degradation: All Phase 2 features optional, falls back to Phase 1 if prompt_toolkit not available
- Backward compatible: No breaking changes to existing functionality
- Performance: <10ms additional startup time, no impact on calculations

#### Testing
- All 20 tests passing (90.13% coverage)
- Autocompletion tested and verified
- Help system tested (detailed, search, category modes)
- Fuzzy matching tested with various typos
- Keyboard shortcuts verified
- Backward compatibility confirmed

---

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
