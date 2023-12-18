import os
import json
import re
import requests
from defect_dojo_api import *
from datetime import datetime
import getopt,sys

pattern = r"\[(.*?)\]\((.*?)\)"
api_key=''

project_name=''
time_template="%H:%M:%S"+'.000Z'
date_template="%Y-%m-%d"

if __name__=='__main__':
    print("[+] Start importing...")
    
    argumentList=sys.argv[1:]
    options="f:p:k:u:"
    long_options=["File=,projectName=","apiKey=","URL="]
    arguments, values = getopt.getopt(argumentList, options, long_options)
    for argument,value in arguments:
        if argument in ('-p','--projectName'):
            project_name=value
        elif argument in ('-k','--apiKey'):
            api_key=value
        elif argument in ('-u','--URL'):
            base_url=value
        elif argument in ('-f','--File'):
            file_path=value
    if api_key=='':
        raise ValueError("Test failed: API key not provided")
    if project_name=='':
        raise ValueError("Test failed: project name not provided")

    today=datetime.now()
    try:
        engage_name=project_name+'_'+today.strftime(date_template)
    except:
        raise ValueError("Test failed: Failed creating test")
    try:
        print(import_scan(api_key,engage_name,project_name,base_url,file_path))
    except:
        raise ValueError("Test failed: Failed uploading scan")
