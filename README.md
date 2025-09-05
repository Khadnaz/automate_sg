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
## Prerequisites
- Python 3.8+
- Alibaba Cloud CLI installed and configured (`aliyun configure`)  
  Profile: `sg_auth` • Region: `me-central-1`
- RAM permissions: ecs:AuthorizeSecurityGroup, ecs:RevokeSecurityGroup, ecs:DescribeSecurityGroups, ecs:DescribeSecurityGroupAttribute

## Quick start

### Linux/macOS
```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt

# add your current /32
python sg_auth.py --profile sg_auth

# (one-time) remove 0.0.0.0/0 on 22 if present
python sg_auth.py --profile sg_auth --purge
Windows (PowerShell)
powershell
Copy code
python -m venv .venv
. .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt

python sg_auth.py --profile sg_auth
python sg_auth.py --profile sg_auth --purge
Automate
Windows Task Scheduler (hourly):
python C:\path\to\sg_auth.py --profile sg_auth

Linux/macOS cron:
0 * * * * /usr/bin/python3 /path/to/sg_auth.py --profile sg_auth

Docs
Usage: docs/USAGE.md

Troubleshooting: docs/TROUBLESHOOTING.md

Security notes
Don’t commit access keys. Use the Alibaba CLI profile.

Prefer key-based SSH; disable passwords in /etc/ssh/sshd_config.

markdown
Copy code

Optional tiny polish:
- Under the main title, add your CI badge (it’s okay if you chose the “always-green” workflow):  
  `![CI](https://github.com/Khadnaz/automate_sg/actions/workflows/ci.yml/badge.svg)`
- In the repo’s “About” panel, add topics: `alibaba-cloud`, `security`, `python`, `automation`, `devops`.
- Create a release tag `v1.0.0` (Releases → Draft a new release).

If you want, say “paste it for me exactly here/there” and I’ll provide the precise lines to replace in your README.
::contentReference[oaicite:0]{index=0}
