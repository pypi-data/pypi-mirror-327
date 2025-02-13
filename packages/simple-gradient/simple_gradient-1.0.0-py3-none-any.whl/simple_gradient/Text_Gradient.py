import colorama
from colorama import Fore, Style

# Inicializa o Colorama
colorama.init()

def rgb_to_ansi(r, g, b):
    """Converte um valor RGB para um código ANSI de 24 bits."""
    return f'\033[38;2;{r};{g};{b}m'

def apply_gradient(text, rgb_start, rgb_end):
    """Aplica um degradê entre duas cores RGB em uma string."""
    lines = text.split("\n")
    max_length = max(len(line) for line in lines)
    colored_lines = []
    
    for i, line in enumerate(lines):
        colored_line = ""
        for j, char in enumerate(line):
            ratio = j / (max_length - 1) if max_length > 1 else 0
            r = int(rgb_start[0] + (rgb_end[0] - rgb_start[0]) * ratio)
            g = int(rgb_start[1] + (rgb_end[1] - rgb_start[1]) * ratio)
            b = int(rgb_start[2] + (rgb_end[2] - rgb_start[2]) * ratio)
            
            colored_line += rgb_to_ansi(r, g, b) + char
        colored_lines.append(colored_line)
    
    return "\n".join(colored_lines) + Style.RESET_ALL
