# Troubleshooting
- Ensure the instance has a public IP/EIP.
- The attached Security Group should be sg-l4vimuwylkiv6dk7jxc6 in region me-central-1.
- OS firewall:
  - Ubuntu: sudo ufw allow 22/tcp && sudo ufw reload
  - CentOS: sudo firewall-cmd --permanent --add-service=ssh && sudo firewall-cmd --reload
- If you ever saw a "hardcoded credentials" warning, remove any keys from mycred_acs.py and use `aliyun configure`.
