import requests
import json
from datetime import datetime

api_key=""
time_template="%H:%M:%S"+'.000Z'
date_template="%Y-%m-%d"
def find_product_id(key,name,base_url):
    header={
    "Content-Type": "application/json",
    'Authorization': f"Token {key}",
    "Accept":"application/json"
    }
    endpoint=base_url+"/api/v2/products/"
    data={
        'name':name,
    }
    hasil=json.loads(requests.get(endpoint,data,headers=header).text)

    product_id=hasil['results'][0]['id']
    return product_id

def get_engange_len(key,name,base_url):
    header={
    "Content-Type": "application/json",
    'Authorization': f"Token {key}",
    "Accept":"application/json"
    }
    endpoint=base_url+"/api/v2/engagements/"
    data={
        'product':name,
    }
    hasil=json.loads(requests.get(endpoint,data,headers=header).text)
    engage_len=len(hasil['results'])
    return engage_len

def check_engage(key,engage_name,base_url):
    header={
    "Content-Type": "application/json",
    'Authorization': f"Token {key}",
    "Accept":"application/json"
    }
    print('[*] Checking if engage exist')
    endpoint=base_url+"/api/v2/engagements/"
    data={
        'name':engage_name,
    }
    hasil=json.loads(requests.get(endpoint,data,headers=header).text)
    return (hasil['count']>0)

def find_engage(key,engage_name,base_url):
    header={
    "Content-Type": "application/json",
    'Authorization': f"Token {key}",
    "Accept":"application/json"
    }
    endpoint=base_url+"/api/v2/engagements/"
    data={
        'name':engage_name
    }
    hasil=json.loads(requests.get(endpoint,data,headers=header).text)
    return (hasil['results'][0]['id'])

def create_engage(key,engage_name,product_name,base_url):
    header={
    "Content-Type": "application/json",
    'Authorization': f"Token {key}",
    "Accept":"application/json"
    }
    if(check_engage(key,engage_name,base_url)):
        engage_id=find_engage(key,engage_name,base_url)
        print('[+] Engagements already exist')
        return engage_id
    print("[-] Engagements aren't exist yet")
    print('[*] Creating Engangement')
    endpoint=base_url+"/api/v2/engagements/"
    product_id=find_product_id(key,product_name,base_url)
    today=datetime.now()
    data={
        'name': engage_name,
        'target_start':today.strftime(date_template),
        'target_end':today.strftime(date_template),
        'created':today.strftime(date_template)+'T'+today.strftime(time_template),
        'product':product_id
    }
    hasil=json.loads(requests.post(endpoint,json=data,headers=header).text)
    print('[+] Done Creating Engagement')
    return hasil['id']

def create_test(key,engage_name,product_name,base_url):
    header={
    "Content-Type": "application/json",
    'Authorization': f"Token {key}",
    "Accept":"application/json"
    }
    engage_id=create_engage(key,engage_name,product_name,base_url)
    today=datetime.now()
    endpoint=base_url+"/api/v2/tests/"
    data={
        'title':today.strftime(time_template),
        'engagement':engage_id,
        'target_start':today.strftime(date_template)+'T'+today.strftime(time_template),
        'target_end':today.strftime(date_template)+'T'+today.strftime(time_template),
        'test_type':157,#87 = snyk, #157 = trufflehog
    }
    hasil=json.loads(requests.post(endpoint,json=data,headers=header).text)
    return hasil['id']

def import_scan(key,engage_name,product_name,base_url,file_name):
    header={
    'Authorization': f"Token {key}",
    "Accept":"application/json"
    }
    json_data=open(file_name,'rb')
    
    endpoint=base_url+"/api/v2/import-scan/"
    engage_id=create_engage(key,engage_name,product_name,base_url)
    today=datetime.now()
    data={
        'product_name':product_name,
        'engagement_name':engage_name,
        'scan_date':today.strftime(date_template),
        'minimum_severity':'Info',
        'active':"true",
        'verified':"false",
        'scan_type':'Trufflehog Scan',
        'tag':'yes',
    }
    print('[*] importing')
    hasil=json.loads(requests.post(endpoint,files={'file':json_data},data=data,headers=header).text)
    return '[+] finish importing'