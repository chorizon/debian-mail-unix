#!/usr/bin/python3

import subprocess
import argparse
import pwd
import re
import os
import shutil
import sys

from chorizon.basic import check_domain, add_line, del_line, add_user, del_user, set_quota_grp, obtain_mountpoint_file 

parser = argparse.ArgumentParser(description='A simple script for add an new domain and user')

parser.add_argument('--domain', help='The domain to create', required=True)
parser.add_argument('--user', help='The user father of all accounts of this domain', required=True)

args = parser.parse_args()

#Check if valid domain

#Add user

args.user=args.user+'@'+args.domain

# delete entry in directory 

domain_line=args.domain+" "+args.domain

if not del_line(domain_line, '/etc/postfix/virtual_domains'):
    print('{"PROGRESS": 100, "MESSAGE": "ERROR: THE DOMAIN DOESN\'T EXISTS IN THIS SERVER", "ERROR":1, "CODE_ERROR": 1}')
    exit(1)

print('{"PROGRESS": 50, "MESSAGE": "Domain deleted from server", "ERROR":0, "CODE_ERROR": 0}')

if not del_user(args.user):
    print('{"PROGRESS": 100, "MESSAGE": "ERROR: THE USER DOESN\'T EXISTS", "ERROR":1, "CODE_ERROR": 1}')
    exit(1)

print('{"PROGRESS": 100, "MESSAGE": "User for this domain deleted from server", "ERROR":0, "CODE_ERROR": 0}')

"""
if not add_user(args.user, '/home/mailboxes'):
    print('{"PROGRESS": 100, "MESSAGE": "ERROR: CANNOT CREATE THE USER, CHECK IF HAVE PERMISSIONS TO CREATE NEW USER", "ERROR":1, "CODE_ERROR": 1}')
    exit(1)
else:

    print('{"PROGRESS": 25, "MESSAGE": "Created Account for this domain", "ERROR":0, "CODE_ERROR": 0}')

#Add domain to /etc/postfix/virtual_domains.

if not add_line(args.domain+' '+args.domain, "/etc/postfix/virtual_domains"):
    print('{"PROGRESS": 100, "MESSAGE": "ERROR: CANNOT ADD DOMAIN TO MAIL SERVER", "ERROR":1, "CODE_ERROR": 2}')
    exit(1)
    
print('{"PROGRESS": 50, "MESSAGE": "Added new domain", "ERROR":0, "CODE_ERROR": 0}')

#Add quota for this user.

# "setquota -g "+args.user+" "+quota*1024+" "+(quota*1024+4024)

quota=int(args.quota)

if quota>0:
    
    mountpoint=obtain_mountpoint_file('/home')
    
    if not set_quota_grp(args.user, quota, mountpoint):
        #delete domain
        print('{"PROGRESS": 100, "MESSAGE": "ERROR: CANNOT ADD QUOTA TO THIS USER", "ERROR":1, "CODE_ERROR": 3}')
        exit(1)
        
print('{"PROGRESS": 75, "MESSAGE": "Setting quota", "ERROR":0, "CODE_ERROR": 0}')

print('{"PROGRESS": 100, "MESSAGE": "Finished", "ERROR":0, "CODE_ERROR": 0}')
"""
