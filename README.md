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
```bash
python -m venv .venv && source .venv/bin/activate    # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python sg_auth.py --profile sg_auth           # add your current /32
python sg_auth.py --profile sg_auth --purge   # (one-time) remove 0.0.0.0/0 on 22

Automate

Windows Task Scheduler (hourly): python C:\path\to\sg_auth.py --profile sg_auth

Linux/macOS cron: 0 * * * * /usr/bin/python3 /path/to/sg_auth.py --profile sg_auth

Docs

Usage: docs/USAGE.md

Troubleshooting: docs/TROUBLESHOOTING.md

Proof for recruiters (what to screenshot): docs/PROOF.md

Security notes

Don’t commit access keys. Use aliyun configure (CLI profile).

Prefer key-based SSH; disable passwords in /etc/ssh/sshd_config.

License

MIT — see LICENSE
.


Then add the missing files (website → Add file → Create new file):

requirements.txt


aliyun-python-sdk-core>=2.13.0
aliyun-python-sdk-ecs>=4.24.0
requests>=2.28.0


.gitignore


.venv/
pycache/
*.py[cod]
.log
.DS_Store
.env
last_ip.txt


docs/USAGE.md

Usage

aliyun configure # profile: sg_auth, region: me-central-1
python sg_auth.py --profile sg_auth
python sg_auth.py --profile sg_auth --purge # one-time cleanup
Windows: Test-NetConnection -ComputerName <PUBLIC_IP> -Port 22
macOS/Linux: nc -vz <PUBLIC_IP> 22


docs/TROUBLESHOOTING.md


Ensure instance has a public IP/EIP and the attached SG is sg-l4vimuwylkiv6dk7jxc6 in me-central-1.

OS firewall:

Ubuntu: sudo ufw allow 22/tcp && sudo ufw reload

CentOS: sudo firewall-cmd --permanent --add-service=ssh && sudo firewall-cmd --reload

Remove any hardcoded keys from mycred_acs.py; use aliyun configure list.


docs/PROOF.md


Before/after SG screenshots (22/22: 0.0.0.0/0 → your /32).

Connectivity check screenshot.

Short note on least-privilege + purge logic.


If you want, I can give you a tiny “Topics” list and a one-liner for your CV once you push those files.
::contentReference[oaicite:1]{index=1}
