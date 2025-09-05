README.md

# Alibaba ECS Security Group Auto-IP Updater (`sg_auth`)

Keeps remote access **locked down** by allowing only *your* current public IP (/32) on an Alibaba Cloud **Security Group** and removing old/world-open rules.

**Your project specifics**
- Region: **me-central-1** (Riyadh)
- Security Group: **sg-l4vimuwylkiv6dk7jxc6**
- Port: **SSH (22/22)**
- CLI Profile: **sg_auth**

## Why this matters
Exposing SSH to `0.0.0.0/0` is risky. This tool enforces least privilege by updating a single `/32` rule whenever your IP changes.

## Quick start
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt


Run it:

python sg_auth.py --profile sg_auth


One-time cleanup (remove any world-open 22/22 rule):

python sg_auth.py --profile sg_auth --purge

Automate

Windows Task Scheduler (hourly): python C:\path\to\sg_auth.py --profile sg_auth

Linux/macOS cron: 0 * * * * /usr/bin/python3 /path/to/sg_auth.py --profile sg_auth

Proof (for recruiters)

Replaces 0.0.0.0/0 SSH with a strict /32 tied to your current IP.

Uses Alibaba CLI profile (no hardcoded keys).

Before/after verification via DescribeSecurityGroupAttribute.

Connectivity: Test-NetConnection <public-ip> -Port 22 (Windows) or nc -vz <ip> 22

Security notes

Never commit access keys. Use aliyun configure (CLI profile).

Prefer key-based SSH; disable passwords in /etc/ssh/sshd_config.

License

MIT — see LICENSE.


2) requirements.txt


aliyun-python-sdk-core>=2.13.0
aliyun-python-sdk-ecs>=4.24.0
requests>=2.28.0


3) .gitignore


.venv/
pycache/
*.py[cod]
.log
.DS_Store
.env
last_ip.txt


4) docs/USAGE.md
```markdown
# Usage

## Configure Alibaba CLI
```bash
aliyun configure
# profile name: sg_auth
# region: me-central-1

Run
python sg_auth.py --profile sg_auth
# optional one-time cleanup:
python sg_auth.py --profile sg_auth --purge

Test reachability

Windows:

Test-NetConnection -ComputerName <PUBLIC_IP> -Port 22


Linux/macOS:

nc -vz <PUBLIC_IP> 22


5) docs/TROUBLESHOOTING.md
```markdown
# Troubleshooting

- **Still can’t SSH**: ensure the instance has a public IP/EIP and that the attached SG is `sg-l4vimuwylkiv6dk7jxc6` in region `me-central-1`.
- **OS firewall**:
  - Ubuntu: `sudo ufw allow 22/tcp && sudo ufw reload`
  - CentOS: `sudo firewall-cmd --permanent --add-service=ssh && sudo firewall-cmd --reload`
- **Credentials warning**: remove any hardcoded keys in `mycred_acs.py`; use `aliyun configure list` to confirm profile.


docs/PROOF.md

# Proof

- Goal: automate least-privilege SSH on Alibaba ECS by keeping only current `/32`.
- Design: use CLI profile, add `/32` for 22/22, optional `--purge` to remove `0.0.0.0/0`, track last IP locally.
- Ops: cron/Task Scheduler; describe SG before/after.
- Evidence to include: SG screenshots before/after, connectivity check output, short demo GIF.


SECURITY.md

# Security

- Do not commit access keys. Use Alibaba CLI or env vars.
- Enforce `/32` on admin ports; remove `0.0.0.0/0`.
- Prefer key-based SSH; disable password auth.
- If secrets were exposed, rotate keys and scrub history before pushing.


LICENSE

MIT License
Copyright (c) 2025
Permission is hereby granted, free of charge, to any person obtaining a copy
... (standard MIT text is acceptable here) ...


(optional, nice to have) 9) .github/workflows/ci.yml
Create folders by typing the full path:

filename: .github/workflows/ci.yml

name: ci
on: [push, pull_request]
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: python -m pip install --upgrade pip ruff
      - run: ruff check .
