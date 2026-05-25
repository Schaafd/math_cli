"""Autocompletion engine for math_cli using prompt_toolkit."""

from typing import Dict, List, Iterable
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.document import Document


class MathOperationCompleter(Completer):
    """Custom completer for math operations with parameter hints."""

    app_commands = {
        '/help': 'Show help and shortcuts',
        '/operations': 'Browse math operations',
        '/history': 'Show or manage history',
        '/settings': 'Open settings',
        '/themes': 'Open theme settings',
        '/sessions': 'Manage sessions',
        '/session': 'Session actions',
        '/bookmark': 'Bookmark actions',
        '/export': 'Export history',
        '/clear': 'Clear workspace',
        '/quit': 'Exit interactive mode',
        '/exit': 'Exit interactive mode',
    }

    def __init__(self, operations_metadata: Dict, session_manager=None):
        """Initialize the completer with operations metadata.

        Args:
            operations_metadata: Dictionary of operation name -> operation info
            session_manager: Optional SessionManager for session name completion
        """
        self.operations_metadata = operations_metadata
        self.operation_names = sorted(operations_metadata.keys())
        self.session_manager = session_manager

        self.special_commands = sorted(self.app_commands.keys())

    def get_completions(self, document: Document, complete_event) -> Iterable[Completion]:
        """Generate completions for the current input.

        Args:
            document: The current document/input
            complete_event: The completion event

        Yields:
            Completion objects for matching operations
        """
        # Get the text before the cursor
        text_before_cursor = document.text_before_cursor

        # Split into words
        words = text_before_cursor.split()

        # If we're at the start or after whitespace, complete operation names
        if not words or (text_before_cursor and text_before_cursor[-1].isspace()):
            return

        # Get the current word being typed
        current_word = words[-1].lower()

        # Slash commands are reserved for app/control actions.
        if len(words) == 1:
            if current_word.startswith('/'):
                for cmd, help_text in self.app_commands.items():
                    if cmd.startswith(current_word):
                        yield Completion(
                            cmd,
                            start_position=-len(current_word),
                            display=cmd,
                            display_meta=help_text
                        )
                return

            # Suggest operations
            for op_name in self.operation_names:
                if op_name.lower().startswith(current_word):
                    op_info = self.operations_metadata[op_name]
                    args_str = ' '.join(f'<{arg}>' for arg in op_info['args'])

                    # Add variadic indicator
                    if op_info.get('variadic', False):
                        args_str += ' ...'

                    display_meta = f"{args_str} - {op_info['help']}"

                    yield Completion(
                        op_name,
                        start_position=-len(current_word),
                        display=op_name,
                        display_meta=display_meta
                    )

        # For subsequent words, check for session name completion
        else:
            # Check if we're completing session names
            if self.session_manager and len(words) >= 2:
                first_word = words[0].lower()

                # Complete session names for slash session actions.
                if first_word == '/session' and len(words) >= 2 and words[1].lower() in ['open', 'delete']:

                    # Get all session names
                    session_names = self.session_manager.get_session_names()

                    for session_name in session_names:
                        if session_name.lower().startswith(current_word.lower()):
                            yield Completion(
                                session_name,
                                start_position=-len(current_word),
                                display=session_name,
                                display_meta="session"
                            )

            # Check if they're typing a new operation (for chain commands)
            for op_name in self.operation_names:
                if op_name.lower().startswith(current_word):
                    op_info = self.operations_metadata[op_name]
                    args_str = ' '.join(f'<{arg}>' for arg in op_info['args'])

                    if op_info.get('variadic', False):
                        args_str += ' ...'

                    display_meta = f"{args_str}"

                    yield Completion(
                        op_name,
                        start_position=-len(current_word),
                        display=op_name,
                        display_meta=display_meta
                    )

    def _get_special_command_help(self, command: str) -> str:
        """Get help text for special commands.

        Args:
            command: The special command name

        Returns:
            Help text for the command
        """
        help_texts = {
            **self.app_commands,
            'chain': 'Execute chained calculations',
        }
        return help_texts.get(command, '')


def get_fuzzy_matches(word: str, candidates: List[str], max_distance: int = 2) -> List[tuple]:
    """Find fuzzy matches for a word using Levenshtein distance.

    Args:
        word: The word to match
        candidates: List of candidate words
        max_distance: Maximum edit distance to consider

    Returns:
        List of (candidate, distance) tuples, sorted by distance
    """
    def levenshtein_distance(s1: str, s2: str) -> int:
        """Calculate Levenshtein distance between two strings."""
        if len(s1) < len(s2):
            return levenshtein_distance(s2, s1)

        if len(s2) == 0:
            return len(s1)

        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                # Cost of insertions, deletions, or substitutions
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row

        return previous_row[-1]

    matches = []
    word_lower = word.lower()

    for candidate in candidates:
        distance = levenshtein_distance(word_lower, candidate.lower())
        if distance <= max_distance:
            matches.append((candidate, distance))

    # Sort by distance (closest first)
    matches.sort(key=lambda x: x[1])

    return matches


def suggest_corrections(unknown_op: str, operations_metadata: Dict, max_suggestions: int = 3) -> List[str]:
    """Suggest corrections for an unknown operation.

    Args:
        unknown_op: The unknown operation name
        operations_metadata: Dictionary of valid operations
        max_suggestions: Maximum number of suggestions to return

    Returns:
        List of suggested operation names
    """
    # Get fuzzy matches with a reasonable max distance
    max_distance = min(3, max(1, len(unknown_op) // 3))
    matches = get_fuzzy_matches(unknown_op, list(operations_metadata.keys()), max_distance=max_distance)

    # Also check for prefix matches (higher priority)
    prefix_matches = [
        op for op in operations_metadata.keys()
        if op.lower().startswith(unknown_op[:3].lower()) and len(unknown_op) >= 3
    ]

    # Check for substring matches (also useful)
    substring_matches = [
        op for op in operations_metadata.keys()
        if unknown_op.lower() in op.lower() and op not in prefix_matches
    ]

    # Combine and deduplicate, prioritizing close matches
    suggestions = []

    # Add very close fuzzy matches first (distance <= 2)
    for match, distance in matches:
        if distance <= 2 and match not in suggestions and len(suggestions) < max_suggestions:
            suggestions.append(match)

    # Add prefix matches
    for match in prefix_matches[:max_suggestions]:
        if match not in suggestions and len(suggestions) < max_suggestions:
            suggestions.append(match)

    # Add remaining fuzzy matches
    for match, distance in matches:
        if match not in suggestions and len(suggestions) < max_suggestions:
            suggestions.append(match)

    # Add substring matches as last resort
    for match in substring_matches[:max_suggestions]:
        if match not in suggestions and len(suggestions) < max_suggestions:
            suggestions.append(match)

    return suggestions[:max_suggestions]


def get_parameter_hint(operation: str, operations_metadata: Dict) -> str:
    """Get a parameter hint string for an operation.

    Args:
        operation: The operation name
        operations_metadata: Dictionary of operation metadata

    Returns:
        A formatted parameter hint string
    """
    if operation not in operations_metadata:
        return ""

    op_info = operations_metadata[operation]
    args = op_info['args']

    if not args:
        return f"{operation} - {op_info['help']}"

    args_str = ' '.join(f'<{arg}>' for arg in args)

    if op_info.get('variadic', False):
        args_str += ' ...'

    return f"{operation} {args_str} - {op_info['help']}"
