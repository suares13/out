import time
import socket
import requests
import hashlib
import urllib.parse
from src.display import print_scan_line, print_scanning
from src.colors import C

HEADERS = {
    "User-Agent": "OUT-Scanner/1.0 (educational tool)"
}


# ─────────────────────────────────────────────
#  EMAIL SCAN
# ─────────────────────────────────────────────

def scan_email(email: str) -> dict:
    results = {
        "mode": "email",
        "target": email,
        "breaches": [],
        "pastes": [],
        "password_exposed": False,
        "social": [],
        "score": 0,
        "checks": {}
    }

    print_scanning("BREACHES")
    breaches = _check_hibp_breaches(email)
    results["breaches"] = breaches
    results["checks"]["breaches"] = len(breaches)
    time.sleep(0.3)

    print_scanning("PASTES")
    pastes = _check_hibp_pastes(email)
    results["pastes"] = pastes
    results["checks"]["pastes"] = len(pastes)
    time.sleep(0.3)

    print_scanning("PASSWORD HASH")
    pw_exposed = _check_password_hash(email)
    results["password_exposed"] = pw_exposed
    results["checks"]["password"] = pw_exposed
    time.sleep(0.3)

    print_scanning("SOCIAL PRESENCE")
    username = email.split("@")[0]
    social = _check_social_presence(username)
    results["social"] = social
    results["checks"]["social"] = len(social)
    time.sleep(0.3)

    results["score"] = _calculate_score(results)
    return results


# ─────────────────────────────────────────────
#  USERNAME SCAN
# ─────────────────────────────────────────────

def scan_username(username: str) -> dict:
    results = {
        "mode": "username",
        "target": username,
        "social": [],
        "score": 0,
        "checks": {}
    }

    print_scanning("SOCIAL PRESENCE")
    social = _check_social_presence(username)
    results["social"] = social
    results["checks"]["social"] = len(social)
    time.sleep(0.3)

    results["score"] = _calculate_score(results)
    return results


# ─────────────────────────────────────────────
#  DOMAIN SCAN
# ─────────────────────────────────────────────

def scan_domain(domain: str) -> dict:
    results = {
        "mode": "domain",
        "target": domain,
        "dns": {},
        "open_ports": [],
        "score": 0,
        "checks": {}
    }

    print_scanning("DNS LOOKUP")
    dns = _check_dns(domain)
    results["dns"] = dns
    results["checks"]["dns"] = bool(dns)
    time.sleep(0.3)

    print_scanning("COMMON PORTS")
    ports = _check_common_ports(domain)
    results["open_ports"] = ports
    results["checks"]["ports"] = len(ports)
    time.sleep(0.3)

    results["score"] = _calculate_score(results)
    return results


# ─────────────────────────────────────────────
#  INTERNAL HELPERS
# ─────────────────────────────────────────────

def _check_hibp_breaches(email: str) -> list:
    """Query XposedOrNot for breach data — no API key required."""
    try:
        encoded = urllib.parse.quote(email)
        url = f"https://api.xposedornot.com/v1/check-email/{encoded}"
        r = requests.get(url, headers=HEADERS, timeout=6)
        if r.status_code == 200:
            data = r.json()
            # XposedOrNot returns {"breaches": [["BreachName", ...], ...]} or {"Error": "Not found"}
            raw = data.get("breaches", [])
            if not raw:
                return []
            # Each item in the list is a breach name string
            breaches = []
            for item in raw:
                if isinstance(item, list):
                    for name in item:
                        breaches.append({"name": str(name), "year": "?", "data": []})
                elif isinstance(item, str):
                    breaches.append({"name": item, "year": "?", "data": []})
            return breaches
        elif r.status_code == 404:
            return []
        else:
            return []
    except Exception:
        return []


def _check_hibp_pastes(email: str) -> list:
    """Query XposedOrNot for paste exposure — no API key required."""
    try:
        encoded = urllib.parse.quote(email)
        url = f"https://api.xposedornot.com/v1/check-email/{encoded}"
        r = requests.get(url, headers=HEADERS, timeout=6)
        if r.status_code == 200:
            data = r.json()
            # XposedOrNot includes paste count in the same response
            paste_count = data.get("paste_count", 0) or 0
            return [{"source": "XposedOrNot"}] * int(paste_count)
        return []
    except Exception:
        return []


def _check_password_hash(email: str) -> bool:
    """
    Checks if any common derivation of the email appears in HIBP Pwned Passwords.
    Uses k-anonymity model — only sends first 5 chars of SHA1 hash.
    This checks the email itself as a string, not an actual password.
    """
    try:
        sha1 = hashlib.sha1(email.encode()).hexdigest().upper()
        prefix, suffix = sha1[:5], sha1[5:]
        r = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}", timeout=5)
        if r.status_code == 200:
            for line in r.text.splitlines():
                h, count = line.split(":")
                if h == suffix:
                    return True
        return False
    except Exception:
        return False


def _check_social_presence(username: str) -> list:
    """
    Checks a curated list of platforms for username existence
    via HTTP HEAD requests. No scraping, no auth.
    """
    platforms = {
        "GitHub":    f"https://github.com/{username}",
        "Twitter/X": f"https://x.com/{username}",
        "Reddit":    f"https://www.reddit.com/user/{username}",
        "HackerNews":f"https://news.ycombinator.com/user?id={username}",
        "Dev.to":    f"https://dev.to/{username}",
        "Medium":    f"https://medium.com/@{username}",
    }

    found = []
    for platform, url in platforms.items():
        try:
            r = requests.head(url, headers=HEADERS, timeout=4, allow_redirects=True)
            if r.status_code == 200:
                found.append({"platform": platform, "url": url})
        except Exception:
            pass

    return found


def _check_dns(domain: str) -> dict:
    """Basic DNS resolution."""
    try:
        ip = socket.gethostbyname(domain)
        return {"ip": ip, "resolved": True}
    except Exception:
        return {"ip": None, "resolved": False}


def _check_common_ports(domain: str) -> list:
    """Light port scan on common ports."""
    ports_to_check = [21, 22, 25, 80, 443, 3306, 8080, 8443]
    open_ports = []
    for port in ports_to_check:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((domain, port))
            if result == 0:
                open_ports.append(port)
            sock.close()
        except Exception:
            pass
    return open_ports


# ─────────────────────────────────────────────
#  SCORING
# ─────────────────────────────────────────────

def _calculate_score(results: dict) -> int:
    score = 0
    checks = results.get("checks", {})

    breach_count = checks.get("breaches", 0)
    if breach_count >= 5:   score += 40
    elif breach_count >= 3: score += 30
    elif breach_count >= 1: score += 20

    paste_count = checks.get("pastes", 0)
    if paste_count >= 3:    score += 20
    elif paste_count >= 1:  score += 10

    if checks.get("password", False):
        score += 25

    social_count = checks.get("social", 0)
    if social_count >= 4:   score += 15
    elif social_count >= 2: score += 8
    elif social_count >= 1: score += 3

    port_count = checks.get("ports", 0)
    if port_count >= 4:     score += 20
    elif port_count >= 2:   score += 10
    elif port_count >= 1:   score += 5

    return min(score, 100)
