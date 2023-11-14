import requests
import json
from datetime import datetime

api_key='f0f53e577ad7a3fb95230cada410d1f0bf09e71a'
time_template="%H:%M:%S"+'.000Z'
date_template="%Y-%m-%d"
header={
    "Content-Type": "application/json",
    'Authorization': f"Token {api_key}",
    "Accept":"application/json"
}
def find_product_id(name):
    
    endpoint="http://localhost:8080/api/v2/products/"
    data={
        'name':name,
    }
    hasil=json.loads(requests.get(endpoint,data,headers=header).text)

    product_id=hasil['results'][0]['id']
    return product_id

def get_engange_len(name):
    endpoint="http://localhost:8080/api/v2/engagements/"
    data={
        'product':name,
    }
    hasil=json.loads(requests.get(endpoint,data,headers=header).text)
    engage_len=len(hasil['results'])
    return engage_len

def check_engage(engage_name):
    print('[*] Checking if engage exist')
    endpoint="http://localhost:8080/api/v2/engagements/"
    data={
        'name':engage_name,
    }
    hasil=json.loads(requests.get(endpoint,data,headers=header).text)
   
    return (hasil['count']>0)

def find_engage(engage_name):
    endpoint="http://localhost:8080/api/v2/engagements/"
    data={
        'name':engage_name
    }
    hasil=json.loads(requests.get(endpoint,data,headers=header).text)
    return (hasil['results'][0]['id'])

def create_engage(engage_name,product_name):
    if(check_engage(engage_name)):
        engage_id=find_engage(engage_name)
        print('[+] Engagements already exist')
        return engage_id
    print("[-] Engagements aren't exist yet")
    print('[*] Creating Engangement')
    endpoint="http://localhost:8080/api/v2/engagements/"
    product_id=find_product_id(product_name)
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

def create_test(engage_name,product_name):
    engage_id=create_engage(engage_name,product_name)
    today=datetime.now()
    endpoint="http://localhost:8080/api/v2/tests/"
    data={
        'title':today.strftime(time_template),
        'engagement':engage_id,
        'target_start':today.strftime(date_template)+'T'+today.strftime(time_template),
        'target_end':today.strftime(date_template)+'T'+today.strftime(time_template),
        'test_type':87,
    }
    hasil=json.loads(requests.post(endpoint,json=data,headers=header).text)
    return hasil['id']
