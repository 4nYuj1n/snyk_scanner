import os
import json
import re
import requests
from snyk_create_engage import create_test
from datetime import datetime
import getopt,sys

pattern = r"\[(.*?)\]\((.*?)\)"
api_key=''
run_snyk_code="snyk code test --json > snyk_out.json"
project_name=''
time_template="%H:%M:%S"+'.000Z'
date_template="%Y-%m-%d"
header={
    "Content-Type": "application/json",
    'Authorization': f"Token {api_key}",
    "Accept":"application/json"
}

def convert_severity(score):
    if score < 500 :
        return ["Low","S1"]
    elif score < 600 :
        return ["Medium","S2"]
    elif score < 900 :
        return ["High","S3"]
    else:
        return ["Critical","S4"]

def abreviate(txt):
    if txt=="PT":
        return "Path Traversal"
    elif txt=="OR":
        return "Open Redirect"
    else:
        return txt

def snyk_scanning(test_id):
    print("[+] Starting Scanner")
    print("[*] scanning...")
    os.system(run_snyk_code)
    print("[+] Done scanning")
    print('[*] Importing to defect dojo')
    snyk_file=open('snyk_out.json').read()
    snyk_file=json.loads(snyk_file)
    
    print(f'[*] start importing to {test_id}')
    for j in snyk_file["runs"][0]['results']:
        Title = abreviate(j['ruleId'])
        severity = j['properties']['priorityScore']
        desc  = j['message']['text']+", Score : "+str(severity)+", Line : "+str(j['locations'][0]['physicalLocation']['region']['startLine'])+' - '+str(j['locations'][0]['physicalLocation']['region']['endLine'])
        File_Path= j['codeFlows'][0]['threadFlows'][0]['locations'][0]['location']['physicalLocation']['artifactLocation']['uri']
        data={
            'test':test_id,
            'found_by':[1],
            'title':Title,
            'severity':convert_severity(int(severity))[0],
            'description':desc,
            'active':'True',
            'file_path':File_Path,
            'verified':'False',
            'numerical_severity':convert_severity(int(severity))[1]
        }
        r=requests.post('http://localhost:8080/api/v2/findings/',json=data,headers=header)

    print('[+] done importing')

if __name__=='__main__':

    argumentList=sys.argv[1:]
    options="p:k:"
    long_options=["projectName=","apiKey="]
    arguments, values = getopt.getopt(argumentList, options, long_options)
    for argument,value in arguments:
        if argument in ('-p','--projectName'):
            project_name=value
        elif argument in ('-k','--apiKey'):
            api_key=value

    if api_key=='':
        raise ValueError("Test failed: API key not provided")
    if project_name=='':
        raise ValueError("Test failed: project name not provided")

    today=datetime.now()
    try:
        engage_name=project_name+'_'+today.strftime(date_template)
        test_id=create_test(engage_name,project_name)
    except:
        raise ValueError("Test failed: Failed creating test")
    try:
        snyk_scanning(test_id)
    except:
        raise ValueError("Test failed: Failed uploading scan")
