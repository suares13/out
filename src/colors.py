class C:
    # Base colors
    RESET   = "\033[0m"
    BOLD    = "\033[1m"

    BLACK   = "\033[30m"
    RED     = "\033[91m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    BLUE    = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN    = "\033[96m"
    WHITE   = "\033[97m"

    # Dim variants
    RED_DIM    = "\033[31m"
    GREEN_DIM  = "\033[32m"
    YELLOW_DIM = "\033[33m"
    CYAN_DIM   = "\033[36m"

    # Background
    BG_RED    = "\033[41m"
    BG_GREEN  = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE   = "\033[44m"

    # Severity
    CRITICAL = "\033[91m"  # bright red
    HIGH     = "\033[93m"  # yellow
    MEDIUM   = "\033[96m"  # cyan
    LOW      = "\033[92m"  # green
    NONE     = "\033[37m"  # grey

    # Neon palette for the logo gradient
    NEON = [
        "\033[91m",  # red
        "\033[93m",  # yellow
        "\033[92m",  # green
        "\033[96m",  # cyan
        "\033[94m",  # blue
        "\033[95m",  # magenta
    ]
