README.md

# Alibaba ECS Security Group Auto-IP Updater (`sg_auth`)
![CI](https://github.com/Khadnaz/automate_sg/actions/workflows/ci.yml/badge.svg)

Keeps remote access **locked down** by allowing only *your* current public IP (/32) on an Alibaba Cloud **Security Group** and removing old/world-open rules.

**Your project specifics**
- Region: **me-central-1** (Riyadh)
- Security Group: **sg-l4vimuwylkiv6dk7jxc6**
- Port: **SSH (22/22)**
- CLI Profile: **sg_auth**

## Why this matters
Exposing SSH to `0.0.0.0/0` is risky. This tool enforces least privilege by updating a single `/32` rule whenever your IP changes.

## Quick start
# Alibaba ECS Security Group Auto-IP Updater (`sg_auth`)

Keep SSH locked down by allowing only *your* current public IP (/32) on an Alibaba Cloud **Security Group**—and removing old or world-open rules automatically.

**Project specifics**
- Region: me-central-1 (Riyadh)
- Security Group: sg-l4vimuwylkiv6dk7jxc6
- Port: SSH (22/22)
- CLI Profile: sg_auth

## Why
Exposing SSH to `0.0.0.0/0` is risky. This tool enforces least-privilege by updating a single `/32` rule when your IP changes and optionally purging world-open rules.

## Quick start

## Windows (PowerShell)
python -m venv .venv
. .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt

python sg_auth.py --profile sg_auth
python sg_auth.py --profile sg_auth --purge

## Automate
- Windows (Task Scheduler, hourly):
python C:\path\to\sg_auth.py --profile sg_auth

- Linux/macOS (cron):
0 * * * * /usr/bin/python3 /path/to/sg_auth.py --profile sg_auth

## Sanity checks
- Windows: Test-NetConnection -ComputerName <PUBLIC_IP> -Port 22

- macOS/Linux: nc -vz <PUBLIC_IP> 22

## How it works

1. Detects your current public IPv4.

2. (Optional --purge) Removes any 0.0.0.0/0 rule for port 22/22.

3. Adds an allow rule for yourIP/32 on 22/22.

4. Stores your last IP locally (last_ip.txt) so a new run can revoke the old /32.

## Security notes
- Never commit access keys. Use the Alibaba CLI profile (or env vars).

- Prefer key-based SSH; disable passwords in /etc/ssh/sshd_config.

## Repo structure
.
├─ sg_auth.py                 # updates the Security Group
├─ mycred_acs.py              # loads Alibaba CLI profile creds
├─ requirements.txt
├─ .gitignore
├─ .github/
│  └─ workflows/ci.yml        # CI (lint/sanity)
├─ docs/
│  └─ TROUBLESHOOTING.md
└─ LICENSE

## License

If you still see everything as one big grey block after pasting this, click “Raw” on GitHub to confirm the backticks are intact, then paste again.
::contentReference[oaicite:0]{index=0}
