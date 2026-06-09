# OUT — Digital Exposure Scanner

```
 ██████╗ ██╗   ██╗████████╗
██╔═══██╗██║   ██║╚══██╔══╝
██║   ██║██║   ██║   ██║   
██║   ██║██║   ██║   ██║   
╚██████╔╝╚██████╔╝   ██║   
 ╚═════╝  ╚═════╝    ╚═╝   
```

**OUT** scans the digital footprint of an email, username, or domain and tells you — in plain language — how exposed that identity is on the internet.

Built for security professionals and non-technical users alike: the output is readable by anyone, but the data underneath is real.

---

## Install

```bash
git clone https://github.com/suares13/out
cd out
pip install -r requirements.txt
```

No API key required. All data sources are free and public.

---

## Usage

```bash
# Scan an email address
python out.py --email user@gmail.com

# Scan a username across social platforms
python out.py --username h4cker99

# Scan a domain (DNS + open ports)
python out.py --domain example.com
```

---

## What it checks

| Mode         | Checks                                                                      |
|--------------|-----------------------------------------------------------------------------|
| `--email`    | Data breaches (XposedOrNot), paste sites, password hash leaks, social presence |
| `--username` | Presence on GitHub, Twitter/X, Reddit, HackerNews, Dev.to, Medium          |
| `--domain`   | DNS resolution, common open ports                                           |

---

## Output example

```
TARGET ──────────────────────────────────────────────
✉  user@gmail.com

RESULTS ─────────────────────────────────────────────
► BREACHES            ████████░░  3 found  [LinkedIn, Adobe, Canva]
► PASTES              ███░░░░░░░  1 occurrence(s)
► PASSWORDS           ██████░░░░  Hash exposed
► SOCIAL              ████░░░░░░  GitHub  ·  Reddit

VERDICT ─────────────────────────────────────────────
┌──────────────────────────────────────────────────┐
│  SCORE   74/100   ▓▓▓▓▓▓▓░░░   ⚠  HIGH EXPOSURE  │
└──────────────────────────────────────────────────┘

Your data appeared in 3 known breach(es).
A hash tied to your email was found in password leak databases.
This means old passwords may be circulating in credential markets.
```

---

## Project structure

```
out/
├── out.py              # Entry point
├── requirements.txt
├── src/
│   ├── banner.py       # ASCII logo + header display
│   ├── colors.py       # ANSI color constants
│   ├── scanner.py      # Core scan logic (XposedOrNot, social, DNS, ports)
│   ├── display.py      # Output formatting
│   └── utils.py        # Input validation
```

---

## Upgrade roadmap

- [ ] `--export txt` — save report as formatted text file
- [ ] `--watch` mode — re-scan periodically and alert on changes
- [ ] VirusTotal / URLhaus integration for domain mode
- [ ] SPF / DKIM / DMARC checks for email domain
- [ ] Local cache to compare exposure over time
- [ ] `--batch` mode — scan a list of targets from file
- [ ] Shodan API integration for deeper domain recon

---

## Disclaimer

OUT is an educational tool for personal security awareness and authorized security assessments only. Do not use it on targets you don't own or have explicit permission to scan.

---

Made by [@suares13](https://github.com/suares13)
