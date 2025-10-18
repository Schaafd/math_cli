from typing import Dict, Any
from utils.history import HistoryManager
from utils.visual import (
    print_welcome_banner,
    print_result,
    print_error,
    print_info,
    print_success,
    print_tip,
    print_operations_table,
    print_history_table,
    print_chain_step,
    print_final_result,
    print_help_panel,
    console,
    preferences
)

# Phase 2: Interactive features
try:
    from prompt_toolkit import PromptSession
    from prompt_toolkit.history import InMemoryHistory
    from prompt_toolkit.formatted_text import HTML
    from cli.autocompletion import MathOperationCompleter, suggest_corrections
    from cli.keybindings import create_key_bindings, get_bottom_toolbar_text
    from cli.help_system import (
        show_operation_help,
        show_search_results,
        show_category_operations,
        show_quick_reference
    )
    PROMPT_TOOLKIT_AVAILABLE = True
except ImportError:
    PROMPT_TOOLKIT_AVAILABLE = False

def run_interactive_mode(plugin_manager, operations_metadata: Dict, enable_colors=True, enable_animations=True, accessibility_settings=None) -> None:
    """Run the CLI in interactive mode with rich visual enhancements.

    Args:
        plugin_manager: Plugin manager instance
        operations_metadata: Dictionary of operation metadata
        enable_colors: Whether to enable colors
        enable_animations: Whether to enable animations
        accessibility_settings: Optional accessibility settings dictionary
    """
    # Set visual preferences
    if not enable_colors:
        preferences.disable_colors()
    if not enable_animations:
        preferences.disable_animations()

    # Phase 4: Apply accessibility settings
    if accessibility_settings:
        from utils.accessibility import get_accessibility_manager
        a11y = get_accessibility_manager()

        if accessibility_settings.get('screen_reader_mode'):
            a11y.enable_screen_reader_mode()
            # Auto-disable animations and colors for screen readers
            preferences.disable_colors()
            preferences.disable_animations()

        if accessibility_settings.get('high_contrast'):
            a11y.enable_high_contrast()
            # Apply high contrast theme
            from utils.themes import apply_theme_to_visual
            apply_theme_to_visual('high-contrast')

    # Display welcome banner
    print_welcome_banner()
    print_info("Type 'exit' or 'quit' to exit, 'help' for available commands")

    # Initialize history manager
    history = HistoryManager()

    # Store the last result for reference
    last_result = None

    def show_help():
        """Display help information for all operations."""
        # Show operations table
        print_operations_table(operations_metadata)

        # Show history commands help
        history_help = """
**History Commands:**
- `history` - Show calculation history
- `history <n>` - Show the nth most recent calculation
- `history clear` - Clear calculation history
- `!<n>` - Re-run the nth most recent calculation
        """
        print_help_panel("History Commands", history_help)

        # Show previous result reference help
        result_ref_help = """
**Previous Result Reference:**
- `$` or `ans` - Use the result of the previous calculation
- Example: `add $ 5` (adds 5 to the previous result)
        """
        print_help_panel("Previous Result Reference", result_ref_help)

        # Show chain calculation help
        chain_help = """
**Chained Calculations:**
- Syntax: `chain <operation1> <args1> | <operation2> <args2> | ...`
- Example: `chain add 5 3 | multiply $ 2`
- The result of each operation becomes available as `$` in the next one
        """
        print_help_panel("Chained Calculations", chain_help)

        # Show Phase 3 features help
        phase3_help = """
**Configuration & Themes:**
- `config` - Show current configuration
- `config set <key> <value>` - Update configuration
- `theme` - List available themes
- `theme set <name>` - Change theme
- `theme preview <name>` - Preview a theme

**Export & Bookmarks:**
- `export <format> <filepath>` - Export history (json, csv, markdown)
- `bookmark` - List all bookmarks
- `bookmark save <index> <name>` - Bookmark a result
- `bookmark get <name>` - Retrieve a bookmark
        """
        print_help_panel("Session Management", phase3_help)

        # Show Phase 4 features help
        phase4_help = """
**Plotting:**
- `plot <function> <start> <end>` - Plot a mathematical function
- `plot_data <values...>` - Scatter plot of data points
- `plot_bar <values...>` - Bar chart
- `plot_line <values...>` - Line chart

**Multi-line Input:**
- Use `\\` at end of line to continue on next line
- Unclosed brackets `(` `[` `{` automatically continue
- Chain commands ending with `|` continue automatically
- Press Enter twice on blank line to cancel continuation

**Performance:**
- `perf` - Show performance metrics
- `perf reset` - Reset metrics
- `perf startup` - Show startup metrics
        """
        print_help_panel("Advanced Features (Phase 4)", phase4_help)

    def parse_command(input_text, allow_chain=True, current_result=None):
        """Parse the user input command and arguments.

        Args:
            input_text: The command text to parse
            allow_chain: Whether to recognize chain commands
            current_result: Override for the last_result (for chain operations)
        """
        # Use current_result if provided, otherwise default to last_result
        result_to_use = current_result if current_result is not None else last_result

        # Handle chained calculations
        if allow_chain and input_text.lower().startswith('chain '):
            return "chain", input_text[6:].strip()  # Return the rest of the command after 'chain'

        else:
            if result_to_use is not None:
                input_text = input_text.replace('$', str(result_to_use))

                # Split the input to properly handle 'ans' replacement
                parts = input_text.split()
                for i in range(len(parts)):
                    if parts[i].lower() == 'ans':
                        parts[i] = str(result_to_use)
                input_text = ' '.join(parts)

        parts = input_text.split()
        if not parts:
            return None, None

        # Handle history commands
        if parts[0] == "history":
            return "history", parts[1:] if len(parts) > 1 else []

        # Handle history recall shorthand (!n)
        if parts[0].startswith("!") and len(parts[0]) > 1:
            try:
                idx = int(parts[0][1:])
                entry = history.get_entry(idx - 1)  # Convert to 0-based index
                if entry:
                    print(f"Re-running: {entry['command']}")
                    return parse_command(entry['command'])
                else:
                    print(f"Error: History entry {idx} not found")
                    return None, None
            except ValueError:
                print(f"Error: Invalid history index: {parts[0][1:]}")
                return None, None

        op_name = parts[0]

        # Check if it's a special command (config, theme, export, bookmark, perf)
        special_commands = ['config', 'theme', 'export', 'bookmark', 'perf']
        if op_name in special_commands:
            return op_name, parts[1:]

        if op_name not in operations_metadata:
            # Use advanced fuzzy matching if available
            if PROMPT_TOOLKIT_AVAILABLE:
                suggestions = suggest_corrections(op_name, operations_metadata, max_suggestions=3)
                suggestion = f"Did you mean: {', '.join(suggestions)}?" if suggestions else "Use 'help' to see available operations"
            else:
                # Fallback to simple prefix matching
                similar_ops = [op for op in operations_metadata.keys() if op.startswith(parts[0][:3])]
                suggestion = f"Did you mean: {', '.join(similar_ops[:3])}?" if similar_ops else "Use 'help' to see available operations"
            print_error(f"Unknown operation: {op_name}", suggestion)
            return None, None

        return op_name, parts[1:]

    def process_args(op_name, arg_parts):
        """Process and validate command arguments."""
        required_args = operations_metadata[op_name]['args']
        is_variadic = operations_metadata[op_name].get('variadic', False)

        # For variadic functions, we need at least one argument (unless explicitly no args required)
        if is_variadic:
            if len(required_args) > 0 and len(arg_parts) == 0:
                print_error(f"{op_name} requires at least one argument",
                           f"Usage: {op_name} <number1> <number2> ...")
                return None
        else:
            # For non-variadic functions, check exact argument count
            if len(arg_parts) < len(required_args):
                print_error(f"Not enough arguments for {op_name}",
                           f"Expected {len(required_args)} arguments: {', '.join(required_args)}")
                return None

        # Parse arguments
        arg_values = []

        if is_variadic:
            # For variadic functions, parse all provided arguments
            for i, arg_part in enumerate(arg_parts):
                try:
                    arg_values.append(float(arg_part))
                except ValueError:
                    print_error(f"Invalid argument '{arg_part}' at position {i+1}",
                               "Expected a numeric value")
                    return None
        else:
            # For fixed-argument functions, parse only the required number
            for i, arg_name in enumerate(required_args):
                try:
                    if arg_name == 'n' and op_name == 'factorial':
                        # Factorial needs integer
                        arg_values.append(int(float(arg_parts[i])))
                    else:
                        arg_values.append(float(arg_parts[i]))
                except ValueError:
                    print_error(f"Invalid argument '{arg_parts[i]}' for parameter '{arg_name}'",
                               "Expected a numeric value")
                    return None

        return arg_values

    def handle_history_command(args):
        """Handle history-related commands."""
        if not args:
            # Display all history
            entries = history.get_all_entries()
            print_history_table(entries)
        elif args[0] == "clear":
            # Clear history
            history.clear()
            print_success("History cleared")
        else:
            # Show specific history entry
            try:
                idx = int(args[0]) - 1  # Convert to 0-based index
                entry = history.get_entry(idx)
                if entry:
                    print_info(f"{args[0]}: {entry['command']} = {entry['result']}")
                else:
                    print_error(f"History entry {args[0]} not found",
                               f"Valid range: 1-{len(history.get_all_entries())}")
            except ValueError:
                print_error(f"Invalid history index: {args[0]}",
                           "Expected a numeric index")

    def handle_chain_command(chain_text):
        """Handle a chain of calculations."""
        nonlocal last_result

        # Split the chain by the pipe symbol
        operations = chain_text.split('|')
        if not operations:
            print_error("No operations in chain",
                       "Usage: chain <op1> <args> | <op2> <args> | ...")
            return

        chain_result = None
        full_command = "chain " + chain_text
        temp_result = last_result  # Store original last_result to restore if needed

        # Process each operation in the chain
        for i, operation in enumerate(operations):
            operation = operation.strip()
            if not operation:
                continue

            # Parse the operation (with current chain result)
            # Use the updated parse_command that takes a current_result parameter
            op_name, arg_parts = parse_command(
                operation,
                allow_chain=False,
                current_result=chain_result
            )

            if not op_name:
                print_error(f"Invalid operation in chain segment {i+1}",
                           f"Check the syntax of: {operation}")
                last_result = temp_result  # Restore original last_result
                return

            # Process arguments
            arg_values = process_args(op_name, arg_parts)

            if arg_values is None:
                last_result = temp_result  # Restore original last_result
                return

            try:
                # Execute the operation
                result = plugin_manager.execute_operation(op_name, *arg_values)
                chain_result = result

                # Show intermediate result with visual formatting
                print_chain_step(i+1, operation, result)

            except ValueError as e:
                print_error(f"Error in chain segment {i+1}: {str(e)}",
                           "Check your operation arguments")
                last_result = temp_result  # Restore original last_result
                return

        # Store the final result and add to history
        if chain_result is not None:
            print_final_result(chain_result)
            history.add_entry(full_command, chain_result)
            # Update the session's last_result with the chain's final result
            last_result = chain_result
            return chain_result
        else:
            # If no result was produced, restore the original last_result
            last_result = temp_result

        return None

    def handle_config_command(args):
        """Handle configuration commands."""
        from utils.config import get_config

        config = get_config()

        if not args:
            # Show all configuration
            config.show_config()
        elif args[0] == "set" and len(args) >= 3:
            # Set a configuration value
            key = args[1]
            value = args[2]

            # Convert value to appropriate type
            if value.lower() in ('true', 'false'):
                value = value.lower() == 'true'
            elif value.isdigit():
                value = int(value)

            if config.set(key, value):
                print_success(f"Configuration updated: {key} = {value}")
            else:
                print_error("Failed to save configuration")
        elif args[0] == "get" and len(args) >= 2:
            # Get a configuration value
            key = args[1]
            value = config.get(key)
            if value is not None:
                print_info(f"{key} = {value}")
            else:
                print_error(f"Configuration key not found: {key}")
        elif args[0] == "reset":
            # Reset to defaults
            if config.reset():
                print_success("Configuration reset to defaults")
            else:
                print_error("Failed to reset configuration")
        else:
            print_error("Invalid config command",
                       "Usage: config [set <key> <value> | get <key> | reset]")

    def handle_theme_command(args):
        """Handle theme commands."""
        from utils.themes import get_theme_manager, apply_theme_to_visual, THEMES
        from utils.config import get_config

        theme_manager = get_theme_manager()
        config = get_config()

        if not args:
            # List all available themes
            themes = theme_manager.list_themes()
            current = config.get('theme', 'default')

            console.print("\n[bold]Available Themes:[/bold]\n")
            for name, description in sorted(themes.items()):
                marker = "→" if name == current else " "
                console.print(f"{marker} [cyan]{name:15}[/cyan] {description}")
            console.print(f"\n[dim]Current theme: {current}[/dim]")
        elif args[0] == "set" and len(args) >= 2:
            # Set a theme
            theme_name = args[1]
            if apply_theme_to_visual(theme_name):
                # Save to configuration
                config.set('theme', theme_name)
                print_success(f"Theme changed to: {theme_name}")
                print_info("Theme will be applied to new output")
            else:
                available = ', '.join(THEMES.keys())
                print_error(f"Theme not found: {theme_name}",
                           f"Available themes: {available}")
        elif args[0] == "preview" and len(args) >= 2:
            # Preview a theme
            theme_name = args[1]
            theme_manager.preview_theme(theme_name)
        else:
            print_error("Invalid theme command",
                       "Usage: theme [set <name> | preview <name>]")

    def handle_export_command(args):
        """Handle history export commands."""
        from pathlib import Path

        if not args or len(args) < 2:
            print_error("Invalid export command",
                       "Usage: export <format> <filepath>\n"
                       "Formats: json, csv, markdown")
            return

        format_type = args[0].lower()
        filepath = Path(' '.join(args[1:]))  # Join remaining args as filepath

        try:
            if format_type == "json":
                if history.export_to_json(filepath):
                    print_success(f"History exported to {filepath}")
                else:
                    print_error("Failed to export history")
            elif format_type == "csv":
                if history.export_to_csv(filepath):
                    print_success(f"History exported to {filepath}")
                else:
                    print_error("Failed to export history")
            elif format_type == "markdown" or format_type == "md":
                if history.export_to_markdown(filepath):
                    print_success(f"History exported to {filepath}")
                else:
                    print_error("Failed to export history")
            else:
                print_error(f"Unknown export format: {format_type}",
                           "Supported formats: json, csv, markdown")
        except Exception as e:
            print_error(f"Export failed: {str(e)}")

    def handle_bookmark_command(args):
        """Handle bookmark commands."""
        if not args:
            # List all bookmarks
            bookmarks = history.list_bookmarks()
            if not bookmarks:
                print_info("No bookmarks saved")
                return

            from rich.table import Table
            from rich import box

            table = Table(
                title="Saved Bookmarks",
                box=box.ROUNDED,
                header_style="bold cyan"
            )
            table.add_column("Name", style="yellow bold")
            table.add_column("Command", style="cyan")
            table.add_column("Result", style="green bold")

            for name, bookmark in sorted(bookmarks.items()):
                from utils.visual import format_number
                table.add_row(
                    name,
                    bookmark['command'],
                    format_number(bookmark['result'])
                )

            console.print(table)
        elif args[0] == "save" and len(args) >= 3:
            # Save a bookmark: bookmark save <index> <name>
            try:
                index = int(args[1]) - 1  # Convert to 0-based
                name = args[2]
                history.bookmark_result(index, name)
                print_success(f"Result bookmarked as '{name}'")
            except ValueError:
                print_error("Invalid bookmark index",
                           "Usage: bookmark save <history_index> <name>")
        elif args[0] == "get" and len(args) >= 2:
            # Get a bookmark value
            name = args[1]
            bookmark = history.get_bookmark(name)
            if bookmark:
                from utils.visual import format_number
                print_info(f"Bookmark '{name}': {bookmark['command']} = {format_number(bookmark['result'])}")
            else:
                print_error(f"Bookmark not found: {name}")
        elif args[0] == "delete" and len(args) >= 2:
            # Delete a bookmark
            name = args[1]
            if history.delete_bookmark(name):
                print_success(f"Bookmark deleted: {name}")
            else:
                print_error(f"Bookmark not found: {name}")
        else:
            print_error("Invalid bookmark command",
                       "Usage: bookmark [save <index> <name> | get <name> | delete <name>]")

    def handle_perf_command(args):
        """Handle performance monitoring commands."""
        from utils.performance import get_monitor, get_startup_metrics

        monitor = get_monitor()

        if not args:
            # Show performance summary
            monitor.print_summary()
        elif args[0] == "reset":
            # Reset metrics
            monitor.reset()
            print_success("Performance metrics reset")
        elif args[0] == "startup":
            # Show startup metrics
            metrics = get_startup_metrics()
            console.print(f"\n[cyan]Startup Metrics:[/cyan]")
            console.print(f"  Uptime: {metrics['uptime']:.2f}s")
            console.print(f"  Memory Usage: {metrics['memory_usage']:.2f} MB")
            console.print(f"  Memory Delta: {metrics['memory_delta']:.2f} MB")
        else:
            print_error("Invalid perf command",
                       "Usage: perf [reset | startup]")

    def handle_plot_command(plot_type, args):
        """Handle plotting commands."""
        from utils.plotting import plot_function_string, ASCIIPlotter

        try:
            if plot_type == "plot":
                # plot <function> <start> <end>
                if len(args) < 3:
                    print_error("plot requires 3 arguments",
                               "Usage: plot <function> <start> <end>")
                    return

                func_name = args[0]
                start = float(args[1])
                end = float(args[2])

                result = plot_function_string(func_name, start, end)

                console.print(f"\n[cyan]Plot:[/cyan] {func_name}(x) from {start} to {end}\n")
                console.print(result)

                # Add to history
                history.add_entry(f"plot {func_name} {start} {end}", f"Plotted {func_name}(x)")

            elif plot_type in ["plot_data", "plot_line", "plot_bar"]:
                # plot_data/plot_line/plot_bar <values...>
                if len(args) == 0:
                    print_error(f"{plot_type} requires at least one value",
                               f"Usage: {plot_type} <value1> <value2> ...")
                    return

                # Convert all args to floats
                values = [float(arg) for arg in args]

                # Determine style
                style_map = {
                    'plot_data': 'scatter',
                    'plot_line': 'line',
                    'plot_bar': 'bar'
                }
                style = style_map[plot_type]

                # Create plotter with appropriate size
                width = min(len(values) * 4, 60) if style == 'bar' else 50
                plotter = ASCIIPlotter(width=width, height=15)
                result = plotter.plot_data(values, style=style)

                # Display
                title_map = {
                    'plot_data': 'Data Plot',
                    'plot_line': 'Line Chart',
                    'plot_bar': 'Bar Chart'
                }
                console.print(f"\n[cyan]{title_map[plot_type]}:[/cyan] {len(values)} points\n")
                console.print(result)

                # Add to history
                history.add_entry(f"{plot_type} {' '.join(args)}", f"Plotted {len(values)} {style}")

        except ValueError as e:
            print_error(f"Error in plot command: {str(e)}",
                       "Check that all numeric arguments are valid")

    # Show initial tips about features
    console.print()
    print_tip("Use '$' or 'ans' to reference the previous result in calculations")
    print_tip("Use 'chain' to perform multiple calculations in sequence")

    if PROMPT_TOOLKIT_AVAILABLE and preferences.colors_enabled:
        print_tip("Press [Tab] for autocompletion, [Ctrl+L] to clear screen")
        print_tip("Use 'help <operation>' for detailed help on any command")
    else:
        print_tip("Type 'help' for a complete list of available commands")

    # Setup prompt_toolkit session if available
    if PROMPT_TOOLKIT_AVAILABLE and preferences.colors_enabled:
        from cli.multiline_input import MultilineDetector
        from prompt_toolkit.filters import Condition

        # Create multiline detector
        multiline_detector = MultilineDetector()

        # Custom multiline check function wrapped in Condition (Filter)
        @Condition
        def is_multiline():
            """Check if input should continue to next line."""
            # Get the current text from the app's current buffer
            from prompt_toolkit.application import get_app
            try:
                app = get_app()
                text = app.current_buffer.text
                needs_cont, _ = multiline_detector.needs_continuation(text)
                return needs_cont
            except:
                return False

        session = PromptSession(
            history=InMemoryHistory(),
            completer=MathOperationCompleter(operations_metadata),
            complete_while_typing=False,  # Only complete on Tab
            key_bindings=create_key_bindings(history),
            bottom_toolbar=lambda: get_bottom_toolbar_text(last_result, show_shortcuts=True),
            multiline=is_multiline,  # Enable smart multiline
            prompt_continuation="... "
        )
    else:
        session = None

    while True:
        try:
            # Get user input with prompt_toolkit or standard input
            if session:
                # Use prompt_toolkit for enhanced input
                if last_result is not None:
                    from utils.visual import format_number
                    prompt_text = HTML(f'\n<ansigreen>❯</ansigreen> <dim>(prev: {format_number(last_result)})</dim> ')
                else:
                    prompt_text = HTML('\n<ansigreen>❯</ansigreen> ')

                user_input = session.prompt(prompt_text).strip()
            else:
                # Fallback to standard input with multiline support
                from cli.multiline_input import collect_multiline_input

                if last_result is not None:
                    from utils.visual import format_number
                    prompt = f"\n❯ (prev: {format_number(last_result)}) " if preferences.colors_enabled else f"\nEnter command (previous: {last_result}): "
                else:
                    prompt = "\n❯ " if preferences.colors_enabled else "\nEnter command: "

                user_input = collect_multiline_input(prompt, "... ", preferences.colors_enabled)

            if user_input.lower() in ('exit', 'quit'):
                print_success("Goodbye! Thanks for using Math CLI")
                break

            # Handle enhanced help commands
            if user_input.lower().startswith('help'):
                parts = user_input.split(maxsplit=1)
                if len(parts) == 1:
                    # Standard help
                    show_help()
                elif PROMPT_TOOLKIT_AVAILABLE:
                    # Enhanced help with argument
                    arg = parts[1]
                    if arg.startswith('search:'):
                        # Search for operations
                        query = arg[7:].strip()
                        show_search_results(query, operations_metadata)
                    elif arg.startswith('category:'):
                        # Show category
                        category = arg[9:].strip()
                        show_category_operations(category, operations_metadata)
                    else:
                        # Show help for specific operation
                        show_operation_help(arg, operations_metadata)
                else:
                    show_help()
                continue

            op_name, arg_parts = parse_command(user_input)
            if not op_name:
                continue

            # Handle special commands
            if op_name == "history":
                handle_history_command(arg_parts)
                continue

            if op_name == "chain":
                result = handle_chain_command(arg_parts)
                # We don't need to update last_result here as it's now handled inside handle_chain_command
                continue

            # Phase 3: Configuration and theme commands
            if op_name == "config":
                handle_config_command(arg_parts)
                continue

            if op_name == "theme":
                handle_theme_command(arg_parts)
                continue

            if op_name == "export":
                handle_export_command(arg_parts)
                continue

            if op_name == "bookmark":
                handle_bookmark_command(arg_parts)
                continue

            # Phase 4: Performance monitoring
            if op_name == "perf":
                handle_perf_command(arg_parts)
                continue

            # Phase 4: Plotting operations (need special handling for string arguments)
            if op_name in ['plot', 'plot_data', 'plot_line', 'plot_bar']:
                handle_plot_command(op_name, arg_parts)
                continue

            # Handle regular operations
            arg_values = process_args(op_name, arg_parts)
            if arg_values is None:
                continue

            try:
                # Profile the operation execution
                from utils.performance import measure
                with measure(f"operation_{op_name}"):
                    result = plugin_manager.execute_operation(op_name, *arg_values)

                print_result(result)

                # Phase 4: Check for special numbers and easter eggs
                if enable_animations and preferences.animations_enabled:
                    from utils.animations import (
                        get_milestone_detector,
                        get_special_number_detector,
                        AnimationController
                    )

                    animation_controller = AnimationController(console, enable_animations)

                    # Check for easter eggs first (takes priority)
                    easter_egg_shown = animation_controller.check_and_show_easter_egg(result)

                    # Check for special numbers (if no easter egg)
                    if not easter_egg_shown:
                        special_detector = get_special_number_detector()
                        special_info = special_detector.check_number(result)
                        if special_info:
                            name, emoji = special_info
                            animation_controller.show_special_number(name, emoji, result)

                    # Check for calculation milestones
                    milestone_detector = get_milestone_detector()
                    milestone = milestone_detector.increment()
                    if milestone:
                        animation_controller.celebrate_milestone(milestone)

                # Store as the last result for reference
                last_result = result

                # Add to history
                history.add_entry(user_input, result)

            except ValueError as e:
                print_error(str(e), "Please check your input and try again")

        except KeyboardInterrupt:
            print_info("\nOperation interrupted")
        except EOFError:
            print_success("\nGoodbye! Thanks for using Math CLI")
            break
        except Exception as e:
            print_error(f"Unexpected error: {str(e)}",
                       "This might be a bug. Please report it if it persists")
