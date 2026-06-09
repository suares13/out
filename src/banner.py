import time
from src.colors import C

# Blocky double-border ASCII art for "OUT"
# Each line gets a different neon color for rainbow gradient effect
LOGO_LINES = [
    r" ██████╗ ██╗   ██╗████████╗",
    r"██╔═══██╗██║   ██║╚══██╔══╝",
    r"██║   ██║██║   ██║   ██║   ",
    r"██║   ██║██║   ██║   ██║   ",
    r"╚██████╔╝╚██████╔╝   ██║   ",
    r" ╚═════╝  ╚═════╝    ╚═╝   ",
]

GRADIENT = [
    C.RED,
    C.YELLOW,
    C.GREEN,
    C.CYAN,
    C.BLUE,
    C.MAGENTA,
]


def print_banner():
    width = 58

    print()
    # Logo with gradient
    for i, line in enumerate(LOGO_LINES):
        color = GRADIENT[i % len(GRADIENT)]
        centered = line.center(width)
        print(f"  {color}{C.BOLD}{centered}{C.RESET}")
        time.sleep(0.04)

    print()

    # Subtitle bar
    _box_line(f"{C.CYAN}[ DIGITAL EXPOSURE SCANNER ]{C.RESET}  {C.GREEN}v1.0{C.RESET}", width)
    _info_line("NODE: BR-SP-01", "UPLINK: ACTIVE", "🔴", width)
    _bottom_bar(width)

    print()


def _box_line(content, width):
    bar = "═" * (width - 2)
    print(f"  {C.CYAN_DIM}╔{bar}╗{C.RESET}")
    inner = f"  {C.CYAN_DIM}║{C.RESET}  {content}"
    print(inner)


def _info_line(left, right, icon, width):
    text = f"  {C.CYAN_DIM}║{C.RESET}  {C.YELLOW_DIM}{left}{C.RESET}  //  {C.GREEN_DIM}{right}{C.RESET}  {icon}"
    print(text)


def _bottom_bar(width):
    bar = "═" * (width - 2)
    print(f"  {C.CYAN_DIM}╚{bar}╝{C.RESET}")
