# Usage

## Configure Alibaba CLI
aliyun configure
# profile name: sg_auth
# region: me-central-1

## Run
python sg_auth.py --profile sg_auth
# one-time cleanup:
python sg_auth.py --profile sg_auth --purge

## Test reachability
Windows:  Test-NetConnection -ComputerName <PUBLIC_IP> -Port 22
Linux/macOS:  nc -vz <PUBLIC_IP> 22
