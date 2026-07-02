import os
import sys
import time
import re

# ANSI Color & Style Constants
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
UNDERLINE = "\033[4m"

# Foreground Colors
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"
BRIGHT_RED = "\033[91m"
BRIGHT_GREEN = "\033[92m"
BRIGHT_YELLOW = "\033[93m"
BRIGHT_BLUE = "\033[94m"
BRIGHT_CYAN = "\033[96m"

# Helper wrappers
def colorize(text, color, bold=False):
    style = BOLD if bold else ""
    return f"{style}{color}{text}{RESET}"

def red(text, b=False): return colorize(text, RED, b)
def green(text, b=False): return colorize(text, GREEN, b)
def yellow(text, b=False): return colorize(text, YELLOW, b)
def blue(text, b=False): return colorize(text, BLUE, b)
def magenta(text, b=False): return colorize(text, MAGENTA, b)
def cyan(text, b=False): return colorize(text, CYAN, b)
def white(text, b=False): return colorize(text, WHITE, b)
def bold(text): return f"{BOLD}{text}{RESET}"

# Try to reconfigure stdout to UTF-8 for nice block progress bars on Windows
try:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    BAR_CHAR = "█"
    EMPTY_CHAR = "░"
    # Test encoding compatibility
    BAR_CHAR.encode(sys.stdout.encoding or 'ascii')
except Exception:
    BAR_CHAR = "#"
    EMPTY_CHAR = "-"

# Typewriter printing that respects ANSI escape codes
ANSI_ESCAPE = re.compile(r'(\x1b\[[0-9;]*m)')

def type_print(text, delay=0.008, end='\n'):
    """Prints text character by character, writing ANSI escape sequences immediately."""
    parts = ANSI_ESCAPE.split(str(text))
    for part in parts:
        if ANSI_ESCAPE.match(part):
            sys.stdout.write(part)
            sys.stdout.flush()
        else:
            for char in part:
                # Fallback replacement if write encounters encoding error
                try:
                    sys.stdout.write(char)
                except UnicodeEncodeError:
                    if char == "█":
                        sys.stdout.write("#")
                    elif char == "░":
                        sys.stdout.write("-")
                    else:
                        sys.stdout.write("?")
                sys.stdout.flush()
                time.sleep(delay)
    sys.stdout.write(end)
    sys.stdout.flush()

def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def draw_bar(current, max_val, color_func, length=20, bar_char=None, empty_char=None):
    """Generates a colorized progress bar string."""
    if bar_char is None:
        bar_char = BAR_CHAR
    if empty_char is None:
        empty_char = EMPTY_CHAR
    percent = max(0, min(1, current / max_val))
    filled_len = int(round(length * percent))
    bar = bar_char * filled_len + empty_char * (length - filled_len)
    return color_func(f"[{bar}] {current}/{max_val}")

def health_bar(current, max_hp, length=20):
    ratio = current / max_hp if max_hp > 0 else 0
    if ratio > 0.5:
        color = green
    elif ratio > 0.2:
        color = yellow
    else:
        color = red
    return draw_bar(current, max_hp, color, length)

def mana_bar(current, max_mp, length=20):
    return draw_bar(current, max_mp, blue, length)

def xp_bar(current, max_xp, length=20):
    return draw_bar(current, max_xp, magenta, length)

def print_header(title, color=cyan):
    """Prints a styled header banner."""
    width = 60
    border = "=" * width
    type_print(color(border, True))
    type_print(color(title.center(width), True))
    type_print(color(border, True))

def print_box(lines, color=white):
    """Prints a list of strings inside a box border."""
    width = 58
    border = "+" + "-" * width + "+"
    type_print(color(border))
    for line in lines:
        type_print(color(f"| {line.ljust(width - 2)} |"))
    type_print(color(border))

def prompt_input(prompt_text, valid_choices=None):
    """Prompts player for input and optionally validates choices (case-insensitive)."""
    while True:
        try:
            sys.stdout.write(f"\n{prompt_text} ")
            sys.stdout.flush()
            user_input = input().strip()
            if not user_input:
                continue
            
            if valid_choices:
                # Convert choices to lowercase strings for matching
                choices_lower = [str(c).lower() for c in valid_choices]
                if user_input.lower() in choices_lower:
                    # Return the matching original choice
                    idx = choices_lower.index(user_input.lower())
                    return valid_choices[idx]
                else:
                    type_print(red(f"Invalid input. Choices: {', '.join(map(str, valid_choices))}"))
            else:
                return user_input
        except (KeyboardInterrupt, EOFError):
            type_print(red("\nGame interrupted. Exiting..."))
            sys.exit(0)
