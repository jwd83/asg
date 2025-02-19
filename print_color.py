# my simple color print function
def print_color(color: str, text: str):

    # ANSI escape codes for colors
    ANSI = {
        "RED": "\033[31m",
        "GREEN": "\033[32m",
        "YELLOW": "\033[33m",
        "BLUE": "\033[34m",
        "MAGENTA": "\033[35m",
        "RESET": "\033[0m",
    }

    if color not in ANSI:
        print(f"{text}")
    else:
        print(f"{ANSI[color]}{text}{ANSI['RESET']}")
