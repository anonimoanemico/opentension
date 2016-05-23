import os, sys
from flask import Flask, request
from datetime import datetime

# import libraries at the parent level
root_dir = os.path.abspath("..")
common_lib_dir = os.path.join(root_dir, "lib")
print root_dir
print common_lib_dir
sys.path.append(root_dir)
sys.path.append(common_lib_dir)
from bpreading import BP_value

def create_a_BP_value(request):
    a_diastolic = int(request.args.get('diastolic'))
    a_systolic  = int(request.args.get('systolic'))
    a_date_str  = request.args.get('timestamp')
    a_source    = request.args.get('source')
    a_comment   = request.args.get('comment')
    a_pulse     = int(request.args.get('pulse'))
    a_aritmia   = int(request.args.get('aritmia'))  
    a_profile   = int(request.args.get('profile'))
    
    a_date = datetime.strptime(a_date_str, 'Jun 1 2005  1:33PM', '%Y-%m-%d %H:%M:%S')
    a_timestamp = (a_date - datetime(1970, 1, 1)).total_seconds()
    
    return BP_value(no_read = 0, timestamp = a_timestamp, diastolic = a_diastolic, systolic = a_systolic, pulse = a_pulse, restflag = 0, irregular = a_aritmia, source = a_source, comment = a_comment, profile = a_profile)