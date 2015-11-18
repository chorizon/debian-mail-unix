#!/usr/bin/python3

import subprocess
import argparse
import pwd
import re
import os
import shutil
import sys

from chorizon.basic import check_domain, add_line, add_user, set_quota_grp, obtain_mountpoint_file 

"""
def check_domain(domain):
    
    pattern='[a-zA-Z\d-]{,63}(\.[a-zA-Z\d-]{,63})*'

def add_line(line, file_line):

    line=line.strip()

    line_exists=0

    try:

        file=open(file_line, 'r')
    
    except:
        
        return False

    for old_line in file:
        old_line=old_line.strip()
        
        if old_line == line:
            line_exists=1

    file.close()

    if line_exists==0:
        
        try:
        
            file=open(file_line, 'a')
            
            file.write(line+"\n")

            file.close()
        
            return True
        
        except:
            
            return False
        

def add_user(username, home_base='/home', clean_user=True):

    user_folder=home_base+"/"+username

    try:

        user_check=pwd.getpwnam(username)

        if clean_user==True:
            return False
        else:
            return True

    except KeyError:

        if not os.path.isdir(home_base):
            os.mkdir(home_base, 0o755)
            
        if not os.path.isdir(user_folder):
            os.mkdir(user_folder, 0o755)

        if subprocess.call("sudo useradd -M -d "+user_folder+" -s /usr/sbin/nologin "+username,  shell=True) > 0:
            return False
        else:
            
            shutil.chown(user_folder, username, username)
            
            return True

#Save quota in mb

def set_quota_grp(group, quota, filesystem):
    
    #quotatool -u johan -b -q 50G -l 50G /home
    #Check 
    
    #print("sudo quotatool -g "+group+" -b -q "+str(quota)+"M -l "+str(quota+2048)+"M "+filesystem)
    #Check where is the /home directory
    
    # df -h .
    
    quota_hard=quota+2
    
    if subprocess.call("sudo quotatool -g "+group+" -b -q "+str(quota)+"M -l "+str(quota_hard)+"M "+filesystem,  shell=True) > 0:
        return False
    else:
        return True

def obtain_mountpoint_file(file_path):

    df = subprocess.Popen(["df", file_path], stdout=subprocess.PIPE)
    output = df.communicate()[0]
    
    device, size, used, available, percent, mountpoint = output.decode('utf-8').split("\n")[1].split()
    
    return  mountpoint

"""

parser = argparse.ArgumentParser(description='A simple script for add an new domain and user')

parser.add_argument('--domain', help='The domain to create', required=True)
parser.add_argument('--user', help='The user father of all accounts of this domain', required=True)
parser.add_argument('--quota', help='The total quota for this domain.Zero for no limits', required=True)
parser.add_argument('--num_accounts', help='The num of accounts of this domain.Zero for no limits', required=True)
#parser.add_argument('--filesystem', help='The filesystem where make the quota', required=True)

args = parser.parse_args()

#Check if valid domain

#Add user

args.user=args.user+'@'+args.domain

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

