#!/usr/bin/env python3

import sys
import time
import argparse
from src.banner import print_banner
from src.scanner import scan_email, scan_username, scan_domain
from src.display import print_results, print_error
from src.utils import validate_input

def main():
    parser = argparse.ArgumentParser(
        description="OUT — Digital Exposure Scanner",
        add_help=False
    )
    parser.add_argument("--email",    metavar="EMAIL",    help="Scan an email address")
    parser.add_argument("--username", metavar="USERNAME", help="Scan a username")
    parser.add_argument("--domain",   metavar="DOMAIN",   help="Scan a domain")
    parser.add_argument("--help", "-h", action="store_true")

    args = parser.parse_args()

    print_banner()

    if args.help or (not args.email and not args.username and not args.domain):
        print_usage()
        sys.exit(0)

    target, mode = validate_input(args)
    if not target:
        print_error("No valid target provided. Use --email, --username, or --domain.")
        sys.exit(1)

    if mode == "email":
        results = scan_email(target)
    elif mode == "username":
        results = scan_username(target)
    elif mode == "domain":
        results = scan_domain(target)

    print_results(results, target, mode)


def print_usage():
    from src.colors import C
    print(f"""
  {C.CYAN}USAGE:{C.RESET}
    python out.py --email    <email>
    python out.py --username <username>
    python out.py --domain   <domain>

  {C.CYAN}EXAMPLES:{C.RESET}
    python out.py --email    user@gmail.com
    python out.py --username h4cker99
    python out.py --domain   example.com
""")


if __name__ == "__main__":
    main()
