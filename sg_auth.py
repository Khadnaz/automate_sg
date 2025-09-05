############################################################
# Version 0.90
# Date Created: 2018-06-28
# Last Update:  2018-06-28
# https://www.neoprime.io
# Copyright (c) 2018, NeoPrime, LLC
# Author: John Hanley
############################################################

""" Add my public IP to an Alibaba Cloud Security Group """

import    os
import    json
import    logging
import    optparse
import    requests
from aliyunsdkcore.client import AcsClient
from aliyunsdkecs.request.v20140526 import AuthorizeSecurityGroupRequest
from aliyunsdkecs.request.v20140526 import RevokeSecurityGroupRequest
from aliyunsdkecs.request.v20140526 import DescribeSecurityGroupAttributeRequest

g_debug = False
g_print = True    # Set to diplay messages to console

LAST_IP_FILENAME = 'last_ip.txt'

# Option 1: ipify (most reliable)
IP_ENDPOINT = 'https://api.ipify.org'

# Option 2: icanhazip
IP_ENDPOINT = 'http://icanhazip.com'

# Option 3: ifconfig.me
IP_ENDPOINT = 'http://ifconfig.me/ip'

# Option 4: ipinfo
IP_ENDPOINT = 'https://ipinfo.io/ip'

PROFILE_NAME = 'sg_auth'    # specify the credentials profile name to use

sg_auth_params = {
    'sg_id': 'sg-l4vimuwylkiv6dk7jxc6',    # Change this value to your security group
    'ip_protocol': 'tcp',
    'port_range': '3389/3389',        # Use this port range for Remote Desktop (RDP)
    'port_range': '22/22',            # Use this port range for SSH
    'description': 'My public IP address',
    'source_cidr_ip': ''
}

logger = logging.getLogger('sg_auth')

def setup_logging():
    """ This creates sets the logging configuration """
    f1 = '%(asctime)s %(name)s %(levelname)s %(message)s'
    f2 = '%(message)s'

    if g_debug is False:
        if g_print is False:
            logging.basicConfig(filename='sg_auth.log', level=logging.INFO, format=f1)
        else:
            logging.basicConfig(level=logging.INFO, format=f2)
    else:
        if g_print is False:
            logging.basicConfig(filename='sg_auth.log', level=logging.DEBUG, format=f1)
        else:
            logging.basicConfig(level=logging.DEBUG, format=f2)

    logger.info('########################################')
    logger.info('Program start')

def usage():
    """ Command Usage Help """
    print("Usage: sg_auth [-d, --debug] [-p, --purge]")

def process_cmdline():
    """ Process the Command Line """
    parser = optparse.OptionParser()

    parser.set_defaults(debug=False, profile=False, region_id=False, slb_id=False)

    parser.add_option(
            '-d',
            '--debug',
            action='store_true',
            dest='debug',
            default=False,
            help="enable debugging")

    parser.add_option(
            '-p',
            '--purge',
            action='store_true',
            dest='purge',
            default=False,
            help="purge security groups rules with same port range")

    parser.add_option(
            '--profile',
            action = 'store',
            dest = 'profile',
            default = PROFILE_NAME,
            help = "specify the credentials profile name")

    (cmd_options, cmd_args) = parser.parse_args()

    return (cmd_options, cmd_args)

def get_current_ip():
    """ Get my public IP address """
    # Try multiple services in case one fails
    ip_services = [
        'https://api.ipify.org',
        'http://icanhazip.com',
        'http://ifconfig.me/ip',
        'https://ipinfo.io/ip'
    ]
    
    for service in ip_services:
        try:
            resp = requests.get(service, timeout=5)
            resp.raise_for_status()
            ip = resp.content.strip().decode('utf-8')
            # Add /32 for CIDR notation
            ip += '/32'
            return ip
        except:
            continue  # Try next service
    
    # If all services fail
    raise Exception("Could not determine public IP address")



def get_last_ip():
    """ Get my last public IP address that was saved """
    if not os.path.exists(LAST_IP_FILENAME):
        return None

    try:
        with open(LAST_IP_FILENAME, 'r') as fp:
            ip = fp.readline().strip()
    except:
        ip = None
    return ip

def save_new_ip(ip):
    """ Save my public IP address """
    with open(LAST_IP_FILENAME, 'w') as fp:
        fp.write(ip + '\n')

def sg_authorize(client, params):
    """ Authorize an IP address """
    # Initialize a request and set parameters
    request = AuthorizeSecurityGroupRequest.AuthorizeSecurityGroupRequest()

    request.set_SecurityGroupId(params['sg_id'])
    request.set_IpProtocol(params['ip_protocol'])
    request.set_PortRange(params['port_range'])
    request.set_Description(params['description'])
    request.set_SourceCidrIp(params['source_cidr_ip'])

    response = client.do_action_with_exception(request)

    if g_debug:
        logger.debug(response)

    r = json.loads(response)

    logger.debug('Request ID: %s', r['RequestId'])

def sg_revoke(client, params):
    """ Revoke an IP address """

    logger.info('Removing IP: %s', sg_auth_params['source_cidr_ip'])

    # Initialize a request and set parameters
    request = RevokeSecurityGroupRequest.RevokeSecurityGroupRequest()

    request.set_SecurityGroupId(params['sg_id'])
    request.set_IpProtocol(params['ip_protocol'])
    request.set_PortRange(params['port_range'])
    request.set_Description(params['description'])
    request.set_SourceCidrIp(params['source_cidr_ip'])

    response = client.do_action_with_exception(request)

    if g_debug:
        logger.debug(response)

    r = json.loads(response)

    logger.debug('Request ID: %s', r['RequestId'])

def purge_rules(client, params):
    """ Remove all rules with the same port range """

    logger.info('Purging all security groups rules for port range %s', params['port_range'])

    # Initialize a request and set parameters
    request = DescribeSecurityGroupAttributeRequest.DescribeSecurityGroupAttributeRequest()

    request.set_SecurityGroupId(params['sg_id'])

    response = client.do_action_with_exception(request)

    if g_debug:
        logger.debug(response)

    r = json.loads(response)

    logger.debug('Request ID: %s', r['RequestId'])

    for permission in r['Permissions']['Permission']:
        if permission['PortRange'] == params['port_range']:
            sg_auth_params['source_cidr_ip'] = permission['SourceCidrIp']
            sg_revoke(client, sg_auth_params)

def main_cmdline(options):
    """ This is the main function """

    last_ip = None
    current_ip = get_current_ip()

    if options.purge is False:
        last_ip = get_last_ip()
        if last_ip == current_ip:
            logger.info('Last ip and current ip are the same. No changes are required.')
            return 0

    # My library for processing Alibaba Cloud Services (ACS) credentials
    # This library is only used when running from the desktop and not from the cloud
    import mycred_acs

    # Load the Alibaba Cloud Credentials (AccessKey)
    logger.info('Loading credentials for profile %s', options.profile)
    credentials = mycred_acs.LoadCredentials(options.profile)

    if options.debug:
        logger.info('Access Key ID: %s', credentials['accessKeyId'])

    if credentials is False:
        logger.error('Error: Cannot load credentials')
        return 1

    # Initialize AcsClient instance
    client = AcsClient(
        credentials['accessKeyId'],
        credentials['accessKeySecret'],
        credentials['region'])

    if options.purge:
        purge_rules(client, sg_auth_params)

    sg_auth_params['source_cidr_ip'] = current_ip

    logger.info('Adding IP:   %s', sg_auth_params['source_cidr_ip'])

    sg_authorize(client, sg_auth_params)

    save_new_ip(current_ip)

    if last_ip is not None:
        sg_auth_params['source_cidr_ip'] = last_ip
        sg_revoke(client, sg_auth_params)

    return 0

# Setup logging
setup_logging()

# Process the command line
(g_options, g_args) = process_cmdline()

if g_options.debug:
    g_debug = True

ret = main_cmdline(g_options)