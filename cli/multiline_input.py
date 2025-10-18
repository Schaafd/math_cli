"""Multi-line input handling for Math CLI."""

from typing import List, Tuple, Optional


class MultilineDetector:
    """Detect when input should continue on multiple lines."""

    def __init__(self):
        """Initialize the multiline detector."""
        self.brackets = {'(': ')', '[': ']', '{': '}'}
        self.opening = set(self.brackets.keys())
        self.closing = set(self.brackets.values())

    def needs_continuation(self, text: str) -> Tuple[bool, str]:
        """Check if input needs continuation on next line.

        Args:
            text: Current input text

        Returns:
            Tuple of (needs_continuation, reason)
        """
        # Check for explicit continuation with backslash
        if text.rstrip().endswith('\\'):
            return True, "explicit_continuation"

        # Check for unclosed brackets
        bracket_info = self._check_brackets(text)
        if bracket_info['unclosed']:
            return True, f"unclosed_{bracket_info['type']}"

        # Check for pipe in chain command (might want more)
        if text.strip().startswith('chain') and text.rstrip().endswith('|'):
            return True, "chain_continuation"

        return False, ""

    def _check_brackets(self, text: str) -> dict:
        """Check bracket matching in text.

        Args:
            text: Text to check

        Returns:
            Dictionary with bracket information
        """
        stack = []
        unclosed = []

        for char in text:
            if char in self.opening:
                stack.append(char)
            elif char in self.closing:
                if stack:
                    opener = stack.pop()
                    # Check if they match
                    if self.brackets[opener] != char:
                        unclosed.append((opener, char))
                else:
                    # Closing bracket with no opener
                    unclosed.append(('', char))

        # Add any unclosed opening brackets
        unclosed.extend([(b, '') for b in stack])

        bracket_type = ""
        if stack:
            bracket_type = stack[-1]

        return {
            'unclosed': len(stack) > 0 or any(u[1] == '' for u in unclosed),
            'type': bracket_type,
            'count': len(stack),
            'mismatched': any(u[0] != '' and u[1] != '' for u in unclosed)
        }

    def get_continuation_prompt(self, reason: str, line_number: int = 2) -> str:
        """Get the appropriate continuation prompt.

        Args:
            reason: Reason for continuation
            line_number: Current line number

        Returns:
            Continuation prompt string
        """
        if reason == "explicit_continuation":
            return f"... "
        elif reason.startswith("unclosed_"):
            bracket = reason.split('_')[1]
            return f"... "
        elif reason == "chain_continuation":
            return "... "
        else:
            return f"{line_number:3d} "


class BracketMatcher:
    """Visual bracket matching for multi-line input."""

    def __init__(self):
        """Initialize bracket matcher."""
        self.brackets = {'(': ')', '[': ']', '{': '}'}

    def highlight_matching_brackets(self, text: str, cursor_pos: int) -> List[int]:
        """Find matching bracket positions for highlighting.

        Args:
            text: Input text
            cursor_pos: Current cursor position

        Returns:
            List of positions to highlight
        """
        if cursor_pos < 0 or cursor_pos >= len(text):
            return []

        char = text[cursor_pos]

        # Check if cursor is on a bracket
        if char in self.brackets:
            # Opening bracket - find closing
            match_pos = self._find_closing_bracket(text, cursor_pos)
            if match_pos is not None:
                return [cursor_pos, match_pos]
        elif char in self.brackets.values():
            # Closing bracket - find opening
            match_pos = self._find_opening_bracket(text, cursor_pos)
            if match_pos is not None:
                return [cursor_pos, match_pos]

        return []

    def _find_closing_bracket(self, text: str, open_pos: int) -> Optional[int]:
        """Find the matching closing bracket.

        Args:
            text: Input text
            open_pos: Position of opening bracket

        Returns:
            Position of closing bracket or None
        """
        opener = text[open_pos]
        closer = self.brackets[opener]
        count = 1
        pos = open_pos + 1

        while pos < len(text) and count > 0:
            if text[pos] == opener:
                count += 1
            elif text[pos] == closer:
                count -= 1
                if count == 0:
                    return pos
            pos += 1

        return None

    def _find_opening_bracket(self, text: str, close_pos: int) -> Optional[int]:
        """Find the matching opening bracket.

        Args:
            text: Input text
            close_pos: Position of closing bracket

        Returns:
            Position of opening bracket or None
        """
        closer = text[close_pos]
        opener = None
        for o, c in self.brackets.items():
            if c == closer:
                opener = o
                break

        if opener is None:
            return None

        count = 1
        pos = close_pos - 1

        while pos >= 0 and count > 0:
            if text[pos] == closer:
                count += 1
            elif text[pos] == opener:
                count -= 1
                if count == 0:
                    return pos
            pos -= 1

        return None


def format_multiline_input(lines: List[str], show_line_numbers: bool = True) -> str:
    """Format multi-line input for display.

    Args:
        lines: List of input lines
        show_line_numbers: Whether to show line numbers

    Returns:
        Formatted string
    """
    if not lines:
        return ""

    if not show_line_numbers:
        return '\n'.join(lines)

    # Calculate line number width
    width = len(str(len(lines)))

    formatted = []
    for i, line in enumerate(lines, 1):
        formatted.append(f"{i:>{width}d} │ {line}")

    return '\n'.join(formatted)


def collect_multiline_input(prompt: str = "❯ ",
                            continuation_prompt: str = "... ",
                            enable_colors: bool = True) -> str:
    """Collect multi-line input from user.

    Args:
        prompt: Initial prompt
        continuation_prompt: Continuation prompt
        enable_colors: Whether colors are enabled

    Returns:
        Complete multi-line input as single string
    """
    detector = MultilineDetector()
    lines = []

    # First line
    try:
        line = input(prompt)
        lines.append(line)

        # Check if we need continuation
        while True:
            needs_cont, reason = detector.needs_continuation(' '.join(lines))

            if not needs_cont:
                break

            # Get continuation
            cont_prompt = detector.get_continuation_prompt(reason, len(lines) + 1)
            try:
                next_line = input(cont_prompt)
                # Remove trailing backslash if present
                if lines[-1].rstrip().endswith('\\'):
                    lines[-1] = lines[-1].rstrip()[:-1].rstrip()
                lines.append(next_line)
            except EOFError:
                break

    except EOFError:
        return ""

    # Join lines into single command
    return ' '.join(lines)


def validate_brackets(text: str) -> Tuple[bool, str]:
    """Validate bracket matching in text.

    Args:
        text: Text to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    detector = MultilineDetector()
    info = detector._check_brackets(text)

    if info['mismatched']:
        return False, "Mismatched brackets detected"
    elif info['unclosed']:
        return False, f"Unclosed bracket: '{info['type']}'"

    return True, ""
