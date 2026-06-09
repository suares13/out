import re


def validate_input(args) -> tuple:
    """Returns (target, mode) or (None, None) if invalid."""

    if args.email:
        email = args.email.strip()
        if _is_valid_email(email):
            return email, "email"
        else:
            print(f"  Invalid email format: {email}")
            return None, None

    if args.username:
        username = args.username.strip()
        if username:
            return username, "username"

    if args.domain:
        domain = args.domain.strip().lower()
        if _is_valid_domain(domain):
            return domain, "domain"
        else:
            print(f"  Invalid domain format: {domain}")
            return None, None

    return None, None


def _is_valid_email(email: str) -> bool:
    pattern = r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def _is_valid_domain(domain: str) -> bool:
    pattern = r"^(?:[a-z0-9](?:[a-z0-9\-]{0,61}[a-z0-9])?\.)+[a-z]{2,}$"
    return bool(re.match(pattern, domain))
