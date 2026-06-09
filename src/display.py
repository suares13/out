import time
import sys
from src.colors import C

WIDTH = 58


def print_scanning(label: str):
    """Animated scanning line."""
    frames = ["▏", "▎", "▍", "▌", "▋", "▊", "▉", "█"]
    sys.stdout.write(f"  {C.CYAN_DIM}►{C.RESET} {C.WHITE}{label:<20}{C.RESET} ")
    sys.stdout.flush()
    for f in frames:
        sys.stdout.write(f"\b{C.YELLOW}{f}{C.RESET}")
        sys.stdout.flush()
        time.sleep(0.04)
    sys.stdout.write(f"\b{C.GREEN}✓{C.RESET}\n")
    sys.stdout.flush()


def print_scan_line(label: str, value: str, severity: str = "none"):
    color = {
        "critical": C.CRITICAL,
        "high":     C.HIGH,
        "medium":   C.MEDIUM,
        "low":      C.LOW,
        "none":     C.NONE,
    }.get(severity, C.NONE)

    print(f"  {C.CYAN_DIM}►{C.RESET} {C.WHITE}{label:<20}{C.RESET} {color}{value}{C.RESET}")


def print_results(results: dict, target: str, mode: str):
    score   = results.get("score", 0)
    s_color = _score_color(score)
    s_label = _score_label(score)

    print()
    _divider("TARGET")
    print(f"  {C.CYAN}✉{C.RESET}  {C.WHITE}{target}{C.RESET}")
    print()

    _divider("RESULTS")

    if mode == "email":
        _print_email_results(results)
    elif mode == "username":
        _print_username_results(results)
    elif mode == "domain":
        _print_domain_results(results)

    print()
    _divider("VERDICT")
    _print_score_bar(score, s_color, s_label)
    print()
    _print_explanation(results, mode, score)
    print()
    _divider("ACTIONS")
    _print_actions(results, mode)
    print()


def _print_email_results(results: dict):
    breaches = results.get("breaches", [])
    pastes   = results.get("pastes", [])
    pw       = results.get("password_exposed", False)
    social   = results.get("social", [])

    # Breaches
    if breaches:
        sev = "critical" if len(breaches) >= 3 else "high"
        bar = _mini_bar(min(len(breaches) * 2, 10), 10)
        names = ", ".join(b["name"] for b in breaches[:3])
        suffix = f" +{len(breaches)-3} more" if len(breaches) > 3 else ""
        print_scan_line("BREACHES", f"{bar}  {len(breaches)} found  [{names}{suffix}]", sev)
    else:
        print_scan_line("BREACHES", f"{'░' * 10}  None found", "none")

    # Pastes
    if pastes:
        bar = _mini_bar(min(len(pastes) * 3, 10), 10)
        print_scan_line("PASTES", f"{bar}  {len(pastes)} occurrence(s)", "high")
    else:
        print_scan_line("PASTES", f"{'░' * 10}  None found", "none")

    # Password
    if pw:
        print_scan_line("PASSWORDS", f"{'█' * 6}{'░' * 4}  Hash exposed", "critical")
    else:
        print_scan_line("PASSWORDS", f"{'░' * 10}  Not found in leaks", "none")

    # Social
    if social:
        names = "  ·  ".join(s["platform"] for s in social)
        bar   = _mini_bar(min(len(social) * 2, 10), 10)
        print_scan_line("SOCIAL", f"{bar}  {names}", "low")
    else:
        print_scan_line("SOCIAL", f"{'░' * 10}  No profiles found", "none")


def _print_username_results(results: dict):
    social = results.get("social", [])
    if social:
        for s in social:
            print_scan_line(s["platform"], s["url"], "low")
    else:
        print_scan_line("SOCIAL", "No public profiles found", "none")


def _print_domain_results(results: dict):
    dns   = results.get("dns", {})
    ports = results.get("open_ports", [])

    if dns.get("resolved"):
        print_scan_line("IP ADDRESS", dns["ip"], "medium")
    else:
        print_scan_line("IP ADDRESS", "Could not resolve", "none")

    if ports:
        sev = "high" if len(ports) >= 4 else "medium"
        bar = _mini_bar(min(len(ports) * 2, 10), 10)
        print_scan_line("OPEN PORTS", f"{bar}  {', '.join(map(str, ports))}", sev)
    else:
        print_scan_line("OPEN PORTS", "None detected", "none")


def _print_score_bar(score: int, color: str, label: str):
    filled = int(score / 10)
    empty  = 10 - filled
    bar    = f"{'▓' * filled}{'░' * empty}"

    print(f"  ┌{'─' * (WIDTH - 4)}┐")
    print(f"  │  SCORE  {color}{score:>3}/100{C.RESET}   {color}{bar}{C.RESET}   {color}{C.BOLD}{label}{C.RESET}")
    print(f"  └{'─' * (WIDTH - 4)}┘")


def _print_explanation(results: dict, mode: str, score: int):
    lines = []

    if mode == "email":
        breaches = results.get("breaches", [])
        pw       = results.get("password_exposed", False)

        if breaches:
            lines.append(
                f"  Your data appeared in {C.YELLOW}{len(breaches)} known breach(es){C.RESET}."
            )
        if pw:
            lines.append(
                f"  {C.RED}A hash tied to your email was found in password leak databases.{C.RESET}"
            )
            lines.append(
                f"  This means old passwords may be circulating in credential markets."
            )
        if score < 20:
            lines.append(
                f"  {C.GREEN}Your digital footprint looks clean. Keep it that way.{C.RESET}"
            )

    elif mode == "domain":
        ports = results.get("open_ports", [])
        if len(ports) >= 4:
            lines.append(
                f"  {C.RED}Many open ports detected.{C.RESET} Reduces your attack surface by closing unused services."
            )
        elif ports:
            lines.append(
                f"  Some open ports found. Review if all services are necessary."
            )

    elif mode == "username":
        social = results.get("social", [])
        if len(social) >= 4:
            lines.append(
                f"  Your username appears on {C.YELLOW}{len(social)} platforms{C.RESET}. "
                f"High visibility — consider if all accounts are still in use."
            )

    for line in lines:
        print(line)


def _print_actions(results: dict, mode: str):
    if mode == "email":
        breaches = results.get("breaches", [])
        pw       = results.get("password_exposed", False)

        if breaches:
            print(f"  {C.YELLOW}→{C.RESET} Change passwords for affected services")
            print(f"  {C.YELLOW}→{C.RESET} Enable 2FA on any account from those breaches")
        if pw:
            print(f"  {C.RED}→{C.RESET} Stop reusing old passwords immediately")
        if not breaches and not pw:
            print(f"  {C.GREEN}→{C.RESET} You're in good shape — consider running this monthly")

    elif mode == "domain":
        ports = results.get("open_ports", [])
        if ports:
            print(f"  {C.YELLOW}→{C.RESET} Review firewall rules for ports: {', '.join(map(str, ports))}")
            print(f"  {C.YELLOW}→{C.RESET} Disable any service you don't actively need")

    elif mode == "username":
        social = results.get("social", [])
        if social:
            print(f"  {C.CYAN}→{C.RESET} Audit inactive accounts and consider deleting them")


def print_error(msg: str):
    print(f"\n  {C.RED}[ERROR]{C.RESET} {msg}\n")


# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────

def _divider(label: str = ""):
    if label:
        pad = WIDTH - len(label) - 3
        print(f"  {C.CYAN_DIM}{label} {'─' * pad}{C.RESET}")
    else:
        print(f"  {C.CYAN_DIM}{'─' * WIDTH}{C.RESET}")


def _mini_bar(filled: int, total: int) -> str:
    return f"{'█' * filled}{'░' * (total - filled)}"


def _score_color(score: int) -> str:
    if score >= 70: return C.RED
    if score >= 40: return C.YELLOW
    return C.GREEN


def _score_label(score: int) -> str:
    if score >= 70: return "⚠  HIGH EXPOSURE"
    if score >= 40: return "~  MODERATE EXPOSURE"
    if score >= 10: return "·  LOW EXPOSURE"
    return "✓  CLEAN"
